#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
from abc import abstractmethod

from testbot.result.logger import logger_manager
from testbot.result.testreporter import StepReporter
from testbot.config import RUNNER_LOGS_PATH
from testbot.app.base import TestApplicationBase


class TestToolBase(TestApplicationBase):
    """
    测试工具基类

    """
    def __init__(self, **kwargs):
        super(TestToolBase, self).__init__(**kwargs)
        self.reporter = kwargs.get("reporter", StepReporter.get_instance(logger=logger_manager.register("CaseRunner", filename=os.path.join(RUNNER_LOGS_PATH, "CaseRunner.log"), default_level="INFO", for_test=True)))
        self.logger = self.reporter.logger
        self._output_var = dict()
        self.setting = None
        self.test_data_var = dict()
        self.result = None

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
        for k,v in self.__class__.__dict__.items():
            if hasattr(v, "__base__") and v.__base__.__name__ == "TestSettingBase":
                self.setting = v(setting_path=setting_path, filename=filename)
                self.setting.load()

    @abstractmethod
    def start(self, **kwargs):
        """
        开始启动工具，执行测试

        :return:
        :rtype:
        """
        pass
