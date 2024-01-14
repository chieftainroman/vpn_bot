from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String ,select
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs,async_sessionmaker,create_async_engine
from sqlalchemy.exc import SQLAlchemyError
engine = create_async_engine('sqlite+aiosqlite:///vpn.db', echo = True)
meta = MetaData()
Model = declarative_base(name=__name__)
Session = async_sessionmaker(bind=engine)
session = Session()



class ConfigInbound(Model):
    __tablename__ = "ConfigInbound"

    column_id = Column(Integer,primary_key=True)
    id = Column(String) 
    url = Column(String) 
    port = Column(String)
    transmission = Column(String)
    security = Column(String)
    public_key = Column(String)
    private_key = Column(String)
    fingerprint = Column(String)
    server_name = Column(String)
    short_id = Column(String)
    remark = Column(String)
    
class ConfigClient(Model):
    __tablename__ = "ConfigClient"

    column_id = Column(Integer,primary_key=True)
    id = Column(String) 
    url = Column(String) 
    sub_id = Column(String) 
    expire_time = Column(Integer)
    flow = Column(String)
    email = Column(String)
    inbound_id = Column(Integer)
    
    

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

