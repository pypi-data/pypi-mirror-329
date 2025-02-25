#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import itchat
from itchat.content import TEXT


if __name__ == "__main__":
    # 登录微信
    itchat.auto_login(hotReload=True)
    # 扫描二维码登录
    @itchat.msg_register(TEXT)
    def text_reply(msg):
        return '我收到了你的消息:%s' % msg['Text']
    # 开始监听和自动回复
    itchat.run()
