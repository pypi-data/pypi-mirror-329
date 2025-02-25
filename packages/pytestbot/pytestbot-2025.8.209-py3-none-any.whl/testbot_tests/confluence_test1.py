#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from atlassian import Jira
from atlassian import Confluence
from atlassian import Crowd
from atlassian import Bitbucket
from atlassian import ServiceDesk
from atlassian import Xray

if __name__=="__main__":
    jira = Jira(
        url='http://localhost:8080',
        username='admin',
        password='admin')

    confluence = Confluence(
        url='http://localhost:8090',
        username='admin',
        password='admin')

    crowd = Crowd(
        url='http://localhost:4990',
        username='app-name',
        password='app-password'
    )

    bitbucket = Bitbucket(
        url='http://localhost:7990',
        username='admin',
        password='admin')

    service_desk = ServiceDesk(
        url='http://localhost:8080',
        username='admin',
        password='admin')

    xray = Xray(
        url='http://localhost:8080',
        username='admin',
        password='admin')

    # Check page exists
    # type of the page, 'page' or 'blogpost'. Defaults to 'page'
    confluence.page_exists(space, title, type=None)

    # Provide content by type (page, blog, comment)
    confluence.get_page_child_by_type(page_id, type='page', start=None, limit=None, expand=None)

    # Provide content id from search result by title and space
    confluence.get_page_id(space, title)

    # Provide space key from content id
    confluence.get_page_space(page_id)
