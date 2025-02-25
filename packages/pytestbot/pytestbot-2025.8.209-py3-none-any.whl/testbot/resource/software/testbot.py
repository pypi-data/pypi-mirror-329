#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.resource import Software
from testbot.config.setting import dynamic_setting, SettingBase


@dynamic_setting
class TestBotSoftware(Software):
    """
    TestBot测试软件类
    """

    # 接口模块类列表
    MODULES = [
        # 封装模块
        "testbot_aw.modules.wrapper.software.TestBotSoftware.doc.DocWrapperModule",

        # 原子模块
        "testbot_aw.modules.atom.software.TestBotSoftware.doc.DocAtomModule",
    ]

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict()

    def update_json_data(self):
        data = self.DocWrapperModule.get_apis()
        self.setting.apis = data
        self.setting.save()

    class Setting(SettingBase):
        atom_pkg = (None, None)
        wrapper_pkg = (None, None)

