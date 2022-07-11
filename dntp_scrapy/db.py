from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import config

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
        self.session.add(_map)
        self.session.commit()
        self.session.close()
        return self.session.query(Map).filter(Map.map_filename == map_filename).first()
    
    def insert_archive(self, archive_name, archive_filename, archive_hash):
        self.session.add(Archive(archive_name, archive_filename, archive_hash))
        self.session.commit()
        self.session.close()
        return self.session.query(Archive).filter(Archive.archive_filename == archive_filename).first()

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

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    pass