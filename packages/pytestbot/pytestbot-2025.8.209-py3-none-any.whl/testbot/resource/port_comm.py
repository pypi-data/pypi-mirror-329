#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from abc import ABCMeta, abstractmethod


class Interoperable(metaclass=ABCMeta):

    @abstractmethod
    def send(self, cmd: str):
        pass

    @abstractmethod
    def send_binary(self, path: str):
        pass

    @abstractmethod
    def send_and_wait_for(self, cmd: str, wait_res: str, timeout: int, **kwargs):
        pass

    @abstractmethod
    def receive(self):
        pass

    @abstractmethod
    def receive_binary(self):
        pass


class CommandLine(Interoperable):

    def send(self, cmd: str):
        pass

    def send_binary(self, path: str):
        pass

    def send_and_wait_for(self, cmd: str, wait_res: str, timeout: int, **kwargs):
        pass

    def receive(self):
        pass

    def receive_binary(self):
        pass


class SerialComm(Interoperable):

    def send(self, cmd: str):
        self.logger.info("send")
        pass

    def send_binary(self, path: str):
        pass

    def send_and_wait_for(self, cmd: str, wait_res: str, timeout: int, **kwargs):
        pass

    def receive(self):
        pass

    def receive_binary(self):
        pass


class AdbComm(Interoperable):

    def send(self, cmd: str):
        pass

    def send_binary(self, path: str):
        pass

    def send_and_wait_for(self, cmd: str, wait_res: str, timeout: int, **kwargs):
        pass

    def receive(self):
        pass

    def receive_binary(self):
        pass


class GRPCComm(Interoperable):

    def send(self, cmd: str):
        pass

    def send_binary(self, path: str):
        pass

    def send_and_wait_for(self, cmd: str, wait_res: str, timeout: int, **kwargs):
        pass

    def receive(self):
        pass

    def receive_binary(self):
        pass


class SSHComm(Interoperable):

    def send(self, cmd: str):
        pass

    def send_binary(self, path: str):
        pass

    def send_and_wait_for(self, cmd: str, wait_res: str, timeout: int, **kwargs):
        pass

    def receive(self):
        pass

    def receive_binary(self):
        pass


class TelnetComm(Interoperable):

    def send(self, cmd: str):
        pass

    def send_binary(self, path: str):
        pass

    def send_and_wait_for(self, cmd: str, wait_res: str, timeout: int, **kwargs):
        pass

    def receive(self):
        pass

    def receive_binary(self):
        pass


class TCPComm(Interoperable):

    def send(self, cmd: str):
        pass

    def send_binary(self, path: str):
        pass

    def send_and_wait_for(self, cmd: str, wait_res: str, timeout: int, **kwargs):
        pass

    def receive(self):
        pass

    def receive_binary(self):
        pass
