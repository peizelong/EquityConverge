import re
import datetime

from crawler.crawler import crawler
from pymongo import MongoClient
import logging





logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO,
                    #filename='test.log',
                    #filemode='a',
                    #encoding='utf-8'
                    )
class app():
    def __init__(self):
        pass
    def run():
        pass
    

#getText('岩山科技','002195')

crawl = crawler()
crawl.run()