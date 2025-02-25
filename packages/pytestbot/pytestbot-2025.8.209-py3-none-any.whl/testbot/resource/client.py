#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) TCL DIGITAL TECHNOLOGY (SHENZHEN) CO., LTD."
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@tcl.com"

import os
from abc import ABCMeta, abstractmethod
from testbot.result.logger import logger_manager
from testbot.config import MODULE_LOGS_PATH
from testbot.resource.port_comm import SerialComm


class Client(metaclass=ABCMeta):
    """
    代表客户端抽象基类
    """

    def __init__(self, *args, **kwargs):
        self.logger = kwargs.get("logger", logger_manager.register(logger_name="Resource", filename=os.path.join(MODULE_LOGS_PATH, "Resource.log"), for_test=True))

    @abstractmethod
    def _login(self):
        pass

    @abstractmethod
    def connect(self):
        pass


class SerialClient(Client, SerialComm):
    def _login(self):
        self.logger.info("_login")

    def connect(self):
        self.logger.info("connect")
