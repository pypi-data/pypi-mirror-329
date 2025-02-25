#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TCLTVDevice设备原子接口模块类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.resource.module import TCLTVDeviceAtomModuleBase, set_as_grpc_api
from testbot.resource.protoc import tv_picture_pb2_grpc, tv_audio_pb2_grpc, basic_type_pb2
from testbot.resource.protoc.heart_beat_pb2_grpc import HeartBeatStub
from testbot.resource.protoc.basic_type_pb2 import Empty


class GRPCAtomModule(TCLTVDeviceAtomModuleBase):
    """
    TCLTV测试设备源原子接口gRPC模块类
    """

    def check_heart_beat(self) -> str:
        """
        gRPC心跳检测接口

        :return: 若gRPC服务正常则返回online，否则报错异常
        """
        port_obj = self.resource.get_port(type="GRPCPort")
        stub = HeartBeatStub(port_obj._instance)
        request = Empty()
        response = stub.checkHeartBeat(request)
        if response:
            return response.value
        else:
            self.logger.error("通讯异常")
            return ""

    @set_as_grpc_api(timeout=60, duration=3)
    def set_picture_mode(self, value: int) -> bool:
        """
        设置图效

        :param value:范围0-6，对应模式：0-标准，1-明亮，2-柔和，3-FILMMAKER MODE，4-电影，5-办公，6-智能
        :type value:int类型
        :return: 设置是否成功
        :rtype: bool
        """
        port_obj = self.resource.get_port(type="GRPCPort")
        stub = tv_picture_pb2_grpc.SettingsPictureStub(port_obj._instance)
        request = basic_type_pb2.IntType(value=value)
        response = stub.setPictureMode(request)
        if response:
            return response.value
        else:
            return False

    @set_as_grpc_api(timeout=60, duration=3)
    def get_picture_mode(self):
        """
        获取图效

        :return: 图效值，范围0-6，对应模式：0-标准，1-明亮，2-柔和，3-FILMMAKER MODE，4-电影，5-办公，6-智能
        :rtype: int类型
        """
        port_obj = self.resource.get_port(type="GRPCPort")
        stub = tv_picture_pb2_grpc.SettingsPictureStub(port_obj._instance)
        request = basic_type_pb2.Empty()
        response = stub.getPictureMode(request)
        if response:
            return response.value
        else:
            return -1

    @set_as_grpc_api(timeout=60, duration=3)
    def set_audio_option_by_grpc(self, value: int):
        """
        设置音效

        :param value: 范围 0-7，对应模式：0：标准 1：电影 2：音乐 3：新闻 4：游戏 5：体育 6：用户自定义 7：智能
        :type value: int类型
        :return: 无参数返回值
        :rtype: None
        """
        port_obj = self.resource.get_port(type="GRPCPort")
        stub = tv_audio_pb2_grpc.SettingsAudioStub(port_obj._instance)
        request = basic_type_pb2.IntType(value=value)
        stub.setAudioOption(request)

    @set_as_grpc_api(timeout=60, duration=3)
    def get_audio_option(self) -> int:
        """
        获取音效

        :return: 音效值， 范围 0-7，对应模式：0：标准 1：电影 2：音乐 3：新闻 4：游戏 5：体育 6：用户自定义 7：智能,异常返回 -1
        :rtype: int类型
        """
        port_obj = self.resource.get_port(type="GRPCPort")
        stub = tv_audio_pb2_grpc.SettingsAudioStub(port_obj._instance)
        request = basic_type_pb2.Empty()
        response = stub.getAudioOption(request)
        if response:
            return response.value
        else:
            return -1
