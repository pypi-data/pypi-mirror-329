#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from abc import ABCMeta, abstractmethod


class Constraint(metaclass=ABCMeta):
    """
    资源选择器限制条件的基类
    """
    def __init__(self):
        self.description = None

    @abstractmethod
    def is_meet(self, resource, *args, **kwargs):
        pass


class ResourceNotMeetConstraint(Exception):
    def __init__(self, constraints):
        super().__init__("Resource Not Meet Constraints")
        self.description = ""
        for constraint in constraints:
            self.description += constraint.description + "\n"


class ConnectionConstraint(Constraint, metaclass=ABCMeta):
    """
    用户限制获取Remote Port的限制条件。
    """
    @abstractmethod
    def get_connection(self, resource, *args, **kwargs):
        pass
