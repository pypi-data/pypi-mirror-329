#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   fetch.py
# @Time    :   2021/04/09 15:59:10
# @Author  :   Jianbin Li
# @Version :   1.0
# @Contact :   jianbin0410@gmail.com
# @Desc    :   None

# here put the import lib
import time
import asyncio
from curl_cffi import requests
from curl_cffi.requests import AsyncSession


def format_proxies(proxies=None):
    """

    :param proxies:
    :return:
    """
    # 格式化代理
    if isinstance(proxies, dict):
        _proxies = proxies

    elif isinstance(proxies, str):
        _proxies = {
            "http": "",
            "https": "",
        }
        for k in _proxies.keys():
            _proxies[k] = proxies if proxies.startswith(
                'http') else f'http://{proxies}'
    else:
        _proxies = None
    return _proxies


def http_fetch(url, method='GET', data=None, headers=None, proxies=None, **kwargs):
    """
    :param url: 要请求的url
    :param method: 请求参数 支持 get/post
    :param data: post请求时的请求body
    :param headers: 请求头
    :param proxies: 代理， 支持使用封装的类型 或者使用固定url, 固定的url格式为  1.2.3.4:8080
    :return: 请求结果
    """
    _method = method.upper()
    if _method not in ('GET', 'POST'):
        return int(time.time()), f'暂不支持 {method} 请求方法', None

    # 格式化请求头
    if not isinstance(headers, dict):
        kwargs['headers'] = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }
    else:
        kwargs['headers'] = headers
    kwargs['proxies'] = format_proxies(proxies)
    if 'verify' not in kwargs:
        kwargs['verify'] = False
    if 'timeout' not in kwargs:
        kwargs['timeout'] = (6.05, 8.05)
    try:
        if _method == 'GET':
            _response = requests.get(url, **kwargs)
        else:
            _response = requests.post(url, data=data, **kwargs)
    except Exception as e:
        return int(time.time()), repr(e), None
    else:
        return int(time.time()), _response.status_code, _response


async def http_fetch_async(url, method='GET', data=None, headers=None, proxies=None, **kwargs):
    """
    :param url: 要请求的url
    :param method: 请求参数 支持 get/post
    :param data: post请求时的请求body
    :param headers: 请求头
    :param proxies: 代理， 支持使用封装的类型 或者使用固定url, 固定的url格式为  1.2.3.4:8080
    :return: 请求结果
    """
    _method = method.upper()
    if _method not in ('GET', 'POST'):
        return int(time.time()), f'暂不支持 {method} 请求方法', None

    # 格式化请求头
    if not isinstance(headers, dict):
        kwargs['headers'] = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }
    else:
        kwargs['headers'] = headers
    kwargs['proxies'] = format_proxies(proxies)
    if 'verify' not in kwargs:
        kwargs['verify'] = False
    if 'timeout' not in kwargs:
        kwargs['timeout'] = (6.05, 8.05)
    try:
        async with AsyncSession() as session:
            _response = await session.request(method, url, data=data, **kwargs)
    except Exception as e:
        return int(time.time()), repr(e), None
    else:
        return int(time.time()), _response.status_code, _response


if __name__ == '__main__':
    async def main():
        response = await http_fetch_async(
            url="https://www.baidu.com",
            method="GET",
        )
        print(response)
    asyncio.run(main())
    response = http_fetch('https://www.baidu.com')
    print(response)
