#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TCLTVDevice设备原子接口模块类列表
"""

__copyright__ = "Copyright (c) TCL DIGITAL TECHNOLOGY (SHENZHEN) CO., LTD."
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@tcl.com"

from testbot.resource.module import TCLTVDeviceAtomModuleBase


class DemoAtomModule(TCLTVDeviceAtomModuleBase):
    """
    TCLTV测试设备源原子接口DEMO模块类
    """

    def foo(self):
        """
        无参数、无返回值

        :return:
        :rtype:
        """
        pass

    def foo2(self, param1: int, param2: str, param3: bool, param4: bytes, param5: float):
        """
        有参数、无默认值、无返回值

        :param param1:
        :type param1:
        :param param2:
        :type param2:
        :param param3:
        :type param3:
        :param param4:
        :type param4:
        :param param5:
        :type param5:
        :return:
        :rtype:
        """
        pass

    def foo3(self, param1: int = 0, param2: str = "Hello World", param3: bool = False, param4: bytes = b"", param5: float = 1.2):
        """
        有参数、有默认值、无返回值

        :param param1:
        :type param1:
        :param param2:
        :type param2:
        :param param3:
        :type param3:
        :param param4:
        :type param4:
        :param param5:
        :type param5:
        :return:
        :rtype:
        """
        pass

    def foo4(self, param1: int = 0, param2: str = "Hello World", param3: bool = False, param4: bytes = b"Hello World", param5: float = 1.2) -> str:
        """
        有参数、有默认值、有返回值

        :param param1:
        :type param1:
        :param param2:
        :type param2:
        :param param3:
        :type param3:
        :param param4:
        :type param4:
        :param param5:
        :type param5:
        :return:
        :rtype:
        """
        return ""
