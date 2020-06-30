
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from auto_config_ss.items import SiteItem
import re
import json

class ConfigSpider(scrapy.Spider):
    name = 'auto_config'

    def start_requests(self):
        urls = ['http://ss.pythonic.life/'] 
        for url in urls:
            yield SeleniumRequest(url=url, 
             callback=self.parse_url,
             wait_time= 10)
    
    def parse_url(self, response):
        #check page and program
        # with open('page.html', 'wb') as html_file:
        #     html_file.write(response.body)

        # s_container = response.css('div.container')[0]
        # s_main = s_container.css('div.main')[0]
        # s_tbss = s_main.xpath('.//table[@id="tbss"]')        
        # for it in s_tbss.xpath('.//tr[@role="row" and (contains(@class,"even") or contains(@class,"odd"))]'):
        #     d_row = it.css('td::text').getall()
        #     site = SiteItem()
        #     vtum = d_row[0]
        #     vt_1 = vtum.split('/').strip()
        #     vt_2 = []
        #     for it in vt_1:
        #         vt_2.append(int(re.sub('\D','',it)))
        #     site['vtum'] = vt_2
        #     site['address'] = d_row[1]
        #     site['port'] = d_row[2]
        #     site['password'] = d_row[3]
        #     site['method'] = d_row[4]
        #     site['time'] = d_row[5]
        #     site['country'] = d_row[6]
        #     yield site
        s_main = response.xpath('//div[@id="content"]/fieldset')[0]
        s_part = s_main.css('ol')[2]
        link_num = s_part.xpath('.//li/a/@href').getall()
        links = [response.request.url+it[1:] for it in link_num]

        for link in links:
            yield SeleniumRequest(url=link, 
             callback=self.parse_link,
             wait_time= 10)
        # yield SeleniumRequest(url=links[0], 
        #     callback=self.parse_link,
        #     wait_time= 10)
     

    def parse_link(self,response):
        s_content = response.xpath('//div[@id="content"]')[0]
        s_json = s_content.xpath('.//div[@id="json"]')[0]
        json_text = s_json.css('textarea::text').get()
        data_json = json.loads(json_text)
        site = SiteItem()
        site['server'] = data_json['server']
        site['server_ipv6'] = data_json['server_ipv6']
        site['server_port'] = data_json['server_port']
        site['local_address'] = data_json['local_address']
        site['local_port'] = data_json['local_port']
        site['password'] = data_json['password']
        site['group'] = data_json['group']
        site['method'] = data_json['method']
        site['obfsparam'] = data_json['obfsparam']
        site['protoparam'] = data_json['protoparam']
        return site
