#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import json
import os.path
import shutil
import traceback
from abc import abstractmethod

from testbot.config import TESTBOT_ROOT
from testbot.resource.pool import ResourcePool
from testbot.plugin.plugin_base import PluginType
from testbot.resource.error import ResourceNotMeetConstraintError
from testbot.app.base import TestApplicationBase


class TestCaseBase(TestApplicationBase):
    """
    测试用例基类

    用户应该实现以下3个方法：
        * collect_resource: 初始化资源对象
        * setup: 测试执行之前的初始化工作
        * test: 测试执行体
        * cleanup: 测试执行之后的清理工作
    """

    def __init__(self, **kwargs):
        super(TestCaseBase, self).__init__(**kwargs)
        self.iterations = kwargs.get("iterations", 1)
        self._output_var = dict()
        self.setting = None
        self.test_data_var = dict()
        self.result = None

    @abstractmethod
    def collect_resource(self, **kwargs):
        """
        初始化资源对象

        :param pool: 资源池
        :type pool: ResourcePool
        :return:
        :rtype:
        """
        pass

    def setup_class(self, **kwargs):
        """
        执行测试之前的初始化工作

        :param args:
        :return:
        """
        pass

    @abstractmethod
    def setup(self, **kwargs):
        """
        执行测试的每个循环之前的初始化工作

        :param args:
        :return:
        """
        pass

    @abstractmethod
    def test(self, **kwargs):
        """
        测试执行体

        :param args:
        :return:
        """
        pass

    @abstractmethod
    def cleanup(self, **kwargs):
        """
        执行每个循环之后的清理工作

        :param args:
        :return:
        """
        pass

    def cleanup_class(self, **kwargs):
        """
        执行测试之后的清理工作

        :param args:
        :return:
        """
        pass

    @property
    def output_var(self):
        """
        The test case output variable
        Can be collected by Test Engine
        :return:
        """
        return self._output_var

    def get_setting(self, setting_path, filename):
        """
        获取测试用例配置文件实例

        """
        for k, v in self.__class__.__dict__.items():
            if hasattr(v, "__base__") and v.__base__.__name__ == "TestSettingBase":
                self.setting = v(setting_path=setting_path, filename=filename)
                self.setting.load()

    def _run_case(self):
        """
        测试用例执行线程
        """
        _continue = True
        with self._tc_case.start(headline="收集测试资源", message="", prefix="COLLECT_RESOURCE") as self.step:
            # 执行测试资源初始化
            self.pool.init_resources(test_type=getattr(self, "test_type", None))
            try:
                self.collect_resource()
            except ResourceNotMeetConstraintError as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.step.info(message=f"收集测试资源，测试资源不满足条件: {traceinfo}")
                _continue = False
                raise ex
            except Exception as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.logger.error(traceinfo)
                self.step.info(message=f"捕获异常: {traceinfo}")
                _continue = False
                raise ex
            finally:
                pass

        if not _continue:
            return

        with self._tc_case.start(headline="初始化测试", message="", prefix="SETUP_CLASS") as self.step:
            try:
                self.setup_class()
            except ResourceNotMeetConstraintError as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.step.info(message=f"初始化测试失败: {traceinfo}")
                _continue = False
                raise ex
            except Exception as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.logger.error(traceinfo)
                self.step.info(message=f"捕获异常: {traceinfo}")
                _continue = False
                raise ex
            finally:
                pass

        if not _continue:
            return

        with self._tc_case.start(headline=f"执行次测试", message="", prefix="TEST") as step:
            for iteration in range(self.iterations):
                iteration = iteration + 1

                self.logger.info(f"执行第{iteration}次测试")
                with step.start(headline=f"执行第{iteration}次测试", message="", prefix=f"TEST-{iteration}") as step2:
                    with step2.start(headline="执行前置插件", message="", prefix="RUN_PRE_PLUGINS") as self.step:
                        self.plugin_manager.step = self.step
                        # 执行PRE插件
                        self.plugin_manager.run_plugin(PluginType.PRE)
                        # 执行PARALLEL插件
                        self.plugin_manager.run_plugin(PluginType.PARALLEL)

                    with step2.start(headline="初始化前置条件", message="", prefix="SETUP") as self.step:
                        try:
                            self.setup()
                        except Exception as ex:
                            traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                            self.logger.error(traceinfo)
                            self.step.info(message=f"捕获异常: {traceinfo}")
                            self.__call_cleanup(step=step2)
                            return

                    with step2.start(headline="执行测试主体", message="", prefix="SETUP") as self.step:
                        try:
                            self.test()
                        except Exception as ex:
                            traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                            self.logger.error(traceinfo)
                            self.step.info(message=f"捕获异常: {traceinfo}")
                            self.__call_cleanup(step=step2)
                            return

                    self.__call_cleanup(step=step2)

                    with step2.start(headline="执行后置插件", message="", prefix="RUN_POST_PLUGINS") as self.step:
                        self.plugin_manager.step = None
                        # 停止执行PARALLEL插件
                        self.plugin_manager.stop_plugin()
                        # 执行POST插件
                        self.plugin_manager.run_plugin(PluginType.POST)

                # self.reporter.logger = temp_logger
                # self.logger.info(f"切换日志路径：{self.reporter.logger.handlers[0].baseFilename} -> {temp_logger.handlers[0].baseFilename}")
                # logger_manager.unregister(f"{self.__class__.__name__}_{iteration}")

        with self._tc_case.start(headline="清理测试", message="", prefix="CLEANUP_CLASS") as self.step:
            try:
                self.cleanup_class()
            except ResourceNotMeetConstraintError as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.step.info(message=f"清理测试失败: {traceinfo}")
                _continue = False
                raise ex
            except Exception as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.logger.error(traceinfo)
                self.step.info(message=f"捕获异常: {traceinfo}")
                _continue = False
                raise ex
            finally:
                pass

        if not _continue:
            return

    def __call_cleanup(self, step):
        """
        执行清除操作
        """
        with step.start(headline="清理后置条件", message="", prefix="CLEANUP") as self.step:
            try:
                self.cleanup()
            except Exception as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.logger.error(traceinfo)
                self.step.info(message=f"捕获异常: {traceinfo}")
                raise ex
            finally:
                pass

    def start(self):
        try:
            self._run_case()
        except Exception as e:
            self._write_result()
            # 重新抛出异常
            raise e
        finally:
            self._write_result()

    def _write_result(self):
        self.logger.info(self.reporter.root.get_friend_print())
        data = self.reporter.root.to_dict()
        self.logger.info(json.dumps(data))

        log_path = os.path.dirname(self.logger.handlers[0].baseFilename)
        result_path = os.path.join(log_path, "result.json")
        self.logger.info(f"结果文件保存到{result_path}")
        with open(result_path, 'w', encoding="UTF-8") as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)

        src_result_html_path = os.path.join(TESTBOT_ROOT, "result", "result.html")
        dst_result_html_path = os.path.join(log_path, "result.html")
        self.logger.info(f"将HTML结果模板文件{src_result_html_path}拷贝到{dst_result_html_path}")
        if os.path.exists(src_result_html_path) and not os.path.exists(dst_result_html_path):
            shutil.copyfile(src_result_html_path, dst_result_html_path)
