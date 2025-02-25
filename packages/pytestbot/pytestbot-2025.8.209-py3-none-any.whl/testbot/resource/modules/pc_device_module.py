#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.modules.device_module import DeviceModuleBase


class PCDeviceModuleBase(DeviceModuleBase):
    """
    PC测试设备源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(PCDeviceModuleBase, self).__init__(resource, *args, **kwargs)


class NetworkModule(PCDeviceModuleBase):
    """
    PC 网络模块API接口集
    """

    def get_ip_address(self) -> str:
        """
        获取IP地址

        :return: IP地址
        :rtype: str
        """
        self.logger.info("获取IP地址")
        return None
