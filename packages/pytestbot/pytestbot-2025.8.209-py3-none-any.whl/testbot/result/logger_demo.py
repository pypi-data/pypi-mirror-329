#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
from pathlib import Path
from tbot.result.logger import logger_manager


if __name__ == "__main__":
    RESOURCE_LOGGER_FILENAME = os.path.join(str(Path.home()), "TBOT", "logs", "Resource.log")
    TC_LOGGER_FILENAME = os.path.join(str(Path.home()), "TBOT", "logs", "TestCase.log")

    # 注册Resource模块日志对象
    resource_module_logger = logger_manager.register(logger_name="Resource", filename=RESOURCE_LOGGER_FILENAME, for_test=True)
    # 注册用例对象
    tc_logger = logger_manager.register(logger_name="TestCase", filename=TC_LOGGER_FILENAME, is_test=True)

    # Resource模块日志打印信息
    resource_module_logger.info("这是Resource模块日志")
    # 用例日志打印信息
    tc_logger.info("这是用例日志")

    # 在用例执行结束后，去注册用例日志
    logger_manager.unregister("TestCase")

