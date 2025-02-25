#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


import os
import json
from enum import Enum
from threading import Thread
from importlib import import_module
from abc import ABCMeta, abstractmethod

from testbot.result.testreporter import CaseStepEntry
from testbot.config import CONFIG_PATH, MODULE_LOGS_PATH
from testbot.result.logger import logger_manager
from testbot.config.setting import static_setting, SettingBase


class PluginType(Enum):
    PRE = 1
    PARALLEL = 2
    POST =3


class PluginBase(metaclass=ABCMeta):
    """
    插件模块的基类
    """
    plugin_type = None
    priority = 99

    def __init__(self, step: CaseStepEntry, pool, **kwargs):
        self.step = step
        self.logger = kwargs.get("logger", logger_manager.register(logger_name="Plugin", filename=os.path.join(MODULE_LOGS_PATH,"Plugin.log"), for_test=True))
        self.pool = pool
        self.thread = None

    @abstractmethod
    def action(self):
        """
        实现该方法来实现插件的逻辑功能
        """
        pass

    def do(self):
        if self.plugin_type == PluginType.PARALLEL:
            self.thread = Thread(target=self.action)
            self.thread.start()
        else:
            self.action()

    @abstractmethod
    def stop(self):
        """
        实现该方法来实现模块逻辑功能的终止方法
        """
        pass


@static_setting.setting("PluginModule")
class PluginSetting(SettingBase):

    plugin_list_file = os.path.join(CONFIG_PATH, "pluginlist.json")
    plugin_setting_path = CONFIG_PATH


class PluginManager(object):
    """
    配置模块的管理
    """
    def __init__(self, **kwargs):
        self.plugins = dict()
        self.logger = kwargs.get("logger", logger_manager.register(logger_name="PluginManager", filename=os.path.join(MODULE_LOGS_PATH, "PluginManager.log"), for_test=True))
        self.step = kwargs.get("step", None)
        self.pool = kwargs.get("pool", None)

    def load(self):
        """
        从插件列表装载所有插件类
        """
        if not os.path.exists(PluginSetting.plugin_list_file):
            # 如果没有找到插件配置文件，则不做任何操作
            return
        with open(PluginSetting.plugin_list_file) as file:
            obj = json.load(file)

        for item in obj['plugins']:
            try:
                plugin_name = item['name']
                plugin_package = item['package']
                filename = item.get("filename", None)
                setting_path = item.get('setting_path', PluginSetting.plugin_setting_path)
                m = import_module(plugin_package)
                for element, value in m.__dict__.items():
                    if element == plugin_name:
                        self.plugins[plugin_name] = {
                            "class": value,
                            "filename": filename,
                            "setting_path": setting_path
                        }
            except Exception:
                pass

    def add_plugin(self, plugin_class, filename=None, setting_path=None):
        """
        添加插件
        """
        obj = {
            "class": plugin_class,
            "filename": filename,
            "setting_path": setting_path
        }
        self.plugins[plugin_class.__name__] = obj

    def get_plugin_instances(self, plugin_type: PluginType, step: CaseStepEntry, pool):
        """
        获取插件的实例化列表
        """
        rv = list()
        for mkey, mvalue in self.plugins.items():
            self.logger.info(mvalue['class'].plugin_type)
            self.logger.info(plugin_type)
            if mvalue['class'].plugin_type.value == plugin_type.value:
                rv.append(mvalue['class'](step=step, pool=pool))
        return rv

    def save(self):
        """
        保存所有模块到模块配置列表
        """
        obj = dict()
        obj['plugins'] = list()
        for mkey, mvalue in self.plugins.items():
            obj['plugins'].append({
                "name": mkey,
                "package": mvalue["class"].__module__,
                "filename": mvalue['filename'],
                "setting_path": mvalue['setting_path']
            })
        file_dir = os.path.dirname(PluginSetting.plugin_list_file)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(PluginSetting.plugin_list_file, "w") as file:
            json.dump(obj, file, indent=4)

    def run_plugin(self, type):
        for plugin in self.get_plugin_instances(plugin_type=type, step=self.step, pool=self.pool):
            plugin.do()

    def stop_plugin(self):
        pass


if __name__ == "__main__":
    from testbot.plugin.plugin_demo import DemoPlugin
    pm = PluginManager()
    pm.load()
    pm.add_plugin(DemoPlugin)
    pm.save()
    pm.load()
    pre_plugin = pm.get_plugin_instances(plugin_type=PluginType.PRE, step=None, pool=None)
    print(pre_plugin)
