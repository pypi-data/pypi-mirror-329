#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import re
import time
import json
import base64

import requests

from testbot.resource.module import TCLTVDeviceWrapperModuleBase
from testbot.resource.module import TCLTVDeviceWrapperModuleBase, set_as_grpc_api
from testbot.resource.protoc import tv_audio_pb2_grpc, basic_type_pb2, tv_picture_pb2_grpc


class SettingsWrapperModule(TCLTVDeviceWrapperModuleBase):
    """
    TCLTV测试设备源封装接口设置模块类
    """
    # 串口实例
    serial_instance = None
    # 红外实例
    infrared_instance = None
    # adb实例
    adb_instance = None
    # uiautomator2 实例
    u2_instance = None
    # tv串口操作实例
    tv_serial_instance = None
    #
    # 主页包名
    CYBERUI_PACKAGE = "com.tcl.cyberui/.MainActivity"

    grpc_instance = None

    # settings当前选中的菜单
    SETTINGS_ITEM_TEXT_SELECTED_XPATH = '//android.widget.TextView[@selected="true"]'
    # settings当前选中的菜单的第二个值
    SETTINGS_ITEM_VALUE_XPATH = "//*[@resource-id='com.tcl.settings:id/settings_item_view_value' and @selected='true']"

    def init(self):
        infrared_port = self.resource.get_port(type="InfraredSerialPort").name
        serial_port = self.resource.get_port(type="CommSerialPort").name
        # adb_port = self.resource.get_port(type="AdbPort").name
        self.logger.info(f"infrared_port ={infrared_port}")
        self.logger.info(f"serial_port ={serial_port}")
        self.init_remote(remote_port=infrared_port)
        self.init_serial(serial_port=serial_port)
        self.init_adb_and_u2()

    def init_grpc(self, ip: str = None, port: int = 60000):
        pass

    def init_remote(self, remote_port):
        """初始化红外工具类"""
        pass

    def init_serial(self, serial_port):
        """初始化串口"""
        pass

    def init_adb_and_u2(self):
        """初始化adb和uiautomator2"""
        pass

    def enter_all_settings(self):
        """
        进入全部设置界面
        """
        # self.remote.setting()
        # time.sleep(2)
        # self.remote.ok()
        # self.logger.info("进入全部设置界面")
        # 修改为串口指令启动
        for _ in range(3):
            SettingsWrapperModule.tv_serial_instance.enter_settings()
            if "com.tcl.settings" in SettingsWrapperModule.tv_serial_instance.get_current_focus_activity():
                self.logger.info("进入全部设置界面成功")
                return
            time.sleep(2)
        else:
            self.logger.info("进入全部设置界面失败")
            raise Exception("尝试三次进入全部设置界面失败")

    def enter_settings_menu_do_factory_reset(self):
        """
        进入设置菜单做恢复出厂设置操作

        """
        retry_count = 0
        max_retries = 3
        while retry_count <= max_retries:
            self.logger.info(f"进入设置菜单做恢复出厂设置操作:（尝试第{retry_count + 1}/{max_retries}次）")
            self.enter_all_settings()
            try:
                self.enter_level_menu(["关于", "恢复出厂设置"], find_direction=False)
                if "com.tcl.versionUpdateApp" in SettingsWrapperModule.tv_serial_instance.get_current_focus_activity():
                    self.logger.info("当前页面在恢复出厂设置页面")
                    if SettingsWrapperModule.u2_instance.check_selected_focused_by_text("确定"):
                        SettingsWrapperModule.tv_serial_instance.ok()
                        time.sleep(120)
                        return True
                    else:
                        SettingsWrapperModule.tv_serial_instance.right(count=3)
                        SettingsWrapperModule.tv_serial_instance.ok()
                        time.sleep(120)
                        return True
            except Exception as e:
                # 记录失败原因
                self.logger.info(f"尝试失败，原因：{e}")
            retry_count += 1
            if retry_count < max_retries:
                self.logger.info(f"准备第{retry_count + 1}次重试...")
            else:
                self.logger.error(f"进入设置菜单做恢复出厂设置操作失败，已达到最大重试次数{max_retries}次。")
                return False

    def enter_settings_menu_check_hdmi_control_value(self):
        """
        进入设置菜单检查HDMI设备控制开关是否打开

        """
        # 由于开关值是图片显示，采用坐标来判断
        target_bounds = [716, 201, 774, 231]
        retry_count = 0
        max_retries = 3
        while retry_count <= max_retries:
            self.logger.info(f"进入设置菜单检查HDMI设备控制开关是否打开操作:（尝试第{retry_count + 1}/{max_retries}次）")
            self.enter_all_settings()
            try:
                self.enter_level_menu(["信号源", "HDMI设备控制(CEC)"])
                if SettingsWrapperModule.u2_instance.check_element_exits_by_text(text="HDMI设备控制"):
                    self.logger.info("当前进入到HDMI设备控制(CEC)")
                    img_obj = SettingsWrapperModule.u2_instance.find_element_by_resource_id(
                        "com.tcl.settings:id/settings_toggle_thumb")
                    current_bounds = str(img_obj.info["bounds"])
                    self.logger.info(f"当前开关bounds值为{current_bounds}")
                    if all(self.number_in_string(number, current_bounds) for number in target_bounds):
                        self.logger.info("设备控制开关为打开状态")
                        return True
                    self.logger.info("设备控制开关为关闭状态")
                    return False
            except Exception as e:
                # 记录失败原因
                self.logger.info(f"尝试失败，原因：{e}")
            retry_count += 1
            if retry_count < max_retries:
                self.logger.info(f"准备第{retry_count + 1}次重试...")
            else:
                self.logger.error(f"进入设置菜单做恢复出厂设置操作失败，已达到最大重试次数{max_retries}次。")
                return False

    def enter_level_menu(self, menus: list, last_enter=True, find_direction=True):
        """
        进入设置应用的多级菜单
        :param menus: 菜单列表
        :param last_enter: 最后一个菜单是否要进入
        :param find_direction: 查找方向 True:向下查找 False:向上查找
        """
        for index, m in enumerate(menus):
            for i in range(20):
                menu = SettingsWrapperModule.u2_instance.find_element_by_xpath(
                    SettingsWrapperModule.SETTINGS_ITEM_TEXT_SELECTED_XPATH).get_text()
                # if menu == m:
                # 暂时新增文字包含关键字也算找到
                if menu == m or m in menu:
                    self.logger.info(f"找到菜单 {menu}")
                    if index == len(menus) - 1:
                        if last_enter:
                            SettingsWrapperModule.tv_serial_instance.ok(t=0)
                            self.logger.info(f"当前在 {menu} 界面")
                    else:
                        SettingsWrapperModule.tv_serial_instance.ok(t=0)
                    break
                else:
                    self.logger.info(f"向下查找 当前在:{menu}")
                    if find_direction:
                        SettingsWrapperModule.tv_serial_instance.down(t=0)
                    else:
                        SettingsWrapperModule.tv_serial_instance.up(t=0)
            else:
                raise Exception(f"进入指定的{menus}设置应用的多级菜单失败")

    def enter_vod_play_video_and_check(self):
        """
        进入vod播放视频,并检查是否成功
        """
        for _ in range(3):
            SettingsWrapperModule.tv_serial_instance.start_vod_clear_play()
            if SettingsWrapperModule.tv_serial_instance.check_activity("com.tcl.vod"):
                self.logger.info("进入vod播放视频成功")
                return True
        self.logger.error("进入vod播放视频失败")
        return False

    def enter_home(self):
        """
        进入TV主页
        """
        self.logger.info("进入TV主页")
        for _ in range(3):
            SettingsWrapperModule.serial_instance.exec_command("input keyevent 4 4 3", with_root=False)
            if SettingsWrapperModule.tv_serial_instance.check_activity(SettingsWrapperModule.CYBERUI_PACKAGE):
                self.logger.info("进入主页成功")
                return True
            time.sleep(2)
        else:
            self.logger.info("进入主页失败")
            return False

    def connect_wifi(self, wifi_name, wifi_pwd):
        """
        连接指定wifi热点

        参数:
        wifi_name (string类型): wifi名
        wifi_pwd (string类型): wifi密码

        """
        return SettingsWrapperModule.tv_serial_instance.connect_wifi(ssid=wifi_name, pwd=wifi_pwd)

    def get_image_text3(self, file_path: str):
        start_time = time.time()
        headers = {"Content-type": "application/json"}
        img = open(file_path, 'rb').read()
        b = base64.b64encode(img).decode('utf8')
        data = {'images': [b]}
        r = requests.post(url='http://10.120.26.2:8868/predict/ocr_system', headers=headers, data=json.dumps(data))
        # 打印data数据和返回结果
        data = r.json()
        text = None
        if "results" in data:
            result1 = data["results"][0]
            text = ""
            for res in result1:
                if "text" in res:
                    text += res["text"] + "\n"
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"这次代码执行耗时: {elapsed_time} 秒")
        print("识别结果：\n【%s】\n" % text)
        return text

    def check_keyword_in_tabs(self, keywords: list, ignore_case: bool = False, time_out=120) -> bool:
        """
        在Tab页检查是否有关键字

        :return:
        :rtype:
        """
        # 位移到最左边的tab页面，采取找到“应用中心“后“+”字段结束循环
        # "+" tab页 classname= android.view.View
        found = False
        last_selected_tab_class_name = "android.view.View"
        self.tv_serial_instance.left(count=5, t=0.5)
        begin_time = time.time()
        time_out = time_out
        while time.time() - begin_time < time_out:
            try:
                selected_tab_class_name = SettingsWrapperModule.u2_instance.find_element_by_focused().info['className']
            except Exception as e:
                self.logger.info(f"异常信息{e}")
                selected_tab_class_name = ""
            if selected_tab_class_name == last_selected_tab_class_name:
                # 找到也要执行最后一次逻辑
                # 截图
                logpath = self.logger.handlers[0].baseFilename
                self.logger.info(f"日志路径：{logpath}")
                pic_path = os.path.join(os.path.dirname(logpath), f"image-{int(round(time.time() * 1000))}.png")
                self.adb_instance.shell_for_result(command="screencap /sdcard/image.png")
                self.adb_instance.adb_for_process(command=f"pull /sdcard/image.png {pic_path}")
                time.sleep(2)
                # OCR文字识别
                data = self.get_image_text3(file_path=pic_path)
                if ignore_case:
                    for keyword in keywords:
                        if data != "" and keyword.upper() in data.upper():
                            found = True
                            break
                else:
                    for keyword in keywords:
                        if data != "" and keyword in data:
                            found = True
                            break
                break
            else:
                # 截图
                logpath = self.logger.handlers[0].baseFilename
                self.logger.info(f"日志路径：{logpath}")
                pic_path = os.path.join(os.path.dirname(logpath), f"image-{int(round(time.time() * 1000))}.png")
                self.adb_instance.shell_for_result(command="screencap /sdcard/image.png")
                self.adb_instance.adb_for_process(command=f"pull /sdcard/image.png {pic_path}")
                time.sleep(2)
                # OCR文字识别
                data = self.get_image_text3(file_path=pic_path)
                if ignore_case:
                    for keyword in keywords:
                        if data != "" and keyword.upper() in data.upper():
                            found = True
                            break
                else:
                    for keyword in keywords:
                        if data != "" and keyword in data:
                            found = True
                            break
                # 若包含关键字，则break，否则切换到下一个TAB
                if found:
                    break
                else:
                    self.tv_serial_instance.right(t=0.5)
                    continue
        return found

    def check_and_install_app(self, package_name, package_path):
        """
        检查是否安装指定包名apk，未安装则安装指定路径下apk

        """
        if not SettingsWrapperModule.serial_instance.re_search(command=f"pm list package|grep '{package_name}'",
                                                               pattern=f"package:{package_name}"):
            self.logger.warn(f"检测到未安装 {package_name} apk,进行安装")
            SettingsWrapperModule.adb_instance.connect()
            result = SettingsWrapperModule.adb_instance.cmd(f"install -r -t {package_path}")
            if "Success" in result:
                self.logger.info("安装apk成功")
                return True
            self.logger.info(f"安装异常：{result}")
            return False
        self.logger.info("检查已安装apk")
        return True

    def skip_startup_wizard(self):
        """
        跳过开机向导
        """
        cmd_list = ["settings put secure user_setup_complete 1", "settings put global device_provisioned 1",
                    "pm disable com.tcl.initsetup/com.tcl.initsetup.unitizeui.ui.UnitizeUIActivity"]
        SettingsWrapperModule.serial_instance.exec_commands(cmd_list=cmd_list)
        if self.enter_home():
            self.logger.info("跳过开机向导成功")
            return True
        self.logger.error("跳过开机向导失败")
        return False

    def excute_pre_install_cmd(self):
        """
        执行安装前置指令
        """
        cmd_list = ["setprop debug.configprovider.enable 1", "setprop debug.vendor.config_download.self_test 1",
                    "am restart"]
        SettingsWrapperModule.serial_instance.exec_commands(cmd_list=cmd_list)
        time.sleep(20)
        cmd = 'feature update InstallConfig \'[{"enable":"true","strategies":[{"name":"safeStrategy","enable":"true",' \
              '"priority":"0"},{"name":"blackListStrategy","enable":"false","packages":[""],"priority":"1"},' \
              '{"name":"thridStrategy","enable":"true","packages":["com.dangbeimarket","com.shafa.market"],' \
              '"priority":"2"},{"name":"launcherStrategy","enable":"false","packages":["com.manager.mylauncher"],' \
              '"priority":"3"},{"name":"overDueStrategy","enable":"true","packages":[""],"priority":"4"},' \
              '{"name":"pmStrategy","enable":"false","priority":"5"}]}]\' database '
        result = SettingsWrapperModule.serial_instance.exec_command(cmd=cmd)
        if "type_onComand:database" in result:
            return True
        return False

    def check_pre_install_cmd(self):
        """
        检查是否执行安装前置指令
        """
        key = '[{"name":"safeStrategy","enable":"true","priority":"0"}'
        cmd = 'feature query InstallConfig'
        result = SettingsWrapperModule.serial_instance.exec_command(cmd=cmd)
        if key in result:
            return True
        return False

    def check_pre_install_cmd_and_excute(self):
        """
        检查是否执行安装前置指令,没有则执行
        """
        if not self.check_pre_install_cmd():
            self.logger.info("查询到未执行安装前置指令,现在执行")
            return self.excute_pre_install_cmd()
        self.logger.info("已执行安装前置指令")
        return True

    def check_and_start_grpc_service(self, time_out=10):
        """
        检查 GRPC 服务是否启动，如果未启动则尝试启动并检查是否在超时内成功启动。

        :param time_out: 超时时间（秒）
        """
        start_time = time.time()  # 记录开始时间
        service_started = False  # 服务启动标志

        while time.time() - start_time < time_out:
            try:
                # 检查 GRPC 服务是否已启动
                result1 = SettingsWrapperModule.adb_instance.shell_for_result(command="\"ps -ef | grep 'ff'\"")
                result2 = SettingsWrapperModule.adb_instance.shell_for_result(
                    command="\"dumpsys activity services | grep 'com.tcl.fftestmonitor'\"")

                if "com.tcl.fftestmonitor" in result1 and "com.tcl.fftestmonitor/.service.GrpcNettyService" in result2:
                    self.logger.info("GRPC 服务已经启动")
                    service_started = True
                    time.sleep(10)
                    return service_started

                # 如果服务没有启动，尝试启动
                self.logger.warn("检查到 GRPC 服务进程不存在，启动服务")
                SettingsWrapperModule.adb_instance.shell("am startservice -n com.tcl.fftestmonitor/.service"
                                                         ".GrpcNettyService")
                time.sleep(2)

            except Exception as e:
                self.logger.error(f"调用异常：{e}")
                return False

        if not service_started:
            self.logger.error("在指定时间内 GRPC 服务未能启动成功。")
            return service_started

    def get_ip(self):
        for _ in range(3):
            SettingsWrapperModule.serial_instance.interrupt()
            address_info = SettingsWrapperModule.serial_instance.exec_command("ifconfig eth0")
            pattern = re.compile(r"inet addr:\s*(\d+\.\d+\.\d+\.\d+)\s*")
            if address_info and re.search(pattern, address_info):
                ip_list = re.findall(pattern, address_info)
                for ip in ip_list:
                    return ip
            # #  新增查找wlan0
            # address_info = SettingsWrapperModule.serial_instance.exec_command("ifconfig wlan0")
            # pattern = re.compile(r"inet addr:\s*(\d+\.\d+\.\d+\.\d+)\s*")
            # if address_info and re.search(pattern, address_info):
            #     ip_list = re.findall(pattern, address_info)
            #     for ip in ip_list:
            #         return ip
        return None

    def enter_standard_desktop(self):
        """
        跳转到标准桌面
        """
        SettingsWrapperModule.serial_instance.exec_command(
            "am start -n com.tcl.cyberui/com.tcl.mllauncher.mlchange.MlChangeSysActivity")
        SettingsWrapperModule.tv_serial_instance.right(count=3, t=0.5)
        SettingsWrapperModule.tv_serial_instance.ok()
        if SettingsWrapperModule.tv_serial_instance.check_activity(SettingsWrapperModule.CYBERUI_PACKAGE):
            self.logger.info("进入主页成功")
            return True
        return False

    def enter_smart_desktop(self):
        """
        跳转到灵动桌面
        """
        for _ in range(3):
            SettingsWrapperModule.serial_instance.exec_command(
                "am start -n com.tcl.cyberui/com.tcl.mllauncher.mlchange.MlChangeSysActivity")
            SettingsWrapperModule.tv_serial_instance.left(count=3, t=1)
            SettingsWrapperModule.tv_serial_instance.ok()
            if SettingsWrapperModule.tv_serial_instance.check_activity(SettingsWrapperModule.CYBERUI_PACKAGE):
                self.logger.info("进入主页成功")
                return True
        return False

    def number_in_string(self, number, target_string):
        """
        检查目标字符串中是否存在完整的数字。

        参数:
            number: 要检查的数字。
            target_string: 目标字符串。
        返回:
            布尔值: 如果完整的数字存在于目标字符串中，则返回 True，否则返回 False。
        """
        pattern = r"\b" + str(number) + r"\b"  # 使用 \b 确保是完整的数字
        return re.search(pattern, target_string) is not None

    @set_as_grpc_api(timeout=60, duration=3)
    def set_picture_mode(self, value: int) -> bool:
        """
        设置图效

        :param value:范围0-6，对应模式：0-标准，1-明亮，2-柔和，3-FILMMAKER MODE，4-电影，5-办公，6-智能
        :type value:int类型
        :return: 设置是否成功
        :rtype: bool
        """
        for _ in range(3):
            try:
                stub = tv_picture_pb2_grpc.SettingsPictureStub(self.grpc_instance)
                request = basic_type_pb2.IntType(value=value)
                response = stub.setPictureMode(request)
                if response:
                    return response.value
                else:
                    return False
            except Exception as e:
                self.logger.warn(f"grpc调用异常：{e}")
                self.check_and_start_grpc_service()
        else:
            return False

    @set_as_grpc_api(timeout=60, duration=3)
    def get_picture_mode(self):
        """
        获取图效

        :return: 图效值，范围0-6，对应模式：0-标准，1-明亮，2-柔和，3-FILMMAKER MODE，4-电影，5-办公，6-智能
        :rtype: int类型
        """
        for _ in range(3):
            try:
                stub = tv_picture_pb2_grpc.SettingsPictureStub(self.grpc_instance)
                request = basic_type_pb2.Empty()
                response = stub.getPictureMode(request)
                if response:
                    return response.value
                else:
                    return -1
            except Exception as e:
                self.logger.warn(f"grpc调用异常：{e}")
                self.check_and_start_grpc_service()
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
        for _ in range(3):
            try:
                stub = tv_audio_pb2_grpc.SettingsAudioStub(self.grpc_instance)
                request = basic_type_pb2.IntType(value=value)
                stub.setAudioOption(request)
                return True
            except Exception as e:
                self.logger.warn(f"grpc调用异常：{e}")
                self.check_and_start_grpc_service()
        else:
            return False

    @set_as_grpc_api(timeout=60, duration=3)
    def get_audio_option(self) -> int:
        """
        获取音效

        :return: 音效值， 范围 0-7，对应模式：0：标准 1：电影 2：音乐 3：新闻 4：游戏 5：体育 6：用户自定义 7：智能,异常返回 -1
        :rtype: int类型
        """
        for _ in range(3):
            try:
                stub = tv_audio_pb2_grpc.SettingsAudioStub(self.grpc_instance)
                request = basic_type_pb2.Empty()
                response = stub.getAudioOption(request)
                if response:
                    return response.value
                else:
                    return -1
            except Exception as e:
                self.logger.warn(f"grpc调用异常：{e}")
                self.check_and_start_grpc_service()
        else:
            return -1
