#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.device import TVDevice


class TCLTVDevice(TVDevice):
    """
    TCL电视设备类
    """
    # 接口模块类列表
    MODULES = [
        "testbot.resource.modules.tv_device_module.PowerModule",
        "testbot.resource.modules.tv_device_module.AudioModule",
        "testbot.resource.modules.tv_device_module.CaptureCardModule",
        "testbot.resource.modules.tv_device_module.CommSerialModule",
        "testbot.resource.modules.tv_device_module.InfraredSerialModule",
        "testbot.resource.modules.tv_device_module.ADBModule"
    ]

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict()


if __name__ == "__main__":
    device = TCLTVDevice(name="TV1")
    device.logger.info("This is TCL TV Device")
