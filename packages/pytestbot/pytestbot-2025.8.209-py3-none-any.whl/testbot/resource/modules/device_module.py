#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.modules.module import ModuleBase


class DeviceModuleBase(ModuleBase):
    """
    测试设备资源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(DeviceModuleBase, self).__init__(resource, *args, **kwargs)


class PowerModule(DeviceModuleBase):
    """
    电源模块API接口集
    """

    def set_power(self, on: bool) -> bool:
        """
        给设备上电或断电

        :param on: True是上电，False是断电
        :type on: bool
        :return: 是否断电或上电成功
        :rtype: bool
        """
        self.logger.info("给设备上电/断电")
        return False

    def power_on(self) -> bool:
        """
        给设备上电

        :return: 上电是否成功
        :rtype: bool
        """
        self.logger.info("给设备上电")
        return False

    def power_off(self) -> bool:
        """
        给设备断电

        :return: 断电是否成功
        :rtype: bool
        """
        self.logger.info("给设备断电")
        return False
