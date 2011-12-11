# author: @arthurnn89

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from podcast.items import PodcastItem
import re
from urlparse import urljoin

def collectAllEmail(htmlSource):
    "collects all possible email addresses from a string, but still it can miss some addresses"
    #example: t.s@d.com
    email_pattern = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+")
    return re.findall(email_pattern, htmlSource)


class ItunesSpider(BaseSpider):
    name = "itunes"
    #allowed_domains = ["itunes.apple.com"]
    start_urls = ["http://itunes.apple.com/us/genre/podcasts/id26"]

    def parsePage(self, response):
        hxs = HtmlXPathSelector(response)
        
        item = response.meta['item']
        emails = collectAllEmail(hxs.extract())
        if len(emails) > 0:
            item['email'] = emails[0]
            yield item
           
        extractor = SgmlLinkExtractor(allow_domains=response.url)
        
        for entry in extractor.extract_links(response):
            if entry.url is not None:
                req = Request(entry.url, callback=self.parsePage)
                req.meta['item'] = item
                yield req

    def parsePodcast(self, response):
        hxs = HtmlXPathSelector(response)
        
        try:
            title = hxs.select('//div[contains(@id,"title")]/h1/text()').extract()[0]
        except:
            title = None
        
        try: 
            author = hxs.select('//div[contains(@id,"title")]/h2/text()').extract()[0]
        except:
            author = None
            
        try:
            category = hxs.select('//li[contains(@class,"genre")]/a/text()').extract()[0]
        except:
            category = None
            
        try:
            lang = hxs.select('//li[contains(@class,"language")]/text()').extract()[0]
        except:
            lang = None
        
        try:
            extractor = SgmlLinkExtractor(restrict_xpaths='//a[contains(text(),"Podcast Website")]')
            website = extractor.extract_links(response)[0].url
            
            #website = hxs.select('//a[contains(text(),"Podcast Website")]/@href').extract()[0]
        except:
            website = None
        
        try:
            price = hxs.select('//td[contains(@class,"price")]/span/text()').extract()[0]
        except:
            price = None
        
        item = PodcastItem(title=title,author=author,category=category,lang=lang,website=website,price=price)
        
        if website is not None and len(website) > 0:
            request = Request(website, callback=self.parsePage)
            request.meta['item'] = item
            yield request

    def parseLinks(self, response):
        hxs = HtmlXPathSelector(response)
        arr = hxs.select('//div[contains(@id,"selectedcontent")]//a/@href')
        for url in arr:
            yield Request(url.extract(), callback=self.parsePodcast)
        
        for url in hxs.select('//ul[contains(@class,"list alpha")]/li/a/@href'):
            yield Request(url.extract(), callback=self.parseLinks)

        for url in hxs.select('//ul[contains(@class,"list paginate")]/li/a/@href'):
            yield Request(url.extract(), callback=self.parseLinks)


    def parse(self, response):
        #yield Request('http://itunes.apple.com/us/genre/podcasts-business/id1321', callback=self.parseLinks)
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//a[contains(@class,"top-level-genre")]/@href').extract():
            yield Request(url, callback=self.parseLinks)
