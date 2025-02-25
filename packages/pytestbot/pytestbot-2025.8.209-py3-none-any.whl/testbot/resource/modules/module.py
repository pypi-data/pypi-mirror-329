#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
from abc import ABCMeta

from testbot.result.logger import logger_manager
from testbot.config import MODULE_LOGS_PATH


class ModuleBase(metaclass=ABCMeta):
    """
    模块基类
    """

    def __init__(self, resource, *args: tuple, **kwargs: dict):
        self.resource = resource
        self.logger = kwargs.get("logger", self.resource.logger if self.resource and getattr(self.resource, "logger", None) else logger_manager.register(logger_name="Resource", filename=os.path.join(MODULE_LOGS_PATH, "Resource.log"), for_test=True))


class SoftwareModuleBase(ModuleBase):
    """
    测试软件资源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(SoftwareModuleBase, self).__init__(resource, *args, **kwargs)


class ServiceModuleBase(ModuleBase):
    """
    测试服务资源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(ServiceModuleBase, self).__init__(resource, *args, **kwargs)
