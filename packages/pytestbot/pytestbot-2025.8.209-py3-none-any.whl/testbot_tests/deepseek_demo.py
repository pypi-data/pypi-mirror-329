#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


if __name__ == "__main__":
    from openai import OpenAI

    client = OpenAI(
        api_key="sk-e6e708c03ad648089fb9b9b9a86d0a31",
        base_url="https://api.deepseek.com/beta",
    )

    response = client.completions.create(
        model="deepseek-chat",
        prompt="def fib(a):",
        suffix="    return fib(a-1) + fib(a-2)",
        max_tokens=128
    )
    print(response.choices[0].text)
