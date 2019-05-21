# _*_coding:utf-8_*_

import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'test'])
# execute(['scrapy', 'crawl', 'chinanews'])
# execute(['scrapy', 'crawl', 'zhihu'])
# execute(['scrapy', 'crawl', 'sina'])
# execute(['scrapy', 'crawl', 'sina_news_roll'])