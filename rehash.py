from fileinput import filename
import os
from db import DataManager
from config import engine_location

dbm = DataManager()

ids = dbm.get_maps_ids()

for map_id in ids:
    _map = dbm.get_map(map_id[0])
    map_filename = os.path.join(engine_location + '/maps', _map.map_filename)

    if os.path.exists(map_filename):
        with open(map_filename, 'rb') as f:
            _hash = dbm.hash_map(map_filename)
            _map['map_hash'] = _hash
    
    dbm.update_map(_map)