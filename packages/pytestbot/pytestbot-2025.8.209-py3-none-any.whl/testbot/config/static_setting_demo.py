#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


import os
from pathlib import Path
from testbot.config.setting import static_setting, SettingBase


if __name__ == "__main__":
    # 基于配置基类SettingBase，创建一个配置子类，该配置子类使用装饰器static_setting装饰
    @static_setting.setting("ResourceSetting")
    class ResourceSetting(SettingBase):
        """
        资源设置类
        """
        filename = "ResourceSetting.json"

        resource_path = os.path.join(str(Path.home()), "TESTBOT", "configs")
        auto_connect = False


    # 从本地json文件ResourceSetting.json加载属性信息到类ResourceSetting，由于第一次没有该文件，会创建并使用类的默认属性值
    ResourceSetting.load()

    # 读取属性ResourceSetting.auto_connect
    print(f"ResourceSetting.auto_connect={ResourceSetting.auto_connect}")

    # 设置属性ResourceSetting.auto_connect
    ResourceSetting.auto_connect = True

    # 读取属性ResourceSetting.auto_connect
    print(f"ResourceSetting.auto_connect={ResourceSetting.auto_connect}")

    # 将当前的属性信息保存到本地文件ResourceSetting.json
    ResourceSetting.save()

    # 从本地json文件ResourceSetting.json加载属性信息到类ResourceSetting，由于第一次没有该文件，会创建并使用类的默认属性值
    ResourceSetting.load()

    # 读取属性ResourceSetting.auto_connect
    print(f"ResourceSetting.auto_connect={ResourceSetting.auto_connect}")