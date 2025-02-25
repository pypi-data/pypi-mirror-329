#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

"""
@TC_ID          : SQAOSTC-78198
@Introduction   : Idle期按红外遥控器数字键唤醒电视
@Description    : 功能描述：
串口出现：DeviceIdleController: Moved from STATE_LOCATING to STATE_IDLE.时，电视进入Idle界面
@Precondition   : 
1、STR为ON，Doze mode为ON
2、调整Idle时间的方法：串口执行：dumpsys deviceidle IDLE_TIMEOUT set 300000（300000为时间，可修改）
3、遥控器未配对
@Steps:
1、连接网络，切换到HDMI信源
2、串口执行：
1.dumpsys deviceidle tlog set DEBUG 1 ；
2.logcat | grep DeviceIdleController&；按Power键待机
3、有切换到idle状态的打印后，使用红外遥控器，按数字键，检查电视变化
4、Doze mode设置为关，使用红外遥控器按数字键待机开机

【备注】仅适用海外
@Expected       :
2、串口打印：DeviceIdleController: Moved from STATE_LOCATING to STATE_IDLE.
3、电视整响应遥控器按键操作，成功唤醒
4、待机串口不会有Doze模式打印，电视可以响应遥控器按键操作，成功唤醒
"""

from testbot.case.base import TestCaseBase, TestType
from testbot.case.decorator import case
from testbot.config.setting import TestSettingBase
from testbot.resource.pool import ResourcePool
from testbot.result.testreporter import CaseEntry


@case(priority=1, test_type=TestType.SMOKE_TEST.name, testcase_id="SQAOSTC-78198", testcase_name="测试用例Demo演示")
class TCDemo(TestCaseBase):

    def collect_resource(self, node: CaseEntry, pool: ResourcePool):
        self.logger.info("执行collect_resource方法")
        # 结构化验证点实现方式
        # with node.start(headline="筛选设备", message="") as step:
        #     with step.start(headline="筛选PC设备", message="") as step2:
        #         self.pc = pool.collect_device(device_type="PCDevice", count=1)[0]
        #         if self.pc:
        #             step2.passed(message="筛选PC设备成功")
        #         else:
        #             step2.failed(message="筛选PC设备失败")
        #     with step.start(headline="筛选TV设备", message="") as step2:
        #         self.tv = pool.collect_device(device_type="TVDevice", count=1)[0]
        #         if self.tv:
        #             step2.passed(message="筛选TV设备成功")
        #         else:
        #             step2.failed(message="筛选TV设备失败")
        pass

    def setup(self, node: CaseEntry, **kwargs):
        self.logger.info("执行setup方法")
        # 结构化验证点实现方式
        # self.logger.info(f"case_setting1={self.setting.case_setting1}, case_setting2={self.setting.case_setting2}, TIMEOUT={self.setting.TIMEOUT}")
        with node.start(headline="", message="") as step:
            step.passed(message="设置STR为ON")
        with node.start(headline="", message="") as step:
            step.passed(message="设置STR为ON")
        with node.start(headline="", message="设置待机时长") as step:
            pass
        with node.start(headline="", message="") as step:
            step.info(message="安装WIFI apk")
        with node.start(headline="", message="断开有线连接") as step:
            step.passed(message="断开有线连接")
        with node.start(headline="", message="") as step:
            step.passed(message="连接并检查WIFI热点")

    def test(self, node: CaseEntry, **kwargs):
        self.logger.info("执行test方法")
        with node.start(headline="", message="") as step:
            step.passed(message="打开Youtube播放任意视频")
        with node.start(headline="", message="") as step:
            step.passed(message="按power键进入待机状态")
        with node.start(headline="", message="") as step:
            step.passed(message="等待5秒后，按power键唤醒电视")
        with node.start(headline="", message="") as step:
            step.passed(message="开机后检查WIFI热点")
        with node.start(headline="", message="") as step:
            step.passed(message="开机后进入在线视频")
        with node.start(headline="", message="") as step:
            # self.tv.PowerModule.power_off()
            step.passed(message="给电视断电")
        with node.start(headline="", message="") as step:
            # self.tv.PowerModule.power_on()
            step.passed(message="给电视上电")
        with node.start(headline="", message="") as step:
            step.passed(message="等待30秒后，按power键唤醒电视")
        with node.start(headline="", message="") as step:
            step.passed(message="开机后检查WIFI热点")
        with node.start(headline="", message="") as step:
            1 / 0
            pass
            step.passed(message="开机后进入Launcher页面")
        with step.start(headline="", message="") as step:
            step.passed(message="打开Youtube播放任意视频")

    def cleanup(self, node: CaseEntry, **kwargs):
        self.logger.info("执行cleanup方法")
        with node.start(headline="", message="") as step:
            step.passed(message="断开WIFI热点")
        with node.start(headline="", message="") as step:
            step.passed(message="关闭WIFI开关")

    class TCDemoSetting(TestSettingBase):
        case_setting1 = "setting1"
        case_setting2 = 10
        TIMEOUT = 60


if __name__ == "__main__":
    tc = TCDemo()
    tc.start()
