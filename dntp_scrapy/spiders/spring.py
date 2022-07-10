import scrapy
import json
from ..items import DntpScrapyItem

class SpringSpider(scrapy.Spider):
    name = 'spring'
    allowed_domains = ['springfiles.springrts.com']
    start_urls = ['http://springfiles.springrts.com/']
    targetUrl = 'https://springfiles.springrts.com/json.php?nosensitive=on&images=on&category=*map*&tags=**&limit=99999999999'

    def start_requests(self):
        return [scrapy.Request(self.targetUrl, callback=self.parse_map_json)]
    
    def parse_map_json(self, response):
        text = response.text
        maps = json.loads(text)
        for map in maps:
            item = DntpScrapyItem()
            item['map_name'] = map['name']
            item['map_url'] = map['mirrors'][0]
            item['map_filename'] = map['filename']
            yield item

    def parse(self, response):
        pass
