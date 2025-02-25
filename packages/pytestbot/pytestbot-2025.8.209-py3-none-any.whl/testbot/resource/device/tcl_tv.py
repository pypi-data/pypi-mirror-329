#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.device.device import TVDevice


class TCLTVDevice(TVDevice):
    """
    TCL电视设备类
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
        return dict()


if __name__ == "__main__":
    device = TCLTVDevice(name="TV1")
    device.logger.info("This is TCL TV Device")
