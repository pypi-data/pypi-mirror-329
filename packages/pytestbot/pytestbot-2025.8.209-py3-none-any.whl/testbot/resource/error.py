#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


class ResourceNotMeetConstraintError(Exception):
    def __init__(self, constraint):
        super().__init__(constraint.get_description())


class ResourceLoadError(Exception):
    def __init__(self, filename, inner_ex):
        super().__init__("资源文件%s无法读取" % filename)
        self.inner_ex = inner_ex


class ResourceNotRelease(Exception):
    def __init__(self, filename, owner):
        super().__init__("资源文件被占用%s，使用者为%s" % (filename, owner))
