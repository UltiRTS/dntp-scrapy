from db import DataManager

dbm = DataManager()

dbm.insert_map('test', 'test.sd7', 'test.sdz', 'testhash')
if dbm.map_exists_by_filename('test.sd7'):
    print('map exists')
