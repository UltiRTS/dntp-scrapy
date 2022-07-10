import os
import scrapy
from ..items import DntpScrapyItem

class ZerokSpider(scrapy.Spider):
    name = 'zerok'
    allowed_domains = ['zero-k.info']
    start_urls = ['http://zero-k.info/Maps']

    targetUrl = 'http://zero-k.info/Maps'
    base = 'http://zero-k.info'
    offset = 40
    offset_step = 40
    stop_page = 41
    formData = {
        "mapSupportLevel": "2",
        "size": "any",
        "sea": "any",
        "hills": "any",
        "elongated": "any",
        "assymetrical": "any",
        "special": "2",
        "isTeams": "Any",
        "is1v1": "any",
        "ffa": "any",
        "chicken": "any",
        "isDownloadable": "1",
        "needsTagging": "false",
        "search": "",
        "offset": str(offset)
    }

    def start_requests(self):
        return [scrapy.Request(self.targetUrl, callback=self.parse_list)]
    
    def parse_list(self, response):
        hrefs = response.css('a::attr(href)').extract()
        hrefs = filter(lambda x: x.startswith('/Maps/'), hrefs)

        for href in hrefs:
            yield scrapy.Request(self.base + href, callback=self.parse)

        self.formData['offset'] = str(self.offset)
        self.offset += self.offset_step
        if(self.offset > self.stop_page):
            return
        yield scrapy.FormRequest(self.targetUrl, formdata=self.formData, callback=self.parse)

    def parse(self, response):
        hrefs = response.css('a::attr(href)').extract()
        map_urls = filter(lambda x: x.endswith('.sd7'), hrefs)
        
        for map_url in map_urls:
            item = DntpScrapyItem()
            item['map_url'] = map_url
            item['map_filename'] = os.path.basename(map_url)
            yield item
