#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Device设备原子接口模块类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.module import DeviceAtomModuleBase


class PowerAtomModule(DeviceAtomModuleBase):
    """
    电源模块原子接口类
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
