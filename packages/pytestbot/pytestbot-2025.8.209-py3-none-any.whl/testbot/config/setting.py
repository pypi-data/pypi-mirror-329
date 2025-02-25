#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


import os
import json
from abc import ABCMeta
from functools import wraps

from testbot.config import CONFIG_PATH

_DEFAULT_PATH = CONFIG_PATH


class SettingError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class SettingBase(metaclass=ABCMeta):
    """
    配置基类
    """
    filename = None
    setting_path = _DEFAULT_PATH

    @classmethod
    def _get_full_path(cls):
        """
        获取配置文件全路径
        :return: 配置文件全路径
        :rtype: str
        """
        filename = cls.filename if cls.filename else cls.__name__ + ".json"
        return os.path.join(cls.setting_path, filename)

    @classmethod
    def save(cls):
        """
        保存配置文件

        :return: None
        :rtype: NoneType
        """
        if not os.path.exists(cls.setting_path):
            print(cls.setting_path)
            os.makedirs(cls.setting_path)
        with open(cls._get_full_path(), "w") as file:
            obj = dict()
            for key, value in cls.__dict__.items():
                if key.startswith("_") or key == "setting_path" or key == "filename":
                    continue
                obj[key] = value
            json.dump(obj, file, indent=4)

    @classmethod
    def load(cls):
        """
        加载配置文件

        :return: None
        :rtype: NoneType
        """
        if os.path.exists(cls._get_full_path()):
            with open(cls._get_full_path()) as file:
                obj = json.load(file)
            for key, value in obj.items():
                setattr(cls, key, value)
        else:
            cls.save()


def dynamic_setting(cls):
    """
    对SettingBase子类进行动态配置

    :param cls:
    :type cls:
    :return:
    :rtype:
    """
    @wraps(cls)
    def inner(*args, **kwargs):
        rv = cls(*args, **kwargs)
        for key, value in cls.__dict__.items():
            if hasattr(value, "__base__") and value.__base__.__name__ == "SettingBase":
                setattr(rv, "setting", value)
                if hasattr(rv, "setting_path"):
                    value.setting_path = rv.setting_path
                if hasattr(rv, "filename") and rv.filename is not None:
                    value.filename = rv.filename
                else:
                    if value.filename is None:
                        value.filename = f"{cls.__name__}_{value.__name__}.json"
                    else:
                        value.filename = f"{cls.__name__}_{value.filename}.json"
                setattr(rv, "filename", value.filename)
                value.load()
        return rv
    return inner


class TestSettingBase(SettingBase):
    """
    测试设置基类

    """

    def __init__(self, setting_path, filename):
        self.__class__.filename = filename
        self.__class__.setting_path = setting_path


class StaticSettingManager(object):
    """
    静态配置管理类
    """
    def __init__(self):
        self.settings = dict()
        self._setting_path = _DEFAULT_PATH

    def add_setting(self, setting_name: str, setting_class: object):
        """
        添加配置对象

        :param setting_name: 配置名称
        :type setting_name: str
        :param setting_class: 配置类
        :type setting_class: object
        :return:
        :rtype:
        """
        if hasattr(setting_class, "__base__"):
            if setting_class.__base__.__name__ != "SettingBase":
                raise SettingError("注册的配置必须是SettingBase的子类")
        else:
            raise SettingError("注册的配置必须是SettingBase的子类")
        self.settings[setting_name] = setting_class
        setting_class.setting_path = self._setting_path

    def setting(self, setting_name: str, *args: tuple, **kwargs: dict):
        """
        配置文件的注册装饰器

        :param setting_name: 配置名称
        :type setting_name: str
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        def wrapper(cls):
            self.add_setting(setting_name, cls)
            return cls
        return wrapper

    @property
    def setting_path(self) -> str:
        """
        设置路径

        :return: 设置路径
        :rtype: str
        """
        return self._setting_path

    @setting_path.setter
    def setting_path(self, value):
        self._setting_path = value
        for key, setting in self.settings.items():
            setting.setting_path = value

    def sync_path(self):
        """
        同步所有配置的路径
        """
        for key, setting in self.settings.items():
            setting.setting_path = self._setting_path

    def save_all(self):
        """
        保存所有配置
        """
        self.sync_path()
        for key, setting in self.settings.items():
            setting.save()

    def load_all(self):
        """
        读取所有配置
        """
        self.sync_path()
        for key, setting in self.settings.items():
            setting.load()


static_setting = StaticSettingManager()
