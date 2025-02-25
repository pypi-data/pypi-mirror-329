#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TCLTVDevice设备原子接口模块类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import time
from testbot.resource.module import TCLTVDeviceAtomModuleBase
from testbot_aw.modules.atom.device.TCLTVDevice.keycode import KEYCODES


class InfraredSerialAtomModule(TCLTVDeviceAtomModuleBase):
    """
    TCLTV测试设备源原子接口红外遥控串口模块类
    """

    def write_hex(self, data: str):
        """
        写入hex数据，如 `A1 B2 C3`

        :param data: 数据
        :type data: str
        :return:
        :rtype:
        """
        port_obj = self.resource.get_port(type="InfraredSerialPort")
        self.logger.info(f"发送命令：{data}")
        port_obj._instance.write(bytes.fromhex(data))
        port_obj._instance.flush()

    def read_all(self) -> bytes:
        """
        从串口读取所有数据

        :return: 返回数据
        :rtype: bytes
        """
        port_obj = self.resource.get_port(type="InfraredSerialPort")
        data = port_obj._instance.read_all()
        self.logger.info(f"命令返回：{data}")
        return data

    def send_hex_command(self, data: str) -> bytes:
        """
        发送hex命令

        :param data: hex命令
        :type data: str
        :return: 返回值
        :rtype: bytes
        """
        self.write_hex(data=data)
        time.sleep(0.5)
        return self.read_all()

    def send_key(self, key: str = None, code: str = None, keycodes: dict = KEYCODES.KEY_CODE_CN.value):
        """
        发送键码，若指定键key，则通过KEYCODES键码表查询其码code，

        :param key: 键
        :type key: str
        :param code: 键码
        :type code: str
        :param keycodes: 键码表
        :type keycodes: dict
        :return:
        :rtype:
        """
        if key:
            if key.upper() in keycodes.keys():
                code = keycodes[key.upper()]
                self.write_hex(data=code)
            else:
                if code:
                    self.write_hex(data=code)
                else:
                    raise Exception(f"指定的参数键{key}在键码表{keycodes}不存在！！！且参数码code未指定！")
        elif code:
            self.write_hex(data=code)
