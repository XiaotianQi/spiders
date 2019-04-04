# _*_coding:utf-8_*_

import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(['scrapy', 'crawl', 'sina'])
execute(['scrapy', 'crawl', 'chinanews'])