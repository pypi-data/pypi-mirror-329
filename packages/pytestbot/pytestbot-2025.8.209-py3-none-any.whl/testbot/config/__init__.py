#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


import os
from pathlib import Path

# 根目录，若环境变量TBOT_PATH指定了一个目录并且目录是有效的，则使用它，否则设置为默认的~/TBOT目录
ROOT_PATH = os.environ.get("TB_HOME", None)
if ROOT_PATH:
    try:
        if not os.path.exists(ROOT_PATH):
            os.makedirs(ROOT_PATH)
        ROOT_PATH = os.environ.get("TB_HOME", None)
    except:
        ROOT_PATH = os.path.join(str(Path.home()), "TESTBOT")
else:
    ROOT_PATH = os.path.join(str(Path.home()), "TESTBOT")

# 配置目录
CONFIG_PATH = os.path.join(ROOT_PATH, "configs")
if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

# 日志目录，模块日志目录、用例日志目录、执行器日志目录
LOGS_PATH = os.path.join(ROOT_PATH, "logs")
if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH)

MODULE_LOGS_PATH = os.path.join(LOGS_PATH, "modules")
if not os.path.exists(MODULE_LOGS_PATH):
    os.makedirs(MODULE_LOGS_PATH)

CASE_LOGS_PATH = os.path.join(LOGS_PATH, "cases")
if not os.path.exists(CASE_LOGS_PATH):
    os.makedirs(CASE_LOGS_PATH)

RUNNER_LOGS_PATH = os.path.join(LOGS_PATH, "runner")
if not os.path.exists(RUNNER_LOGS_PATH):
    os.makedirs(RUNNER_LOGS_PATH)

TESTBOT_ROOT = os.path.dirname(os.path.dirname(__file__))
