#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


"""
Test Engine
"""
import os
import inspect
import importlib
import threading
import traceback
from enum import Enum
from pkginfo import Installed
from pkg_resources import get_distribution

from testbot.config import CONFIG_PATH, RUNNER_LOGS_PATH, CASE_LOGS_PATH
from testbot.app.case.precondition import IsTestCaseType, IsTestCasePriority, IsPreCasePassed, IsHigherPriorityPassed
from testbot.config.setting import static_setting, SettingBase
from testbot.result.testreporter import StepReporter
from testbot.app.case.base import TestCaseBase
from testbot.resource.error import ResourceLoadError, ResourceNotRelease
from testbot.resource.pool import ResourcePool
from testbot.testengine.testlist import TestList
from testbot.result.logger import logger_manager
from testbot.utilities.time import get_time_stamp


@static_setting.setting("CaseRunner")
class CaseRunnerSetting(SettingBase):
    """
    The case runner setting
    """
    default_case_setting_path = CONFIG_PATH
    log_path = RUNNER_LOGS_PATH
    case_log = CASE_LOGS_PATH
    log_level = "INFO"


class CaseImportError(Exception):
    def __init__(self, msg, inner_ex=None):
        super().__init__(msg)
        self.inner_ex = inner_ex


class TestEngineNotReadyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class RunningStatus(Enum):
    Idle = 1
    Running = 3


class CaseRunner(object):
    """
    测试用例执行器
    """
    def __init__(self):
        self.resource_pool = None
        self.list_setting = None
        self.test_list = None
        self.case_tree = dict()
        self.priority_list = list()
        self.pre_conditions = list()
        self.status = RunningStatus.Idle
        self.running_thread = None
        self.logger = logger_manager.register("CaseRunner", filename=os.path.join(RUNNER_LOGS_PATH, "CaseRunner.log"), default_level=CaseRunnerSetting.log_level, for_test=True)
        # self.result_report = ResultReporter(logger=self.logger)
        self.step_report = StepReporter.get_instance(logger=self.logger)
        self.logger.info("执行器装载完毕")
        self.case_log_folder = None
        self.case_result = dict()

    def load_resource(self, filename: str = os.path.join(CONFIG_PATH, "pool.json"), owner: str = "sunny"):
        """
        加载测试资源

        :param file_name: 资源文件路径
        :type file_name: str
        :param username: 资源拥有者
        :type username: str
        :return:
        :rtype:
        """
        self.resource_pool = ResourcePool()
        try:
            # 执行设备发现和端口发现
            self.resource_pool.discover_resources(filename=filename, owner=owner)
        except ResourceLoadError as rle:
            #资源文件读取错误
            self.logger.exception(rle)
            self.resource_pool = None
        except ResourceNotRelease as rnr:
            #资源文件被占用
            self.logger.exception(rnr)
            self.resource_pool = None
        except Exception as ex:
            self.logger.exception(ex)
            # self.resource_pool = None
        self.logger.info("测试资源装载完毕")

    @property
    def resource_ready(self):
        """
        资源是否已准备好

        :return:
        :rtype:
        """
        return self.resource_pool is not None

    @property
    def test_list_ready(self):
        """
        测试用例列表是否已准备好

        :return:
        :rtype:
        """
        return self.test_list is not None

    def load_test(self, test_name: str, iterations: int = 1) -> TestCaseBase:
        """
        实例化测试用例

        :param test_name: 测试名称
        :type test_name: str
        :return:
        :rtype:
        """
        # 获取测试用例的模块名和类名
        case_module_name = ".".join(test_name.split(".")[0: -1])
        case_name = test_name.split(".")[-1]
        try:
            self.logger.info(f"正在加载用例模块: {case_module_name}...")
            self.print_module_info()
            case_module = importlib.import_module(case_module_name)
            return getattr(case_module, case_name)(reporter=self.step_report, pool=self.resource_pool, iterations=iterations)
        except Exception as ex:
            traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
            # 导入测试用例失败，抛出异常
            raise CaseImportError("Failed to Import Test Case %s" % test_name, traceinfo)

    def print_module_info(self):
        self.logger.info("#" * 80)
        fwk_versions = {
            "testbot": None,
            "testbot_aw": None,
            "testbot_apps": None
        }
        for key in fwk_versions:
            pkg = None
            location = None
            try:
                pkg = Installed(key)
                location = get_distribution(key)
            except:
                pass
            self.logger.info(f"############## {key}模块 【Version】:{pkg.version},【概要】:{pkg.summary},【安装路径】:{str(location)} ##############")
        self.logger.info("#" * 80)

    def set_test_list(self, test_list: TestList):
        """
        #装载测试列表
        """
        self.test_list = test_list
        self.list_setting = None
        self.case_tree.clear()
        self._import_list_case(self.case_tree, self.test_list)
        if any(self.test_list.setting.priority_to_run):
            self.priority_list = self.test_list.setting.priority_to_run
        self.logger.info("测试列表装载完毕")

    def start(self):
        """
        测试引擎开始执行
        """
        if self.status == RunningStatus.Running:
            return
        if not self.resource_ready:
            raise TestEngineNotReadyError("测试引擎未准备就绪，测试资源未装载")
        if self.test_list is None:
            raise TestEngineNotReadyError("测试引擎未准备就绪，测试列表未装载")
        self.status = RunningStatus.Running
        self.case_log_folder = os.path.join(CaseRunnerSetting.case_log, get_time_stamp())
        self.running_thread = threading.Thread(target=self.__main_test_thread)
        self.running_thread.start()

    def wait_for_test_done(self):
        """
        等待测试完成

        :return:
        :rtype:
        """
        self.running_thread.join()

    def run_case_lcm(self, test: TestCaseBase):
        """
        执行测试用例生命周期管理
        这个方法应该在子线程被运行
        """
        self.__init_precondition(test)
        if not self.__pre_check(test):
            return
        self.__run_case(test=test)

    def _import_list_case(self, case_tree_node, test_list, log_path=None):
        """
        递归导入测试列表中的测试用例
        """
        case_log_path = test_list.test_list_name
        if log_path:
            case_log_path = log_path + "/" + case_log_path
        case_tree_node["list_name"] = test_list.test_list_name
        case_tree_node["iterations"] = test_list.iterations
        case_tree_node["test_cases"] = list()
        for testcase in test_list.test_cases:
            if testcase.strip() == "":
                continue
            case_descriptor = dict()
            case_entry = testcase.split(",")
            case_name = case_entry[0]
            case_setting_file = ""
            if len(case_entry) > 1:
                case_setting_file = case_entry[1]
            try:
                # 导入测试用例
                case_descriptor['case'] = self.load_test(test_name=case_name, iterations=test_list.iterations)
                case_descriptor['case_name'] = case_name.split(".")[-1]
                case_descriptor['log_path'] = case_log_path
                case_descriptor['filename'] = case_setting_file
                # 设置测试用例配置文件路径
                if test_list.setting.case_setting_path:
                    case_descriptor['setting_path'] = test_list.setting.case_setting_path
                else:
                    case_descriptor['setting_path'] = os.path.dirname(inspect.getfile(case_descriptor['case'].__class__)) if case_descriptor['case'] else CaseRunnerSetting.default_case_setting_path
                case_priority = getattr(case_descriptor['case'], "priority", 999)
                if case_priority not in self.priority_list:
                    self.priority_list.append(case_priority)
            except CaseImportError as cie:
                # 测试用例导入失败
                self.logger.error(f"不能导入测试用例{case_name}")
                self.logger.exception(cie)
            case_tree_node['test_cases'].append(case_descriptor)
        case_tree_node['sub_list'] = list()
        for sub_list in test_list.sub_list:
            sub_list_dict = dict()
            case_tree_node['sub_list'].append(sub_list_dict)
            self._import_list_case(sub_list_dict, sub_list, log_path=case_log_path)

    def __init_precondition(self, test: TestCaseBase):
        self.pre_conditions.clear()
        self.pre_conditions.append(IsTestCaseType(self.test_list.setting.run_type))
        if any(self.test_list.setting.priority_to_run):
            self.pre_conditions.append(IsTestCasePriority(self.test_list.setting.priority_to_run))
        if any(test.pre_tests):
            self.pre_conditions.append(IsPreCasePassed(self.case_result))
        self.pre_conditions.append(IsHigherPriorityPassed(test.priority, self.case_result))

    def __pre_check(self, test:TestCaseBase):
        for condition in self.pre_conditions:
            if not condition.is_meet(test, reporter=self.step_report):
                self.step_report.logger.info(f"{test.__class__.__name__}不能执行！")
                return False
        return True

    def __get_case_log(self, path, case_name):
        log_path = os.path.join(self.case_log_folder, path, f"{case_name}.log")
        return logger_manager.register(logger_name=case_name, filename=log_path, is_test=True)

    def __main_test_thread(self):
        try:
            self.__run_test_list(self.case_tree)
        finally:
            self.status = RunningStatus.Idle

    def __run_test_list(self, testlist):
        for test in testlist['test_cases']:
            test["case"].get_setting(test["setting_path"], test["filename"])
            temp_logger = self.step_report.logger
            self.step_report.logger = self.__get_case_log(path=test['log_path'], case_name=test['case_name'])
            self.logger.info(f"切换日志路径：{temp_logger.handlers[0].baseFilename} -> {self.step_report.logger.handlers[0].baseFilename}")
            self.case_result[test["case_name"]] = dict()
            self.case_result[test["case_name"]]['priority'] = test["case"].priority
            self.case_result[test["case_name"]]['result'] = False
            self.run_case_lcm(test=test['case'])
            self.step_report.logger = temp_logger
            self.logger.info(f"切换日志路径：{self.step_report.logger.handlers[0].baseFilename} -> {temp_logger.handlers[0].baseFilename}")
            logger_manager.unregister(test['case_name'])
        for list in testlist['sub_list']:
            self.__run_test_list(list)

    def __run_case(self, test: TestCaseBase):
        """
        测试用例执行线程
        """
        test.start()
