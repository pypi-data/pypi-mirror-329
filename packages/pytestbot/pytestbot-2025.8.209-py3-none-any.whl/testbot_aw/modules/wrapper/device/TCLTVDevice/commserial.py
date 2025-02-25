#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TCLTVDevice设备封装接口模块类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import re
import time

from testbot.resource.module import TCLTVDeviceWrapperModuleBase


class CommSerialWrapperModule(TCLTVDeviceWrapperModuleBase):
    """
    TCLTV测试设备源封装接口指令串口模块类
    """

    def get_ip_addresses(self) -> list:
        """
        获取IP地址

        :return: IP地址
        :rtype: bytes
        """
        ips = []
        output = self.resource.CommSerialAtomModule.send_command(data="ifconfig")
        pat_ipv4 = re.compile(r'^\s*inet addr:(\S+)', flags=re.M)
        for ip in pat_ipv4.findall(output):
            if ip!="127.0.0.1":
                ips.append(ip)
        return ips

    def is_grpc_apk_installed(self) -> bool:
        """
        检查gRPC apk是否安装

        :return:
        """
        output = self.resource.CommSerialAtomModule.send_command(data="pm list package|grep com.tcl.fftestmonitor")
        if "package:com.tcl.fftestmonitor" in output:
            return True
        return False

    def install_grpc_apk(self):
        """
        安装grpc apk

        :return:
        """
        pass

    def is_grpc_service_up(self) -> bool:
        """
        检查gRPC服务启动状态

        :return:
        """
        result1 = self.resource.CommSerialAtomModule.send_command(data="ps -ef | grep 'ff'")
        result2 = self.resource.CommSerialAtomModule.send_command(data="dumpsys activity services | grep 'com.tcl.fftestmonitor'")
        if "com.tcl.fftestmonitor" in result1 and "com.tcl.fftestmonitor/.service.GrpcNettyService" in result2:
            time.sleep(10)
            return True
        return False

    def start_grpc_service(self):
        """
        启动gRPC服务

        :return:
        """
        self.resource.CommSerialAtomModule.send_command(data="am startservice -n com.tcl.fftestmonitor/.service.GrpcNettyService")
        time.sleep(2)
