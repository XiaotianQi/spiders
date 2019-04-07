# -*- coding: utf-8 -*-
import requests
import json
import asyncio
from scrapy.selector import Selector
from random import choice

async def get_ip():
    # 获取ip,并存入json
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    res = requests.get('https://www.xicidaili.com/nn/', headers=headers)
    selector = Selector(res)
    all_trs = selector.css('#ip_list tr')
    ip_list = []
    for tr in all_trs[1:]:
        all_text = tr.css('td::text').extract()
        ip = all_text[0]
        port = all_text[1]
        proxy_type = all_text[5]
        speed = tr.css('.bar::attr(title)').extract()[0]
        if speed:
            speed = float(speed.split("秒")[0])
        if speed < 2:
            verify = await verify_ip(ip, port, proxy_type)
            if verify:
                ip_list.append((ip, port, proxy_type, speed))
    with open(r'tools/ips.json', 'w') as f:
        json.dump(ip_list, f)

async def verify_ip(ip, port, proxy_type):
    # 验证ip是否可用
    http_url = 'https://www.baidu.com/'
    proxy_url = '{}://{}:{}'.format(proxy_type, ip, port)
    try:
        proxies = {
            proxy_type: proxy_url,
        }
        print('START:', proxies)
        response = requests.get(http_url, proxies=proxies)
    except Exception as e:
        print("invalid ip and port")
        return False
    else:
        code = response.status_code
        if code >= 200 and code < 300:
            print("effective ip")
            return True
        else:
            print("invalid ip and port")
            return False

def get_random_ip(afresh=False):
    if afresh:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_ip())
        loop.close
    with open(r'tools/ips.json', 'r') as f:
        ips = json.load(f)
    return choice(ips)

if __name__ == "__main__":
    print(get_random_ip())
    