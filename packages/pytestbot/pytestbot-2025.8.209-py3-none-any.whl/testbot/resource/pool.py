#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import re
import cv2
import time
import json
import serial
import platform
from serial.tools import list_ports

from testbot.result.logger import logger_manager
from testbot.resource.resource import ResourceError
from testbot.config import MODULE_LOGS_PATH, CONFIG_PATH
from testbot.config.static_setting import ResourceSetting
from testbot.resource.device.device import PCDevice, TVDevice
from testbot.resource.device.device import Device
from testbot.resource.constraint import ConnectionConstraint, ResourceNotMeetConstraint


class ResourcePool(object):
    """
    资源池类，负责资源的序列化和反序列化以及储存和读取
    """
    def __init__(self, *args, **kwargs):
        self.logger = kwargs.get("logger", logger_manager.register(logger_name="Resource", filename=os.path.join(MODULE_LOGS_PATH, "Resource.log"), for_test=True))
        self.topology = dict()
        self.reserved = None
        self.information = dict()
        self.file_name = None
        self.owner = None

    def add_device(self, device_name: str, **kwargs):
        """
        添加设备到资源池

        :param device_name: 设备名称
        :type device_name: str
        :param kwargs: 键值对参数
        :type kwargs: dict
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.add_device...")
        if device_name in self.topology:
            raise ResourceError(f"device {device_name} already exists")
        self.topology[device_name] = Device(device_name, **kwargs)
        self.logger.info(f"Exiting {self.__class__.__name__}.add_device...")

    def reserve(self):
        """
        占用当前资源

        :return:
        :rtype:
        """
        self.logger.info(f"Entering {self.__class__.__name__}.reserve...")
        if self.file_name is None:
            raise ResourceError("load a resource file first")
        self.load(self.file_name, self.owner)
        self.reserved = {"owner": self.owner, "date": time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())}
        self.save(self.file_name)
        self.logger.info(f"Exiting {self.__class__.__name__}.reserve...")

    def release(self):
        """
        释放当前资源

        :return:
        :rtype:
        """
        self.logger.info(f"Entering {self.__class__.__name__}.release...")
        if self.file_name is None:
            raise ResourceError("load a resource file first")
        self.load(self.file_name)
        self.reserved = None
        self.save(self.file_name)
        self.logger.info(f"Exiting {self.__class__.__name__}.release...")

    def collect_device(self, device_type, count, constraints=list()):
        ret = list()
        for key, value in self.topology.items():
            if value.type == device_type:
                for constraint in constraints:
                    if not constraint.is_meet(value):
                        break
                else:
                    ret.append(value)
            if len(ret) >= count:
                return ret
        else:
            return list()

    def collect_all_device(self, device_type, constraints=list()):
        ret = list()
        for key, value in self.topology.items():
            if value.type == device_type:
                for constraint in constraints:
                    if not constraint.is_meet(value):
                        break
                else:
                    ret.append(value)
        return ret

    def collect_connection_route(self, resource: str, constraints: list=list()) -> list:
        """
        获取资源连接路由

        :param resource:
        :type resource:
        :param constraints:
        :type constraints:
        :return: 链接路由
        :rtype: list
        """
        # 限制类必须是连接限制ConnectionConstraint
        for constraint in constraints:
            if not isinstance(constraint, ConnectionConstraint):
                raise ResourceError(
                    "collect_connection_route only accept ConnectionConstraints type")
        ret = list()
        for constraint in constraints:
            conns = constraint.get_connection(resource)
            if not any(conns):
                raise ResourceNotMeetConstraint([constraint])
            for conn in conns:
                ret.append(conn)
        return ret

    def load(self, filename: str, owner: str):
        """
        加载文件

        :param filename: 文件路径
        :type filename: str
        :param owner: 资源所有人
        :type owner: str
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.load...")
        # 检查文件是否存在
        if not os.path.exists(filename):
            # raise ResourceError(f"Cannot find file {filename}")
            self.save(filename=filename)
        self.file_name = filename

        # 初始化
        self.topology.clear()
        self.reserved = False
        self.information = dict()

        #读取资源配置的json字符串
        with open(filename) as file:
            json_object = json.load(file)

        #判断是否被占用
        # if "reserved" in json_object and json_object['reserved'] is not None and json_object['reserved']['owner'] != owner:
        #     raise ResourceError(f"Resource is reserved by {json_object['reserved']['owner']}")

        self.owner = owner

        if "info" in json_object:
            self.information = json_object['info']
        for key, value in json_object['devices'].items():
            res_obj = None
            resource_type = value.get("type", None)
            if resource_type == "PCDevice":
                res_obj = PCDevice.from_dict(dict_obj=value)
            if resource_type == "TVDevice":
                res_obj = TVDevice.from_dict(dict_obj=value)
            self.topology[key] = res_obj

        # 映射所有设备的连接关系
        for key, device in json_object['devices'].items():
            for port_name, port in device['ports'].items():
                for remote_port in port['remote_ports']:
                    remote_port_obj = self.topology[remote_port["device"]].ports[remote_port["port"]]
                    self.topology[key].ports[port_name].remote_ports.append(remote_port_obj)
        self.logger.info(f"topology={self.topology}")
        self.logger.info(f"Exiting {self.__class__.__name__}.load...")

    def to_dict(self):
        root_object = dict()
        root_object['devices'] = dict()
        root_object['info'] = self.information
        root_object['reserved'] = self.reserved
        for device_key, device in self.topology.items():
            root_object['devices'][device_key] = device.to_dict()
        return root_object

    def save(self, filename: str):
        """
        保存文件

        :param filename: 文件路径
        :type filename: str
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.save...")
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, mode="w") as file:
            json.dump(self.to_dict(), file, indent=4)
        self.logger.info(f"Exiting {self.__class__.__name__}.save...")

    def _set_power_on(self):
        if platform.system() == 'Linux':
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(12, GPIO.OUT)
            GPIO.output(12, GPIO.HIGH)

    def _discover_infra_port(self):
        infra_port = None
        for port in list_ports.comports():
            if port[0].startswith("/dev/ttyUSB"):
                ser = None
                try:
                    ser = serial.Serial(port=port[0], baudrate=115200, timeout=1)
                    ser.write("\r\n".encode("UTF-8"))
                    ser.flush()
                    time.sleep(3)
                    data = ser.read_all()
                    if b'\xfe\xfd\xdf' in data:
                        infra_port = port[0]
                        ser.close()
                        break
                    else:
                        ser.close()
                except:
                    if ser:
                        ser.close()
        if not infra_port:
            raise Exception("搜索电视的红外串口失败！")
        return infra_port

    def _discover_video_port(self):
        video_index = None
        vid_indices = sorted(
            [int(dev.replace('video', '')) for dev in os.listdir('/dev') if dev.startswith('video') and dev])
        self.logger.info(f"发现采集卡端口：{vid_indices}")
        for vid in vid_indices:
            cap = cv2.VideoCapture(index=vid)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920.0)  # 画面帧宽度
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080.0)  # 画面帧高度
            cap.set(cv2.CAP_PROP_FPS, 30.0)  # 帧率
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 缓存帧数，返回False不支持缓冲区设置
            if not cap.isOpened() or not cap.grab():
                self.logger.info(f"当前采集卡端口：{vid}")
                raise Exception("搜索电视的采集卡串口失败！")
            else:
                video_index = vid
                break
        return video_index

    def _discover_comm_port(self):
        comm_port = None
        for port in list_ports.comports():
            if port[0].startswith("/dev/ttyUSB"):
                ser = None
                try:
                    ser = serial.Serial(port=port[0], baudrate=115200, timeout=1)
                    ser.write("\r\n".encode("UTF-8"))
                    ser.flush()
                    time.sleep(3)
                    data = ser.read_all().decode("UTF-8")
                    if 'console' in data:
                        comm_port = port[0]
                        ser.close()
                        break
                    else:
                        ser.close()
                except:
                    if ser:
                        ser.close()
        if not comm_port:
            raise Exception("搜索电视的指令串口失败！")
        return comm_port

    def _discover_ip_sn(self, comm_port):
        tv_ip, tv_sn = None, None
        ser = None
        ips = []
        try:
            ser = serial.Serial(port=comm_port, baudrate=115200, timeout=1)
            ser.flush()
            ser.write("ifconfig\r\n".encode("UTF-8"))
            time.sleep(3)
            output = ser.read_all().decode("UTF-8").strip()
            pat_ipv4 = re.compile(r'^\s*inet addr:(\S+)', flags=re.M)
            for _ip in pat_ipv4.findall(output):
                if _ip != "127.0.0.1":
                    ips.append(_ip)
            ser.flush()
            ser.write("getprop ro.boot.serialno\r\n".encode("UTF-8"))
            time.sleep(3)
            output = ser.read_all().decode("UTF-8").strip()
            pat_sn = re.compile(r'^\s*getprop ro.boot.serialno\r\r\n(\S+)\r\nconsole:', flags=re.M)
            tv_sn = pat_sn.findall(output)[0]
            if len(ips) >= 1 and tv_sn != "":
                tv_ip = ips[0]
                ser.close()
            else:
                ser.close()
        except:
            if ser:
                ser.close()
        if not tv_ip:
            raise Exception("获取电视的IP地址/序列号信息失败！")
        return tv_ip, tv_sn

    def discover_resources(self, filename: str = os.path.join(CONFIG_PATH, "pool.json"), owner: str = "sunny"):
        infra_port, video_index, comm_port, ip, pc_sn, tv_sn = None, None, None, None, None, None

        self._set_power_on()
        infra_port = self._discover_infra_port()
        video_index = self._discover_video_port()
        comm_port = self._discover_comm_port()
        ip, tv_sn = self._discover_ip_sn(comm_port=comm_port)

        self.load(filename=filename, owner=owner)
        pc, tv = None, None
        for key, device in self.topology.items():
            if getattr(device, "type", None) == "PCDevice":
                pc = device
            if getattr(device, "type", None) == "TVDevice":
                tv = device

        from tatf.resource.device.device import PCDevice
        data = open('/proc/cpuinfo', 'r').read()
        pat_sn = re.compile(r'^\s*Serial\t\t: (\S+)\n', flags=re.M)
        sns = pat_sn.findall(data)
        pc_sn = sns[0]
        if not pc or pc.name != pc_sn:
            pc = PCDevice(name=pc_sn)
        pc.add_port(name=comm_port, type="CommSerialPort", baud_rate=115200)
        pc.add_port(name=infra_port, type="InfraredSerialPort", baud_rate=115200)
        pc.add_port(name=f"/dev/video{video_index}", type="VideoStreamSerialPort")
        pc.add_port(name=f"{ip}:5555", type="AdbPort")
        pc.add_port(name=f"{ip}:60000", type="GRPCPort")
        pc.add_port(name="GPIO12", type="PowerPort")
        pc.add_port(name="GPIO26", type="HDMIPort")
        pc.add_port(name="GPIO21", type="EthernetPort")
        pc.add_port(name="GPIO5/6", type="USBPort")
        self.logger.info(f"pc={pc.ports}, data={pc.to_dict()}")

        from tatf.resource.device.device import TVDevice
        if not tv or tv.name != tv_sn:
            tv = TVDevice(name=tv_sn)
        tv.add_port(name="CommSerialPort", type="CommSerialPort")
        tv.add_port(name="InfraredSerialPort", type="InfraredSerialPort")
        tv.add_port(name="VideoStreamSerialPort", type="VideoStreamSerialPort")
        tv.add_port(name="AdbPort", type="AdbPort")
        tv.add_port(name="GRPCPort", type="GRPCPort")
        tv.add_port(name="PowerPort", type="PowerPort")
        tv.add_port(name="HDMIPort", type="HDMIPort")
        tv.add_port(name="EthernetPort", type="EthernetPort")
        tv.add_port(name="USBPort", type="USBPort")
        self.logger.info(f"tv={tv.to_dict()}")

        pc.ports[comm_port].remote_ports.append(tv.ports['CommSerialPort'])
        tv.ports['CommSerialPort'].remote_ports.append(pc.ports[comm_port])
        pc.ports[infra_port].remote_ports.append(tv.ports['InfraredSerialPort'])
        tv.ports['InfraredSerialPort'].remote_ports.append(pc.ports[infra_port])
        pc.ports[f'/dev/video{video_index}'].remote_ports.append(tv.ports['VideoStreamSerialPort'])
        tv.ports['VideoStreamSerialPort'].remote_ports.append(pc.ports[f'/dev/video{video_index}'])
        pc.ports[f'{ip}:5555'].remote_ports.append(tv.ports['AdbPort'])
        tv.ports['AdbPort'].remote_ports.append(pc.ports[f'{ip}:5555'])
        pc.ports[f'{ip}:60000'].remote_ports.append(tv.ports['GRPCPort'])
        tv.ports['GRPCPort'].remote_ports.append(pc.ports[f'{ip}:60000'])
        pc.ports['GPIO12'].remote_ports.append(tv.ports['PowerPort'])
        tv.ports['PowerPort'].remote_ports.append(pc.ports['GPIO12'])
        pc.ports['GPIO26'].remote_ports.append(tv.ports['HDMIPort'])
        tv.ports['HDMIPort'].remote_ports.append(pc.ports['GPIO26'])
        pc.ports['GPIO5/6'].remote_ports.append(tv.ports['USBPort'])
        tv.ports['USBPort'].remote_ports.append(pc.ports['GPIO5/6'])
        self.logger.info(f"pc2={pc.to_dict()}")
        self.logger.info(f"tv2={tv.to_dict()}")

        self.topology[pc_sn] = pc
        self.topology[tv_sn] = tv
        from tatf.config import CONFIG_PATH
        filepath = os.path.join(CONFIG_PATH, "pool.json")
        self.save(filename=filepath)
        self.logger.info(f"pool={self.to_dict()}")

    def init_resources(self, test_type):
        self.logger.info(f"pool.topology = {self.topology}")
        self.logger.info(f"test_type = {test_type}")
        for name, res_obj in self.topology.items():
            if res_obj.type == "PCDevice":
                res_obj.init_resource(test_type=test_type)
            if res_obj.type == "TVDevice":
                res_obj.init_resource(test_type=test_type)


def get_resource_pool(filename: str, owner: str) -> ResourcePool:
    """
    获取资源池，加载本地json文件以获取资源池，并设置该资源池的owner所有者

    :param filename: 资源池json文件路径
    :type filename: str
    :param owner: 资源所有者
    :type owner: str
    :return: 资源池对象
    :rtype: ResourcePool
    """
    ResourceSetting.load()
    full_name = os.path.join(ResourceSetting.resource_path, filename)
    rv = ResourcePool()
    rv.load(full_name, owner)
    return rv


if __name__ == "__main__":
    from testbot.resource.device import PCDevice, TVDevice
    pc = PCDevice(name="M70JP90W")
    tc = TVDevice(name="5C0AD0760BB0C50AD")

