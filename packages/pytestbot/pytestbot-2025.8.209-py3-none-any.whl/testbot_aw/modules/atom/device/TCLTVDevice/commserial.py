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


class CommSerialAtomModule(TCLTVDeviceAtomModuleBase):
    """
    TCLTV测试设备源原子接口指令串口模块类
    """

    def write(self, data: str):
        """
        写入字符串数据

        :param data: 数据
        :type data: str
        :return:
        :rtype:
        """
        port_obj = self.resource.get_port(type="CommSerialPort")
        if not data.endswith("\n"):
            data = f"{data}\n"
        data = data.encode("UTF-8")
        self.logger.info(f"写入命令：{data}")
        port_obj._instance.write(data)
        port_obj._instance.flush()

    def write_hex(self, data: str):
        """
        写入hex数据，如 `A1 B2 C3`

        :param data: 数据
        :type data: str
        :return:
        :rtype:
        """
        port_obj = self.resource.get_port(type="CommSerialPort")
        port_obj._instance.write(bytes.fromhex(data))
        port_obj._instance.flush()

    def interrupt(self):
        """
        写入Ctrl+C，强制退出在执行的命令

        :return:
        :rtype:
        """
        port_obj = self.resource.get_port(type="CommSerialPort")
        port_obj._instance.write(bytes.fromhex("03"))

    def read(self, size: int = 1024) -> bytes:
        """
        从串口读取指定字节的数据

        :param size: 字节数
        :type size: int
        :return: 返回数据
        :rtype: bytes
        """
        port_obj = self.resource.get_port(type="CommSerialPort")
        data = port_obj._instance.read(size)
        self.logger.info(f"命令返回：{data}")
        return data

    def readline(self) -> bytes:
        """
        从串口读取一行数据

        :return: 返回数据
        :rtype: bytes
        """
        port_obj = self.resource.get_port(type="CommSerialPort")
        data = port_obj._instance.readline()
        self.logger.info(f"命令返回：{data}")
        return data

    def readlines(self) -> bytes:
        """
        从串口读取多行数据

        :return: 返回数据
        :rtype: bytes
        """
        port_obj = self.resource.get_port(type="CommSerialPort")
        data = port_obj._instance.readlines()
        self.logger.info(f"命令返回：{data}")
        return data

    def read_all(self) -> bytes:
        """
        从串口读取所有数据

        :return: 返回数据
        :rtype: bytes
        """
        port_obj = self.resource.get_port(type="CommSerialPort")
        data = port_obj._instance.read_all()
        self.logger.info(f"命令返回：{data}")
        return data

    def search_one(self, keywords: list, ignore_case: bool = False, timeout: int = 5) -> bool:
        """
        从串口读取的数据中搜索关键字，只要发现任意一个关键字，即可返回True，否则超时后返回False

        :param keywords: 关键字列表
        :type keywords: list[str]
        :param ignore_case: 是否忽略关键字大小写
        :type ignore_case: bool
        :param timeout: 超时时间，单位秒
        :type timeout: int
        :return: 是否搜索到关键字
        :rtype: bool
        """
        found = False
        start_ts = time.time()
        while time.time() - start_ts < timeout:
            data = self.readline().decode("UTF-8")
            if ignore_case:
                for keyword in keywords:
                    if data != "" and keyword.upper() in data.upper():
                        found = True
                        break
            else:
                for keyword in keywords:
                    if data!="" and keyword in data:
                        found = True
                        break
        return found

    def search_all(self, keywords: list, ignore_case: bool = False, timeout: int = 20) -> bool:
        """
        从串口读取的数据中搜索关键字，发现所有关键字，返回True，否则超时后返回False

        :param keywords: 关键字列表
        :type keywords: list[str]
        :param ignore_case: 是否忽略关键字大小写
        :type ignore_case: bool
        :param timeout: 超时时间，单位秒
        :type timeout: int
        :return: 是否搜索到关键字
        :rtype: bool
        """
        found = dict()
        for k in keywords:
            found[k] = False
        start_ts = time.time()
        while time.time() - start_ts < timeout:
            data = self.readline().decode("UTF-8")
            if ignore_case:
                for keyword in keywords:
                    if data != "" and keyword.upper() in data.upper():
                        found[keyword] = True
            else:
                for keyword in keywords:
                    if data!="" and keyword in data:
                        found[keyword] = True
        return all([v for k,v in found.items()])

    def send_command(self, data: str) -> str:
        """
        发送命令

        :param data: 命令
        :type data: str
        :return: 返回值
        :rtype: bytes
        """
        self.write(data=data)
        time.sleep(0.5)
        res = self.read_all().decode("UTF-8").replace(data, "").replace("console:/ #", "").replace("console:/ $", "").strip()
        self.logger.info(f"命令{data}返回结果：{res}")
        return res

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
