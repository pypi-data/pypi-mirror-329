#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.modules.device_module import DeviceModuleBase


class AndroidDeviceModuleBase(DeviceModuleBase):
    """
    Android测试设备源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(AndroidDeviceModuleBase, self).__init__(resource, *args, **kwargs)


class TVDeviceModuleBase(AndroidDeviceModuleBase):
    """
    TV测试设备源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TVDeviceModuleBase, self).__init__(resource, *args, **kwargs)

    def get_brand(self):
        self.logger.info("获取品牌名称")
        return "TCL"


class TCLTVDeviceModuleBase(TVDeviceModuleBase):
    """
    TCL TV测试设备源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TCLTVDeviceModuleBase, self).__init__(resource, *args, **kwargs)


class PowerModule(TCLTVDeviceModuleBase):
    """
    TCL TV电源模块API接口集
    """

    def set_power(self, on: bool) -> bool:
        """
        给TCL TV设备上电或断电

        :param on: True是上电，False是断电
        :type on: bool
        :return: 是否断电或上电成功
        :rtype: bool
        """
        self.logger.info("给TV设备上电/断电")
        return False

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

# tatf.resource.tcl_tv_device.TCLTVDevice.register_module("tatf.resource.modules.tv_device_module.PowerModule")


class AudioModule(TCLTVDeviceModuleBase):
    """
    TCL TV音频模块API接口集
    """
    pass


class CaptureCardModule(TCLTVDeviceModuleBase):
    """
    TCL TV采集卡模块API接口集
    """
    pass


class CommSerialModule(TCLTVDeviceModuleBase):
    """
    TCL TV指令通信串口模块API接口集
    """
    pass


class InfraredSerialModule(TCLTVDeviceModuleBase):
    """
    TCL TV红外遥控串口模块API接口集
    """
    pass


class GRPCModule(TCLTVDeviceModuleBase):
    """
    TCL TV gRPC客户端模块API接口集
    """
    pass


class ADBModule(TCLTVDeviceModuleBase):
    """
    TCL TV ADB客户端模块API接口集
    """
    pass
