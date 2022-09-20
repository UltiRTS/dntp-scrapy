from warnings import catch_warnings
from sqlalchemy import create_engine, Column, Integer, String , ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import config
import hashlib

engine = create_engine(f'mysql+pymysql://{config.mysql_username}:{config.mysql_password}@localhost/{config.mysql_dbname}',
    echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class DataManager:
    session = Session()

    def map_exists_by_filename(self, filename):
        return self.session.query(Map).filter(Map.map_filename == filename).first() is not None
    
    def insert_map(self, map_name, map_filename, minimap_filename, map_hash):
        _map = Map(map_name=map_name, map_filename=map_filename, minimap_filename=minimap_filename, map_hash=map_hash)
        try:
            self.session.add(_map)
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()

        return self.session.query(Map).filter(Map.map_filename == map_filename).first()
    
    def get_maps_ids(self):
        return self.session.query(Map.id).all()
    
    def get_map(self, map_id):
        return self.session.query(Map).filter(Map.id == map_id).first()

    def update_map(self, map_id, map_name, map_filename, minimap_filename, map_hash):
        try:
            _map = self.session.query(Map).filter(Map.id == map_id).first()
            _map.map_name = map_name
            _map.map_filename = map_filename
            _map.minimap_filename = minimap_filename
            _map.map_hash = map_hash
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()

        return _map
    
    def insert_archive(self, archive_name, archive_filename, archive_hash):
        self.session.add(Archive(archive_name, archive_filename, archive_hash))
        self.session.commit()
        return self.session.query(Archive).filter(Archive.archive_filename == archive_filename).first()
    
    @staticmethod
    def hash_map(filename):
        m = hashlib.md5()
        with open(filename, 'rb') as f:
            m.update(f.read())
        
        return m.digest().hex()

class Map(Base):
    __tablename__ = 'maps'

    id = Column(Integer, primary_key=True)
    map_name = Column(String(255), unique=True)
    map_filename = Column(String(255), unique=True)
    minimap_filename = Column(String(255))
    map_hash = Column(String(255))

    def __repr__(self) -> str:
        return "<Map(map_name='%s', map_filename='%s', minimap_filename='%s', map_hash='%s')>" \
            % (self.map_name, self.map_filename, self.minimap_filename, self.map_hash)

class Archive(Base):
    __tablename__ = 'archives'

    id = Column(Integer, primary_key=True)
    zip_name = Column(String(255))
    extract_to = Column(String(255))
    zip_hash = Column(String(255))

    def __repr__(self) -> str:
        return "<Archive(zip_name='%s', extract_to='%s', zip_hash='%s')>" \
            % (self.zip_name, self.extract_to, self.zip_hash)

class SystemConfig(Base):
    __tablename__ = 'system_config'

    id = Column(Integer, primary_key=True)
    config_name = Column(String(255))
    engine = Column(Integer, ForeignKey('archives.id'))
    mod = Column(Integer, ForeignKey('archives.id'))
    engine_essentials_hash = Column(String(255))
    mod_essentials_hash = Column(String(255))
    _type = Column(String(255))

    def __repr__(self) -> str:
        return "<SystemConfig(config_name='%s', engine='%s', mod='%s', type='%s')>" \
            % (self.config_name, self.engine, self.mod, self._type)

class LobbyInfo(Base):
    __tablename__ = 'lobby_info'

    id = Column(Integer, primary_key=True)
    version = Column(String(255))
    lobby_hash = Column(String(255))
    lobby_name = Column(String(255))
    _type = Column(String(255))

    def __repr__(self) -> str:
        return "<LobbyInfo(version='%s', lobby_hash='%s', lobby_name='%s', type='%s')>" \
            % (self.version, self.lobby_hash, self.lobby_name, self._type)

class Mod(Base):
    __tablename__ = 'mods'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    archive = Column(Integer, ForeignKey('archives.id'))
    folder_hash = Column(String(255))
    version = Column(String(255))

    def __repr__(self) -> str:
        return "<Mod(name='%s', archive='%d', version='%s')>" \
            % (self.name, self.archive, self.version)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    pass
