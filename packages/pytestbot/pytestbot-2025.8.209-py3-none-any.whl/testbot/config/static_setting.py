#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.config import CONFIG_PATH
from testbot.config.setting import static_setting, SettingBase


@static_setting.setting("ResourceSetting")
class ResourceSetting(SettingBase):
    """
    资源设置类
    """
    file_name = "ResourceSetting.json"
    resource_path = CONFIG_PATH
    auto_connect = False

