#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TCLTVDevice设备原子接口模块类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import cv2
import time
import os.path

from testbot.resource.module import TCLTVDeviceAtomModuleBase


class CaptureCardAtomModule(TCLTVDeviceAtomModuleBase):
    """
    TCLTV测试设备源原子接口采集卡模块类
    """

    def read(self) -> tuple:
        """
        读取图像数据

        :return: 返回数据
        :rtype: tuple
        """
        port_obj = self.resource.get_port(type="VideoStreamSerialPort")
        ret, frame = port_obj._instance.read()
        return ret, frame

    def take_picture(self) -> str:
        """
        将当前图像保存到图片文件

        :return: 图片文件路径
        :rtype: str
        """
        logpath = self.logger.handlers[0].baseFilename
        self.logger.info(f"日志路径：{logpath}")
        pic_path = os.path.join(os.path.dirname(logpath), f"image-{int(round(time.time() * 1000))}.png")

        port_obj = self.resource.get_port(type="VideoStreamSerialPort")
        if port_obj.fps != port_obj._instance.get(cv2.CAP_PROP_FPS):
            for _ in range(int(port_obj.fps)):
                self.read()
                break
        ret, frame = self.read()
        cv2.imwrite(filename=pic_path, img=frame)
        return pic_path

    def record_video(self, duration: int = 10, size: tuple = (1920, 1080)) -> str:
        """
        录制视频

        :param duration: 录制时间，单位秒
        :type duration: int
        :param size: 分辨率
        :type size: tuple
        :return: 视频文件路径
        :rtype: str
        """
        logpath = self.logger.handlers[0].baseFilename
        self.logger.info(f"日志路径：{logpath}")
        video_path = os.path.join(os.path.dirname(logpath), f"video-{int(round(time.time() * 1000))}.wav")

        port_obj = self.resource.get_port(type="VideoStreamSerialPort")
        four_cc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        video_writer = cv2.VideoWriter(video_path, four_cc, port_obj.fps, size)
        start_ts = time.time()
        while time.time() - start_ts < duration:
            ret, frame = self.read()
            if ret:
                resize_frame = cv2.resize(frame, size, interpolation=cv2.INTER_LANCZOS4)
                video_writer.write(resize_frame)
        video_writer.release()
        return video_path
