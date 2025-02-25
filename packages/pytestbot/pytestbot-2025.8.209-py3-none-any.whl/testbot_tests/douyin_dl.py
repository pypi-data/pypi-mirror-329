#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import requests
from bs4 import BeautifulSoup

class DouyinDownloader:
    def __init__(self, url):
        self.url = url
        self.video_url = ""

    def download_video(self):
        # 发送请求获取网页内容
        response = requests.get(self.url)
        if response.status_code == 200:
            # 使用BeautifulSoup解析网页
            soup = BeautifulSoup(response.text, 'html.parser')
            # 提取视频的原始URL
            self.video_url = self._extract_video_url(soup)
            print(f"self.video_url={self.video_url}")
            if self.video_url:
                # 下载视频
                self._save_video(self.video_url)

    def _extract_video_url(self, soup):
        # 这里需要根据抖音网页的结构进行解析，具体实现可能因版本而异
        # 以下代码仅为示例，实际使用时需要根据实际情况调整
        video_tag = soup.find('video')
        if video_tag:
            return video_tag['src']
        return ""

    def _save_video(self, video_url):
        # 发送请求下载视频
        video_response = requests.get(video_url)
        if video_response.status_code == 200:
            # 保存视频到本地
            with open('douyin_video.mp4', 'wb') as video_file:
                video_file.write(video_response.content)
            print("视频下载完成！")
        else:
            print("视频下载失败！")


if __name__=="__main__":
    # dl = DouyinDownloader(url="https://www.douyin.com/user/MS4wLjABAAAACIs5MzoOHIuWssmIINOjhxc34XXx9Ym3H2TD3cDbuRBm1cCZwWe0oKWFK9_v0xfw?from_tab_name=main&modal_id=7428940998916443404&relation=2&vid=7417309907449351435")
    # dl.download_video()

    url = "https://v.douyin.com/CeinRQb8/"
    html = requests.get(url, allow_redirects=False)
    url2 = html.headers['Location']  # 获取跳转地址
    print(url2)

    video_id = url2.split("/")[5]
    print(video_id)

    url3 = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400',
        'cookie': '__gads=ID=0613c5de4392f6a6-2268f52184cf0004:T=1640239783:RT=1640239783:S=ALNI_MYFmzURQ4PZLUsx8kWq5VTByZe82A; Hm_lvt_338f36c03fc36a54e79fbd2ebdae9589=1640239784,1640259798; Hm_lpvt_338f36c03fc36a54e79fbd2ebdae9589=1640259798'
    }
    html2 = requests.get(url3, headers=headers)  # 请求json链接
    # html2 = requests.get(url3)  # 请求json链接
    print("resp:"+html2.text)
    # title = html2.json()['item_list'][0]['desc']  # 抖音视频的文案内容
    # video_id = html2.json()['item_list'][0]['video']['play_addr']['uri']  # 视频的uri，也就是video_id
    # video_url = f'https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}&ratio=720p&line=0'
    # print(video_id, video_url)

