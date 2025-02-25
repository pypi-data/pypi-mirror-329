#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@TC_ID          : CNTC-94402
@Introduction   : 恢复出厂设置
@Description    :
@Precondition   :
1、电视TV下有频道
2、电视连接信号较强的wifi热点
@Steps:
1、进入设置菜单，修改图效、声效为任意值
2、进入VOD下播放视频
3、HDMI1信源播放视频时，执行恢复出厂设置操作
4、完成开机向导后，进入系统
5、检查launcher默认模板下的各个Tab页
6、检查HDMI高级标准默认值
@Expected       :
4.1、过完开机向导后，电视回到主页
4.2、所有频道节目，视频观看历史被清除
4.3、设置菜单里用户数据恢复默认值
--（仅保留WIFI账号密码）--
5、非TCL品牌，各个Tab页下不能出现TCL字样，海报中不能出现TCL的logo
（如：雷鸟，乐华，东芝等品牌不能出现TCL的字样，海报中不能出现TCL的logo）
6、HDMI高级标准默认为开（根据项目的PQ tree检查具体默认值：https://confluence.tclking.com/pages/viewpage.action?pageId=79309061）
注：982项目HDMI高级标准菜单默认为关，不区分品牌；963机型，TCL是关闭；雷鸟是打开
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import random

from testbot.app.case.base import TestCaseBase
from testbot.app.base import TestType
from testbot.app.case.decorator import case
from testbot.config import TESTBOT_ROOT
from testbot.config.setting import TestSettingBase


@case(priority=1, test_type=TestType.CHECK_TEST.name, testcase_id="TcDemo", testcase_name="TcDemo")
class TcDemo(TestCaseBase):

    def collect_resource(self, **kwargs):
        with self.step.start(headline="筛选设备") as step:
            with step.start(headline="筛选PC设备") as step2:
                self.pc = self.pool.collect_device(device_type="PCDevice", count=1)[0]
                if self.pc:
                    self.logger.info(f"self.pc={self.pc}, type={type(self.pc)}")
                    self.logger.info(f"self.pc funcs={dir(self.pc)}")
                    step2.passed(message="筛选PC设备成功")
                else:
                    step2.failed(message="筛选PC设备失败")
            with step.start(headline="筛选TV设备") as step2:
                self.tv = self.pool.collect_device(device_type="TVDevice", count=1)[0]
                if self.tv:
                    self.logger.info(f"self.tv={self.tv}, type={type(self.tv)}")
                    self.logger.info(f"self.tv funcs={dir(self.tv)}")
                    step2.passed(message="筛选TV设备成功")
                else:
                    step2.failed(message="筛选TV设备失败")
        pass

    def setup_class(self, **kwargs):
        with self.step.start(headline="检查是否安装和启动grpc服务APK", message="") as step:
            with step.start(headline="检查是否执行前置指令", message="") as step2:
                pass
            with step.start(headline="检查是否安装应用", message="") as step2:
                pass
            with step.start(headline="检查是否启动grpc服务", message="") as step2:
                pass

    def setup(self, **kwargs):
        with self.step.start(headline="TV进入主页") as step:
            pass
        with self.step.start(headline="", message="") as step:
            pass
        with self.step.start(headline="电视TV下有频道") as step:
            pass
        with self.step.start(headline="建立WIFI连接") as step:
            pass

    def test(self, **kwargs):
        with self.step.start(headline="进入设置菜单，修改图效、声效为任意值") as step:
            with step.start(headline="修改图效为任意值") as step2:
                pass
            with step.start(headline="修改声效为任意值") as step2:
                pass
        with self.step.start(headline="进入VOD下播放视频") as step:
            pass
        with self.step.start(headline="HDMI1信源播放视频时，执行恢复出厂设置操作") as step:
            pass
        with self.step.start(headline="完成开机向导后，进入系统") as step:
            with step.start(headline="过完开机向导后，电视回到主页") as step2:
                pass
            with step.start(headline="执行安装前置指令") as step2:
                pass
            with step.start(headline="安装应用") as step2:
                pass
            with step.start(headline="检查是否启动grpc服务", message="") as step2:
                pass
            with step.start(headline="重新初始化grpc", message="") as step2:
                pass
            with self.step.start(headline="建立WIFI连接") as step2:
                pass
            with step.start(headline="检查设置菜单里用户数据是否恢复默认值") as step2:
                pass
        with self.step.start(headline="检查launcher默认模板下的各个Tab页") as step:
            with step.start(headline="切换tv进入标准桌面") as step2:
                pass
            with step.start(headline="非TCL品牌，各个Tab页下不能出现TCL字样，海报中不能出现TCL的logo") as step2:
                pass
        with self.step.start(headline="检查HDMI高级标准默认值") as step:
            pass

    def cleanup(self, **kwargs):
        with self.step.start(headline="电视回到主页") as step:
            pass

    class TcDemoSetting(TestSettingBase):
        case_setting1 = "setting1"
        case_setting2 = 10
        TIMEOUT = 60
