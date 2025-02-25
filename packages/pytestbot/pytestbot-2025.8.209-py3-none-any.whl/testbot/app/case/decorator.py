#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import json
import re
import inspect
from functools import wraps
from enum import IntEnum


class StepResult(IntEnum):
    """
    表示节点的状态
    """
    INFO = 1
    PASS = 2
    FAIL = 4
    EXCEPTION = 8
    WARNING = 16
    ERROR = 32


class TestDataFileNotFound(Exception):
    pass


class MethodNotFoundError(Exception):
    pass


def case(test_type: str,testcase_id: str, testcase_name: str,  priority: int=0, feature_name: str=None, pre_tests: str=None, skip_if_high_priority_failed: bool=False):
    """
    测试用例装饰器，接收用例参数

    :param priority: 优先级
    :type priority:
    :param test_type: 测试类型
    :type test_type:
    :param feature_name: 特性名称
    :type feature_name:
    :param testcase_id: 测试用例ID
    :type testcase_id:
    :param testcase_name: 测试用例名称
    :type testcase_name:
    :param pre_tests:
    :type pre_tests:
    :param skip_if_high_priority_failed: 是否跳过执行失败的高优先级用例
    :type skip_if_high_priority_failed: bool
    :return:
    :rtype:
    """
    def decorator(cls):
        setattr(cls, "priority", priority)  # 测试用例的优先级
        setattr(cls, "test_type", test_type)  # 测试用例的类型
        setattr(cls, "feature_name", feature_name)  # 测试用例测试的功能
        setattr(cls, "testcase_id", testcase_id)  # 测试用例对应的测试用例ID
        setattr(cls, "testcase_name", testcase_name)  # 测试用例对应的测试用例名称
        setattr(cls, "pre_tests", pre_tests if pre_tests else list())
        setattr(cls, "skip_if_high_priority_failed", skip_if_high_priority_failed)
        return cls
    return decorator


def _replace_value(obj, test_case):
    if not isinstance(obj, dict):
        return
    for key, value in obj.items():
        if isinstance(value, str):
            # 替换字符串
            obj[key] = value % test_case.test_data_var
            # 查找方法并执行
            res = re.findall(r"<func:(.+?)>", obj[key])
            if any(res):
                if hasattr(test_case, res[0]):
                    obj[key] = getattr(test_case, res[0])()
                else:
                    raise MethodNotFoundError(f"method: {res[0]} not found")

        elif isinstance(value, dict):
            _replace_value(value, test_case)
        elif isinstance(value, list):
            for item in value:
                _replace_value(item, test_case)
        else:
            continue


def data_provider(filename=None, stop_on_error=False):
    """
    The data provider for test method in test case
    :param filename: the test data file, default case name is script name + ".json"
    :param stop_on_error: If true, the case will stop if 1 data iteration failed.
    :return:
    """
    def outer(func):
        @wraps(func)
        def wrapper(*args):
            test_case = locals()["args"][0]
            case_file = inspect.getfile(test_case.__class__)
            if filename:
                case_file = filename
            test_data_file = case_file + ".json"
            if not os.path.exists(test_data_file):
                raise TestDataFileNotFound(f"Cannot found test data for case {test_case.__class__.__name__}")
            with open(test_data_file) as file:
                test_data = json.load(file)
            iteration = 1
            for data in test_data["data"]:
                header = data.get("header", f"Iteration {iteration}")
                try:
                    iteration += 1
                    test_case.reporter.add_step_group(header)
                    _replace_value(data, test_case)
                    func(*args, data)
                except Exception as ex:
                    if not stop_on_error:
                        test_case.reporter.add(StepResult.EXCEPTION, f"Exception on {header}")
                    else:
                        raise ex
                finally:
                    test_case.reporter.end_step_group()
        return wrapper
    return outer