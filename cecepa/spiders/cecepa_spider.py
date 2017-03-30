#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule 
from scrapy.selector import Selector
from cecepa.items import CecepaItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import Spider


class LogoSpider(CrawlSpider) : #CrawlSpider用来遍布抓取，通过rules来查找所有符合的URL来爬取信息

    name = "cecepa"
    allowed_domains = ["cecepa.com"]
    start_urls = ["http://www.cecepa.com/artkt/index.html"]
    rules = [
        Rule(SgmlLinkExtractor(allow=('/artkt/index\d{,3}.html'))),
        Rule(SgmlLinkExtractor(allow=(r'/artkt/[a-z0-9]+?'), deny=(r'/artkt/all.html')), follow=True, callback="parse_page"),
    ]

    def parse_page(self, response) :
        sel = Selector(response)
        item = CecepaItem()
        item['albumname'] = ''.join(sel.xpath('//div[@class="title"]/h1[@class="clearfix"]/span/a/text()').extract())
        item['imageurl']  = sel.xpath('//div[@class="con"]/div/img/@src').extract()
        return item

