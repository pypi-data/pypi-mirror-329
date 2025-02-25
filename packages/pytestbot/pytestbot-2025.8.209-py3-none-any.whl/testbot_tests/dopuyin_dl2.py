#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import requests  # 导入requests模块
import re
import os


def dy(txt):

    t = re.findall('(https://v.douyin.com/.*?/)', txt, re.S)
    if len(t)!=0:
        html = requests.get(t[0], allow_redirects=False)
        # 获取跳转地址
        url2=html.headers['Location']
        print(url2)
        item_ids = re.findall('video\/(.*?)\/\?', url2)
        if len(item_ids)!=0:
            ur=f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_ids[0]}'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400',
                'cookie': 'douyin.com; xg_device_score=7.453821943745746; device_web_cpu_core=4; device_web_memory_size=8; __ac_referer=__ac_blank; store-region=cn-gd; store-region-src=uid; xgplayer_user_id=162414252429; passport_csrf_token=9d48ab78d57063ec9ff6710a4c850587; passport_csrf_token_default=9d48ab78d57063ec9ff6710a4c850587; bd_ticket_guard_client_web_domain=2; toutiao_sso_user=c1bf7ced8716b454d7cdd6835b62bb09; toutiao_sso_user_ss=c1bf7ced8716b454d7cdd6835b62bb09; is_staff_user=false; _bd_ticket_crypt_doamin=2; __security_server_data_status=1; UIFID_TEMP=f934fcbcf795d539f0bfaf44dd326fe93e5e5daae30d485d476a271bea66637a1ef794940bab692168182a5cad1b7a8cea2aad762470f1cb8c4c77ce5a39ae25899c50594268a7e062f6acbd935c5e8a; s_v_web_id=verify_m24nrhe5_y7T178P9_WXgk_4rbg_B5ij_baPJLoTS9S2C; hevc_supported=true; fpk1=U2FsdGVkX18uRM47OerckDrvEICvkrQP14zCZoGT9NEdHZNvoYN6SWMRlD/yivddMVKC4TJJlDlTSvrPeQOhAA==; fpk2=9148266e558e3a256f7d785ca080c2a6; UIFID=f934fcbcf795d539f0bfaf44dd326fe93e5e5daae30d485d476a271bea66637a5d12a6ba583641ff39e8751b6542a4bef4caa39dc3b6c9d2ce6bbfae827e1b019fd0429b7c99249d8e36b172d7e575d92575200db8e03c60f3cd5d56e6cc1f5548649eab20e3325c23f153751e3f0d6e2ad78934101e6642aad15e94dd3774dc54443c0183a7a88bdfeaafab0f2e663a9d7f83349f59f36b30a5554d68435937; csrf_session_id=f11777b58b6dcf82577151417ffcbbd0; d_ticket=022b83726fbf80fb9cd7d5191a9823fe2c872; passport_assist_user=CkDEWVOF179aVIAGRAW2A83XibZk5EYODMGOzz3Ho53uM9A80A_M7NZ9yWCf_EE0bvsSnlMEWIRzzhqYx34fe4tmGkoKPClRHagojLTknfPsmymtezBkmqzw1l5EgQvD-2ke7pyWSqTY5bXVhfdwNPxVNzE3HzM-EQZCg-oIpPNoVhCklOENGImv1lQgASIBA04h0RI%3D; n_mh=HzlioHjI5I9wntqCGtTd39Tm1rnlRMsWJKsz04of4C4; sso_uid_tt=52949f0eb18f79a00d72b6425a040c41; sso_uid_tt_ss=52949f0eb18f79a00d72b6425a040c41; sid_ucp_sso_v1=1.0.0-KDdmZDNhMWJhNzNiMjEyMDgwNjllOTY4M2I4OTFmOGQ5M2I3OTkwNjEKIQi-q5Gb0_XFARCRnca5BhjaFiAMMOvuzPYFOAZA9AdIBhoCbHEiIGMxYmY3Y2VkODcxNmI0NTRkN2NkZDY4MzViNjJiYjA5; ssid_ucp_sso_v1=1.0.0-KDdmZDNhMWJhNzNiMjEyMDgwNjllOTY4M2I4OTFmOGQ5M2I3OTkwNjEKIQi-q5Gb0_XFARCRnca5BhjaFiAMMOvuzPYFOAZA9AdIBhoCbHEiIGMxYmY3Y2VkODcxNmI0NTRkN2NkZDY4MzViNjJiYjA5; passport_auth_status=c19efb2f2f7ec5e0f53f7cec1902a778%2C; passport_auth_status_ss=c19efb2f2f7ec5e0f53f7cec1902a778%2C; uid_tt=975086b1e0d4d72102154d28c95db1b5; uid_tt_ss=975086b1e0d4d72102154d28c95db1b5; sid_tt=fd80251e8bbfbe5d4fb376607eef662f; sessionid=fd80251e8bbfbe5d4fb376607eef662f; sessionid_ss=fd80251e8bbfbe5d4fb376607eef662f; ttwid=1%7CyJfKHeC4wV5DL5QRCPuoX42dNh1l6qv-0TKJ4cgBPrM%7C1731301011%7Ca28e180e7b1f6df14a3a2f74877a931b5c6a76795c12f057b33338861e22f20a; _bd_ticket_crypt_cookie=2eb23f10ae2721b53b2547cd95c03730; sid_guard=fd80251e8bbfbe5d4fb376607eef662f%7C1731301013%7C5183999%7CFri%2C+10-Jan-2025+04%3A56%3A52+GMT; sid_ucp_v1=1.0.0-KGYyYmNkYTIwMzA1NTM4MWEwMGRmMjUyZjliNWM1ZWE1NDE5ZWU5OTIKGwi-q5Gb0_XFARCVnca5BhjaFiAMOAZA9AdIBBoCbGYiIGZkODAyNTFlOGJiZmJlNWQ0ZmIzNzY2MDdlZWY2NjJm; ssid_ucp_v1=1.0.0-KGYyYmNkYTIwMzA1NTM4MWEwMGRmMjUyZjliNWM1ZWE1NDE5ZWU5OTIKGwi-q5Gb0_XFARCVnca5BhjaFiAMOAZA9AdIBBoCbGYiIGZkODAyNTFlOGJiZmJlNWQ0ZmIzNzY2MDdlZWY2NjJm; SelfTabRedDotControl=%5B%5D; is_dash_user=1; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; WallpaperGuide=%7B%22showTime%22%3A0%2C%22closeTime%22%3A0%2C%22showCount%22%3A0%2C%22cursor1%22%3A10%2C%22cursor2%22%3A2%7D; pwa2=%220%7C0%7C3%7C0%22; strategyABtestKey=%221732015861.739%22; biz_trace_id=06610736; XIGUA_PARAMS_INFO=%7B%7D; __ac_signature=_02B4Z6wo00f01jXc6awAAIDD2.ktUW0jTxI17O0AAOpZHyUXk6aHFG88E8gFja1J.mdxOq-iWP1Ft2pUA.jzP0cdKVfGWd.3eIwlp9Y4sjHdS7R0t-Ygf7cmWw6p63UyU2MMgc0KtXfwcsG3bb; MONITOR_WEB_ID=ca8e08c7-dd22-4886-886f-770c2ab0f6de; _tea_utm_cache_1243=undefined; __ac_nonce=0673c7f2a00e2879573d2; dy_swidth=1680; dy_sheight=1050; my_rd=2; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA01OKl5u5ghNXMVbMN8NUrSiXX3GJhZ1CL0efgLJHELs%2F1732032000000%2F0%2F0%2F1732018701026%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA01OKl5u5ghNXMVbMN8NUrSiXX3GJhZ1CL0efgLJHELs%2F1732032000000%2F0%2F0%2F1732019301028%22; passport_fe_beating_status=true; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1680%2C%5C%22screen_height%5C%22%3A1050%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A6.8%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCUEN4cnlVUlpDU3dFZC9MSXlvY3YzNTVaS05DNnhHRFBuK3d3ZXd6cy80TzJqWkpHSGd2eGRjemQ0c3FGRVRoV1NMdXhndThVWjh4RU4zNVlKZDhVNG89IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; publish_badge_show_info=%220%2C0%2C0%2C1732018120879%22; odin_tt=98d5fc675333a3b661ddf24b539bf3c2c828efc0590f0f786e5baa56ca4c1f7ac750d68f0475fcc2c6681ffc7b0201d2; IsDouyinActive=false'
            }
            html2 = requests.get(ur,headers=headers)
            # print(html2)  # 链接成功200
            t2=html2.json()
            title=html2.json()['item_list'][0]['desc']
            # print(title)
            video_id=html2.json()['item_list'][0]['video']['play_addr']['uri']
            video_url=f'https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}&ratio=720p&line=0'
            html3=requests.get(video_url,headers=headers)
            #print(html3.url)

            video_response = requests.get(url=video_url, headers=headers)  # 发送下载视频的网络请求
            if video_response.status_code == 200:  # 如果请求成功
                z = os.getcwd()
                temp_path = z + '/抖音视频/'  # 在程序当前文件夹下建立文件夹
                print(f"保存视频文档到{temp_path}")
                if not os.path.exists(temp_path):
                    os.makedirs(temp_path)
                data = video_response.content  # 获取返回的视频二进制数据
                rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                new_title = re.sub(rstr, "_", title)  # 过滤不能作为文件名的字符，替换为下划线
                c = '%s.mp4' % new_title  # 视频文件的命名
                file = open(temp_path + c, 'wb')  # 创建open对象
                file.write(data)  # 写入数据
                file.close()  # 关闭
                print(title+"视频下载成功！")
        else:
            print('请输入正确的分享链接！')

if __name__=="__main__":
    # dl = DouyinDownloader(url="https://www.douyin.com/user/MS4wLjABAAAACIs5MzoOHIuWssmIINOjhxc34XXx9Ym3H2TD3cDbuRBm1cCZwWe0oKWFK9_v0xfw?from_tab_name=main&modal_id=7428940998916443404&relation=2&vid=7417309907449351435")
    # dl.download_video()

    url = """7.15 复制打开抖音，看看【顾顾+的作品】《月亮与六便士》# 月亮与六便士 # 等我攒够了六... https://v.douyin.com/CeinRQb8/ w@S.Yz 11/03 teB:/"""
    dy(url)