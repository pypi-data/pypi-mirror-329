#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.resource import Port
from testbot.resource.resource import Device


class PCDevice(Device):
    """
    PC主机设备类
    """
    # 接口模块类列表
    MODULES = [
        # 封装模块

        # 原子模块
        "testbot_aw.modules.atom.device.PCDevice.network.NetworkAtomModule",
    ]

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super(PCDevice, self).__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return super(PCDevice, self).to_dict()

    @classmethod
    def from_dict(cls, dict_obj):
        """
        预留反序列化接口，即从字典对象反序列化为Resource对象

        :return: 反序列化后的Resource对象
        :rtype: Resource
        """
        res = PCDevice(**dict_obj)
        for key, value in dict_obj.items():
            if key == "ports":
                ports = dict()
                for port_name, port in value.items():
                    ports[port_name] = Port.from_dict(port, res)
                setattr(res, "ports", ports)
            else:
                setattr(res, key, value)
        return res


class RPIDevice(Device):
    """
    树莓派设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return super(RPIDevice, self).to_dict()


class AndroidDevice(Device):
    """
    安卓设备类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)


class TVDevice(AndroidDevice):
    """
    电视设备类
    """

    # 接口模块类列表
    MODULES = [
        # 封装模块
        "testbot_aw.modules.wrapper.device.TCLTVDevice.bluetooth.BluetoothWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.channel.ChannelWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.factory_mode.FactoryModeWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.multimedia.MultimediaWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.power.PowerWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.settings.SettingsWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.ui.UIWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.wifi.WIFIWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.youtube.YoutubeWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.settings.SettingsWrapperModule",
        "testbot_aw.modules.wrapper.device.TCLTVDevice.commserial.CommSerialWrapperModule",

        # 原子模块
        "testbot_aw.modules.atom.device.TCLTVDevice.demo.DemoAtomModule",
        "testbot_aw.modules.atom.device.TCLTVDevice.adb.ADBAtomModule",
        "testbot_aw.modules.atom.device.TCLTVDevice.audio.AudioAtomModule",
        "testbot_aw.modules.atom.device.TCLTVDevice.capture_card.CaptureCardAtomModule",
        "testbot_aw.modules.atom.device.TCLTVDevice.commserial.CommSerialAtomModule",
        "testbot_aw.modules.atom.device.TCLTVDevice.grpc.GRPCAtomModule",
        "testbot_aw.modules.atom.device.TCLTVDevice.infraserial.InfraredSerialAtomModule",
        "testbot_aw.modules.atom.device.TCLTVDevice.power.PowerAtomModule",
    ]

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return super(TVDevice, self).to_dict()

    @classmethod
    def from_dict(cls, dict_obj):
        """
        预留反序列化接口，即从字典对象反序列化为Resource对象

        :return: 反序列化后的Resource对象
        :rtype: Resource
        """
        res = TVDevice(**dict_obj)
        for key, value in dict_obj.items():
            if key == "ports":
                ports = dict()
                for port_name, port in value.items():
                    ports[port_name] = Port.from_dict(port, res)
                setattr(res, "ports", ports)
            else:
                setattr(res, key, value)
        return res


class PhoneDevice(AndroidDevice):
    """
    手机设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)


class TabletDevice(AndroidDevice):
    """
    平板设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return super(TabletDevice, self).to_dict()


class MonitorDevice(AndroidDevice):
    """
    商显设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return super(MonitorDevice, self).to_dict()
