#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模块基类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import functools
import time
from inspect import ismethod
from abc import ABCMeta

from testbot.result.logger import logger_manager
from testbot.config import MODULE_LOGS_PATH


def set_as_grpc_api(*args, **kwargs):
    """
    设置接口方法为gRPC接口，在调用被装饰的gRPC接口之前，检查gRPC连接保活状态，若在默认60以内gRPC包或状态仍然为False，则直接调用gRPC接口
    """

    timeout: int = kwargs.get("timeout", 60)
    duration: int = kwargs.get("duration", 3)
    def decorator(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            self.logger.info(f"在调用方法{self.__class__.__name__}.{func.__name__}之前，做gRPC保活状态检查")
            for name, port in self.resource.ports.items():
                self.logger.info(f"name, port={name}, {port}")
                if port.type == "GRPCPort":
                    for _port in port.remote_ports:
                        if _port.type == "GRPCPort":
                            start_ts = time.time()
                            while time.time() - start_ts <= timeout:
                                if not _port._alive:
                                    self.logger.info(f"gRPC保活状态为False，等待{duration}秒后重新检查")
                                    time.sleep(duration)
                                else:
                                    self.logger.info(f"gRPC保活状态为True，可以放心调用gRPC接口")
                                    break
            return func(self, *args, **kwargs)
        return wrap
    return decorator


class ModuleBase(metaclass=ABCMeta):
    """
    模块基类
    """

    def __init__(self, resource, *args: tuple, **kwargs: dict):
        self.resource = resource
        self.logger = kwargs.get("logger", self.resource.logger if self.resource and getattr(self.resource, "logger", None) else logger_manager.register(logger_name="Module", filename=os.path.join(MODULE_LOGS_PATH, "Module.log"), for_test=True))

    def __getattribute__(self, item):
        attribute = super(ModuleBase, self).__getattribute__(item)
        if ismethod(attribute):
            # print(f"在调用方法{self.__class__.__name__}.{item}之前，做gRPC保活状态检查")
            pass
        return attribute


class DeviceAtomModuleBase(ModuleBase):
    """
    测试设备资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(DeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class DeviceWrapperModuleBase(DeviceAtomModuleBase):
    """
    测试设备资源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(DeviceWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class PCDeviceAtomModuleBase(DeviceAtomModuleBase):
    """
    PC测试设备源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(PCDeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class PCDeviceWrapperModuleBase(PCDeviceAtomModuleBase):
    """
    PC测试设备源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(PCDeviceWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class AndroidDeviceAtomModuleBase(DeviceAtomModuleBase):
    """
    Android测试设备源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(AndroidDeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class AndroidDeviceWrapperModuleBase(AndroidDeviceAtomModuleBase):
    """
    Android测试设备源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(AndroidDeviceWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class TCLTVDeviceAtomModuleBase(AndroidDeviceAtomModuleBase):
    """
    TCLTV测试设备源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TCLTVDeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class TCLTVDeviceWrapperModuleBase(TCLTVDeviceAtomModuleBase):
    """
    TCLTV测试设备源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TCLTVDeviceWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class SoftwareAtomModuleBase(ModuleBase):
    """
    测试软件资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(SoftwareAtomModuleBase, self).__init__(resource, *args, **kwargs)


class SoftwareWrapperModuleBase(SoftwareAtomModuleBase):
    """
    测试软件资源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(SoftwareWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class TestBotSoftwareAtomModuleBase(SoftwareAtomModuleBase):
    """
    TATF测试软件资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TestBotSoftwareAtomModuleBase, self).__init__(resource, *args, **kwargs)


class TestBotSoftwareWrapperModuleBase(TestBotSoftwareAtomModuleBase):
    """
    TATF测试软件资源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TestBotSoftwareWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class ServiceAtomModuleBase(ModuleBase):
    """
    测试服务资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(ServiceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class ServiceWrapperModuleBase(ServiceAtomModuleBase):
    """
    测试服务资源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(ServiceWrapperModuleBase, self).__init__(resource, *args, **kwargs)
