#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from functools import wraps

from testbot.resource.resource import Resource, ResourceError, _resource_port_mapping, _resource_device_mapping


def add_module(module_class):
    print("###### Entering add_module #####")
    def decorator(cls):
        print("###### Entering decorator #####")
        @wraps(cls)
        def innner(*args: tuple, **kwargs: dict):
            print("###### Entering innner #####")
            cls_inst = cls(*args, **kwargs)
            mod_inst = module_class(device=cls_inst)
            setattr(cls_inst, module_class.__name__, mod_inst)
            print("###### Exiting innner #####")
            return cls_inst
        print("###### Exiting decorator #####")
        return innner
    print("###### Exiting add_module #####")
    return decorator


class Device(Resource):
    """
    代表所有测试设备类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)
        self.logger.info("Initialize Device...")
        self.ports = dict()
        self._instance = None

    def add_port(self, name: str, *args: tuple, **kwargs: dict):
        """
        添加端口

        :param name: 端口名称
        :type name: str
        :param args: 元祖参数
        :type args: tuple
        :param kwargs: 键值对参数
        :type kwargs: dict
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.add_port...")
        if name in self.ports:
            raise ResourceError(f"Port Name {name} already exists")
        self.ports[f"{name}"] = Port(parent_device=self, name=name, *args, **kwargs)
        self.logger.info(f"Exiting {self.__class__.__name__}.add_port...")

    def get_port_count(self, **kwargs: dict):
        """
        获取端口数量

        :param kwargs: 键值对参数
        :type kwargs: dict
        :return: 端口数量
        :rtype: int
        """
        return len(self.ports)

    def to_dict(self):
        ret = dict()
        for key, value in self.__dict__.items():
            if key in ["__instance", "logger"]:
                continue
            if key == "ports":
                ret[key] = dict()
                for port_name, port in value.items():
                    ret[key][port_name] = port.to_dict()
            else:
                ret[key] = value
        return ret

    def get_comm_instance(self, new=False):
        if self.type not in _resource_device_mapping:
            raise ResourceError(f"type {self.type} is not registered")
        if not new and self._instance:
            return self._instance
        else:
            self._instance = _resource_device_mapping[self.type](self)
        return self._instance

    @staticmethod
    def from_dict(dict_obj):
        ret = Device()
        for key, value in dict_obj.items():
            if key == "ports":
                ports = dict()
                for port_name, port in value.items():
                    ports[port_name] = Port.from_dict(port, ret)
                setattr(ret, "ports", ports)
            else:
                setattr(ret, key, value)
        return ret


class Port(Resource):
    """
    代表所有端口类
    """

    def __init__(self, parent_device: Device = None, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)
        self.parent = parent_device
        self.remote_ports = list()
        self._instance = None

    def get_comm_instance(self, new=False):
        if self.type not in _resource_port_mapping:
            raise ResourceError(f"type {self.type} is not registered")
        if not new and self._instance:
            return self._instance
        else:
            self._instance = _resource_port_mapping[self.type](self)
        return self._instance

    def to_dict(self):
        ret = dict()
        for key, value in self.__dict__.items():
            if key in ["__instance", "logger"]:
                continue
            if key == "parent":
                ret[key] = value.name
            elif key == "remote_ports":
                ret[key] = list()
                for remote_port in value:
                    #使用device的名称和port的名称来表示远端的端口
                    #在反序列化的时候可以方便地找到相应的对象实例
                    ret[key].append(
                        {
                            "device": remote_port.parent.name,
                            "port": remote_port.name
                        }
                    )
            else:
                ret[key] = value
        return ret

    @staticmethod
    def from_dict(dict_obj, parent):
        ret = Port(parent)
        for key, value in dict_obj.items():
            if key == "remote_ports" or key == "parent":
                continue
            setattr(ret, key, value)
        return ret


class PCDevice(Device):
    """
    PC主机设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict()


class RPIDevice(Device):
    """
    树莓派设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict()


class AndroidDevice(Device):
    """
    安卓设备类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)


class TVDevice(AndroidDevice):
    """
    电视设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict()


class PhoneDevice(AndroidDevice):
    """
    手机设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)


class TabletDevice(AndroidDevice):
    """
    平板设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict()


class MonitorDevice(AndroidDevice):
    """
    商显设备类
    """
    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)

    def to_dict(self) -> dict:
        return dict()
