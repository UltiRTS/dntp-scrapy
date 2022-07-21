from db import DataManager

dbm = DataManager()

dbm.insert_map('test', 'test.sd7', 'test.sdz', 'testhash')
if dbm.map_exists_by_filename('test.sd7'):
    print('map exists')

ids = dbm.get_maps_ids()
print(ids)
_map = dbm.get_map(ids[0][0])
print(_map.map_filename)
