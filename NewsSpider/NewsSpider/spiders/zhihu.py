# -*- coding: utf-8 -*-
import scrapy
import time
import json
from NewsSpider.settings import BASE_DIR
from NewsSpider.items import ZhihuHotItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=50&desktop=true']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'NewsSpider.middlewares.RandomUserAgentMiddleware': 1,
        },
        'ITEM_PIPELINES':{            
            'NewsSpider.pipelines.MysqlTwistedPipline':1,
        },
        'COOKIES_ENABLED': True,
    }

    def start_requests(self):
        '''
        需要手动启动 chrome
        CMD-CHROME路径:chrome.exe --remote-debugging-port=9222
        '''
        import pickle
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.keys import Keys
        from NewsSpider.settings import BASE_DIR
        
        login_success = False
        try:
            with open(BASE_DIR + r'\cookies\zhihu.cookies', 'rb') as f:
                cookies_dict = pickle.load(f)
            login_success = True
        except:
            pass
        
        if not login_success:
            chrome_option = Options()
            chrome_option.add_argument('--disable-extensions')
            chrome_option.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
            browser = webdriver.Chrome(
                executable_path=BASE_DIR+ r'\cookies\zhihu.cookies',
                chrome_options=chrome_option)
            browser.get('https://www.zhihu.com/signin')
            browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys(Keys.CONTROL + 'a')
            browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys('178xxx')
            browser.find_element_by_css_selector('.SignFlow-password input').send_keys(Keys.CONTROL + 'a')
            browser.find_element_by_css_selector('.SignFlow-password input').send_keys('xxx')
            browser.find_element_by_css_selector('.Button.SignFlow-submitButton').click()
            time.sleep(60)

            cookies_get = browser.get_cookies()
            cookies_dict = {}
            with open(BASE_DIR+ r'\cookies\zhihu.cookies', 'wb') as f:
                for cookie in cookies_get:
                    cookies_dict[cookie['name']] = cookie['value']
                pickle.dump(cookies_dict, f)
            #browser.close()
        yield scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookies_dict)

    def parse(self, response):
        hot_json = json.loads(response.text)
        for hot in hot_json['data']:
            hot_item = ZhihuHotItem()
            hot_item['url'] = hot['target']['link']['url']
            hot_item['title'] = hot['target']['title_area']['text']
            hot_item['content'] = hot['target']['excerpt_area']['text']
            hot_item['hot'] = hot['target']['metrics_area']['text']
            hot_item['answer_count'] = hot['feed_specific']['answer_count']
            yield hot_item

