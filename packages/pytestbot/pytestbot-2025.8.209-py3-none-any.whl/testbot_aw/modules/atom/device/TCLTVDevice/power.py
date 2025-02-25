#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TCLTVDevice设备原子接口模块类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.module import TCLTVDeviceAtomModuleBase


class PowerAtomModule(TCLTVDeviceAtomModuleBase):
    """
    TCLTV测试设备源原子接口电源模块类
    """

    def power_on(self) -> bool:
        """
        给TCL TV设备上电

        :return: 上电是否成功
        :rtype: bool
        """
        self.logger.info("给TV设备上电")
        return False

    def power_off(self) -> bool:
        """
        给TCL TV设备断电

        :return: 断电是否成功
        :rtype: bool
        """
        self.logger.info("给TV设备断电")
        return False

