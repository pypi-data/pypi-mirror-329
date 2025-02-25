#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PCDevice设备原子接口模块类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.module import PCDeviceAtomModuleBase


class NetworkAtomModule(PCDeviceAtomModuleBase):
    """
    PC测试设备源原子接口电源模块类
    """

    def get_ip_address(self) -> str:
        """
        获取IP地址

        :return: IP地址
        :rtype: str
        """
        self.logger.info("获取IP地址")
        return None
