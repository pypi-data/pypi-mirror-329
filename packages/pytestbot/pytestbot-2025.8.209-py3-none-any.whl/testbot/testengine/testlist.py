#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


import os
import json
from pathlib import Path

from testbot.config.setting import SettingBase, dynamic_setting
from testbot.app.base import TestType


class TestListError(Exception):
    """
    用来描述测试列表的一系列错误异常
    """
    def __init__(self, message, ex=None):
        super().__init__("测试列表异常:" + message)
        self.parent = ex


@dynamic_setting
class TestList(object):
    """
    测试列表类
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.setting_file_path = None
        self.test_list_name = ""
        self.description = ""
        self.iterations = 1
        self.test_cases = list()
        self.sub_list = list()
        self.load()
        self.setting_path = os.path.dirname(self.setting_file_path)
        self.filename = os.path.basename(self.setting_file_path)

    def load(self):
        """
        读取测试列表
        """
        if not os.path.exists(self.filepath):
            raise TestListError("%s 无法找到" % self.filepath)
        try:
            testlist_file = open(self.filepath)
            testlist_obj = json.load(testlist_file)
            self.test_list_name = testlist_obj['name']
            self.description = testlist_obj['description']
            self.iterations = testlist_obj['iterations']
            self.setting_file_path = testlist_obj['setting_path']
            if not self.setting_file_path:
                setting_filepath = os.path.join(os.path.dirname(self.filepath), Path(self.filepath).stem + "Setting.json")
                if os.path.exists(setting_filepath):
                    self.setting_file_path = setting_filepath

            for testcase in testlist_obj['cases']:
                self.test_cases.append(testcase)
            for sublist in testlist_obj['sublist']:
                fullpath = os.path.join(os.path.dirname(self.filepath), sublist)
                temp_list = TestList(fullpath)
                try:
                    temp_list.load()
                    self.sub_list.append(temp_list)
                except:
                    pass

        except Exception as ex:
            raise TestListError("打开文件%s错误" % self.filepath, ex)

    def save(self):
        """
        将测试列表保存成json格式的文件
        """
        json_obj = dict()
        json_obj['name'] = self.test_list_name
        json_obj['description'] = self.description
        json_obj['iterations'] = self.iterations
        json_obj['setting_path'] = self.setting_file_path
        json_obj['cases'] = list()
        for testcase in self.test_cases:
            json_obj['cases'].append(testcase)
        json_obj['sublist'] = list()
        for sublist in self.sub_list:
            try:
                sublist.save()
                json_obj['sublist'].append(os.path.basename(sublist.filepath))
            except:
                pass
        try:
            testlist_file = open(self.filepath, mode="w")
            json.dump(json_obj, testlist_file, indent=4)
        except Exception as ex:
            raise TestListError("无法保存测试列表%s" % self.filepath, ex)

    class TestListSetting(SettingBase):
        random_seed = 0
        case_setting_path = ""
        skip_if_high_priority_failed = True
        follow_priority = True
        run_type = TestType.COMMON_TEST
        priority_to_run = list()


if __name__ == "__main__":
    tl = TestList("demo_list.testlist")
    # tl2 = TestList("demo_list2.testlist")
    # tl2.test_list_name = "Demo sub list"
    # tl2.description = "desc"
    # tl.test_list_name = "A Demo Test List"
    # tl.description = "Description"
    # tl.setting_file_path = "."
    # tl.sub_list.append(tl2)
    # tl.test_cases.append("case1")
    # tl.test_cases.append("case2")
    # tl.save()
    tl.load()
    print(tl)
