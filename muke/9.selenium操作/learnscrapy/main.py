# -*- coding: utf-8 -*-
import os
import sys
from scrapy import cmdline

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# cmdline.execute(['scrapy', 'crawl', 'jobbole'])
# cmdline.execute(['scrapy', 'crawl', 'zhihu'])
cmdline.execute(['scrapy', 'crawl', 'lagou'])