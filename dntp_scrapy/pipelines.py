# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os
import shutil
import config
import requests
from unitSync import UnitSync
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from db import DataManager


# Spring repo index: https://springfiles.springrts.com/json.php?nosensitive=on&images=on&category=*map*&tags=**&limit=99999999999
class DntpScrapyPipeline:
    uSync = UnitSync(os.getcwd(), os.path.join(config.engine_location, 'libunitsync.so'))
    dbm = DataManager()

    def generate_minimap(self, item):
        return self.uSync.storeMinimap(item['map_name']) 
    
    def hash(self, item):
        with open(os.path.join(config.engine_location + '/maps', item['map_filename']), 'rb') as f:
            return hex(hash(f.read()))[2:]

    
    def get_mapname(self):
        return self.uSync.getMapName()
    
    # download map to engine/maps
    def download(self, item):
        resp = requests.get(item['map_url'])
        if resp.status_code == 200:
            with open(os.path.join(config.engine_location + '/maps', item['map_filename']), 'wb') as f:
                f.write(resp.content)

    def process_item(self, item, spider):
        if(self.dbm.map_exists_by_filename(item['map_filename'])):
            return item

        # download into engine/maps
        self.download(item)
        # reinit after downloading a new map
        self.uSync.reinit()
        item['map_hash'] = self.hash(item)
        item['map_name'] = self.get_mapname()

        minimap_path = self.generate_minimap(item)
        item['minimap_filename'] = os.path.basename(minimap_path)

        # move minimap, map files
        shutil.move(minimap_path, os.path.join(config.archive_location + '/maps', item['minimap_filename']))
        shutil.move(os.path.join(config.engine_location + '/maps', item['map_filename']), 
            os.path.join(config.archive_location + '/maps', item['map_filename']))
        
        self.dbm.insert_map(item['map_name'], item['map_filename'],item['minimap_filename'], item['map_hash'])

        return item

if __name__ == '__main__':
    item = {
        'map_filename': 'titanduel_2.2.sd7',
        'map_url': 'http://zero-k.info/content/maps/titanduel_2.2.sd7'
    }

    pipeline = DntpScrapyPipeline()
    pipeline.process_item(item, '')