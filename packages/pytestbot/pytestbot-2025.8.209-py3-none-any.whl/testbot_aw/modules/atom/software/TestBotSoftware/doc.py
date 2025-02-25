#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PCDevice设备原子接口模块类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import types
import pkgutil
import inspect
import importlib
import traceback
import docstring_parser
from typing import Callable

from testbot.resource.module import ModuleBase
from testbot.resource.module import TestBotSoftwareAtomModuleBase


class DocAtomModule(TestBotSoftwareAtomModuleBase):
    """
    TestBot测试软件源原子接口文档模块类
    """

    def import_modules_from_pkg(self, path: str, name: str) -> list:
        """
        导入指定包路径下的所有模块

        :param path: 包绝对路径
        :type path: str
        :param name: 包路径
        :type name: str
        :return: 模块列表
        :rtype: list
        """
        modules = []
        for _finder, _name, _ispkg in pkgutil.walk_packages(path=path, onerror=lambda x: None):
            modules.append(importlib.import_module(f"{name}.{_name}"))
        return modules

    def get_module_doc(self, mod: types.ModuleType) -> str:
        """
        获取模块文档

        :param mod: 模块
        :type mod: types.ModuleType
        :return: 模块文档
        :rtype: str
        """
        mod_obj = inspect.getmodule(mod)
        return mod_obj.__doc__

    def get_modulebase_sub_classes(self, mod: types.ModuleType) -> list:
        """
        获取python模块的所有ModuleBase子类

        :param mod: 模块
        :type mod: types.ModuleType
        :return: ModuleBase子类
        :rtype: list
        """
        classes = []
        for name, clazz in inspect.getmembers(mod):
            if inspect.isclass(clazz) and issubclass(clazz, ModuleBase) and not name.endswith('ModuleBase'):
                classes.append(clazz)
        return classes

    def get_class_doc(self, clazz: object) -> str:
        """
        获取类对象文档

        :param clazz: 类
        :type clazz: object
        :return: 类文档
        :rtype: str
        """
        return clazz.__doc__

    def get_class_funcs(self, clazz: object) -> dict:
        """
        获取类对象的方法对象字典

        :param clazz: 类
        :type clazz: object
        :return: 类对象的方法对象字典
        :rtype: dict
        """
        funcs = dict()
        for name, func in inspect.getmembers(clazz, predicate=inspect.isfunction):
            if callable(func) and not name.startswith('__') and not name.startswith('__'):
                funcs[name] = func
        return funcs

    def get_func_doc(self, func: Callable) -> str:
        """
        获取方法对象的文档

        :param func: 方法
        :type func: Callable
        :return: 方法文档
        :rtype: str
        """
        import docstring_parser
        return docstring_parser.parse(func.__doc__).description

    def get_obj_pkg_path(self, obj: object) -> str:
        klass = obj.__class__
        module = klass.__module__
        if module == 'builtins':
            return klass.__qualname__  # avoid outputs like 'builtins.str'
        return module + '.' + klass.__qualname__

    def get_func_param_info(self, func: Callable) -> list:
        """
        获取方法对象的参数信息，如参数名称、参数类型、参数默认值

        :param func: 方法
        :type func: Callable
        :return: 参数名称、参数类型、参数默认值
        :rtype: list(str, str, object)
        """
        params = list()
        # self.logger.info(f"{func.__name__}-{func.__qualname__}")
        sign = inspect.signature(func)
        for name, param in sign.parameters.items():
            if name != "self":
                try:
                    self.logger.info(f"func={func.__qualname__}, param default value={param.default}, param default type={type(param.default)}")
                    param_default = ""
                    if param.default == inspect._empty:
                        param_default = ""
                    elif isinstance(param.default, bytes):
                        param_default = param.default.decode()
                    else:
                        param_default = param.default
                    params.append((name, param.annotation.__name__, param_default))
                except Exception as e:
                    try:
                        param_default = ""
                        if param.default == inspect._empty:
                            param_default = ""
                        elif isinstance(param.default, bytes):
                            param_default = param.default.decode()
                        else:
                            param_default = param.default
                        params.append((name, self.get_obj_pkg_path(obj=param.annotation), param_default))
                    except Exception as e:
                        traceinfo = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                        self.logger.error(traceinfo)
        return params

    def get_func_returned_type(self, func: Callable) -> str:
        """
        获取方法对象的返回值类型

        :param func: 方法
        :type func: Callable
        :return: 返回值类型
        :rtype: str
        """
        sign = inspect.signature(func)
        return None if sign.return_annotation==inspect._empty else getattr(sign.return_annotation, '__name__', None)

    def get_func_param_info_from_func_doc(self, func: Callable, arg_name: str) -> tuple:
        """
        从类文档里提取方法参数信息，包括参数描述、参数类型、参数默认值

        :param func: 方法
        :type func: Callable
        :param arg_name: 参数名称
        :type arg_name: str
        :return: 参数描述、参数类型、参数默认值
        :rtype: tuple
        """
        desc, type_name, default = None, None, None
        doc = docstring_parser.parse(func.__doc__)
        # 获取类对象方法信息的文档里的参数名称、参数描述、参数类型、参数默认值
        for param in doc.params:
            print(param.arg_name, param.description, param.type_name, dir(param))
            if param.arg_name==arg_name:
                desc, type_name, default = param.description, param.type_name, param.default
                break
        return (desc, type_name, default)

    def get_func_return_info_from_func_doc(self, func: Callable) -> tuple:
        """
        从类文档里提取方法返回值信息，如返回值类型、返回值描述

        :param func: 方法
        :type func: Callable
        :return: 返回值类型、返回值描述
        :rtype: tuple
        """
        doc = docstring_parser.parse(func.__doc__)
        # 获取类对象方法信息的文档里的返回值类型、描述
        return (doc.returns.type_name if doc.returns else None, doc.returns.description if doc.returns else None)
        
    def get_subclasses(self, clazz) -> list:
        """
        获取类的子孙类

        :param clazz:
        :type clazz:
        :return:
        :rtype:
        """
        all_subclasses = []
        for subclass in clazz.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(self.get_subclasses(subclass))
        return all_subclasses

