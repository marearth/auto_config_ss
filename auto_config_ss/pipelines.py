# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.exporters import JsonItemExporter
import re
from scrapy.exceptions import DropItem

def ipDistrictInfo(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    if res == None:
        return None
    data = load(res)
    return data['country']

def validate_ip(s=''):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True
class JsonItemPipeline:
    def __init__(self):
        self.file = open("sites.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False, indent=4)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
class FilterItemPipeline:
    def process_item(self, item, spider):
        sev = item['server']
        # st = [it < 8 for it in vt_2]
        # if True in st:
        #     raise DropItem("Not a stable and fast site for %s" % item)
        # else:
        #     return item
        if validate_ip(sev):
            if ipDistrictInfo(sev) == 'TW' or (ipDistrictInfo(sev) == None):
                raise DropItem("Not a stable and fast site for %s" % item)
            else:
                return item
        else:
            try:
                import socket
                ip = socket.gethostbyname(sev)
                if ipDistrictInfo(ip) == 'TW' or ipDistrictInfo(ip) == None:
                    raise DropItem("Not a stable and fast site for %s" % item)
                else:
                    return item
            except:
                raise DropItem("Not a avaliable site for %s" % item)








