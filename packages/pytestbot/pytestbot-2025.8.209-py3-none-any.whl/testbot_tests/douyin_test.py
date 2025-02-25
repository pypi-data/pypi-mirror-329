#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import requests
from bs4 import BeautifulSoup

def get_douyin_video_url(video_url):
    # 发起请求
    try:
        response = requests.get(video_url, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        print(f"请求抖音视频发生错误: {e}")
        return None

    # 解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找视频链接
    try:
        video_data = soup.find('video')
        video_src = video_data['src']
        return video_src  # 返回视频播放链接
    except Exception as e:
        print(f"解析视频链接发生错误: {e}")
        return None


if __name__ == "__main__2":
    # 示例用法
    video_url = "https://www.douyin.com/video/7417309907449351435"  # 替换为实际抖音视频链接
    video_src = get_douyin_video_url(video_url)

    if video_src:
        print(f"获取到的视频链接: {video_src}")
    else:
        print("未能获取到视频链接")


if __name__ == "__main__":
        import douyin

        # 创建 DouYin 实例
        dy = douyin.DouYin()

        # 获取用户信息
        user = dy.get_user('testbot')

        # 获取粉丝数量
        follower_count = user['follower_count']

        print(f'抖音号 douyin 的粉丝数量为：{follower_count}')