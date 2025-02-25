#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import cv2
import serial


class Singleton(type):
    _instances = dict()

    def __call__(cls, *args, **kwargs):
        # print(cls.__name__)
        # print(args, kwargs)
        name = kwargs.get("name", None)
        port = kwargs.get("port", None)
        index = kwargs.get("index", None)
        # print(index, type(index))
        filename = kwargs.get("filename", None)
        if cls not in cls._instances:
            if name or port or str(index) or filename:
                cls._instances[cls] = dict()
            else:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        if isinstance(cls._instances[cls], dict):
            if name:
                if name not in cls._instances[cls]:
                    cls._instances[cls][name] = super(Singleton, cls).__call__(*args, **kwargs)
                return cls._instances[cls][name]
            if port:
                if port not in cls._instances[cls]:
                    cls._instances[cls][port] = super(Singleton, cls).__call__(*args, **kwargs)
                return cls._instances[cls][port]
            if isinstance(index, int):
                if index not in cls._instances[cls]:
                    cls._instances[cls][index] = super(Singleton, cls).__call__(*args, **kwargs)
                # print(cls._instances[cls])
                return cls._instances[cls][index]
            if filename:
                if index not in cls._instances[cls]:
                    cls._instances[cls][filename] = super(Singleton, cls).__call__(*args, **kwargs)
                return cls._instances[cls][filename]
        else:
            return cls._instances[cls]


serial_metaclass = type(serial.Serial)


class CombinedMeta(serial_metaclass, Singleton):
    pass


class Serial(serial.Serial, metaclass=CombinedMeta):
    pass


class VideoCapture(cv2.VideoCapture, metaclass=CombinedMeta):
    pass


if __name__ == "__main__":
    from testbot.utilities.singleton import Serial
    s = Serial(port="COM6", baudrate=115200, timeout=1)
    print(s)
    s2 = Serial(port="COM6", baudrate=115200, timeout=1)
    print(s2)

    s3 = Serial(port="COM4", baudrate=115200)
    print(s3)
    s4 = Serial(port="COM4", baudrate=115200)
    print(s4)

    v = VideoCapture(index=0)
    print(v)

    v2 = VideoCapture(index=0)
    print(v2)

    v3 = VideoCapture(index=1)
    print(v3)

    v4 = VideoCapture(index=1)
    print(v4)
