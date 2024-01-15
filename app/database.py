import json

from sqlalchemy import MetaData, Column, Integer, String, Boolean
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

engine = create_async_engine('sqlite+aiosqlite:///vpn.db', echo=True)
meta = MetaData()
Base = declarative_base(name=__name__)
Session = async_sessionmaker(bind=engine)
session = Session()


class ConfigInbound(Base):
    __tablename__ = 'config_inbound'

    id = Column(String, primary_key=True)
    url = Column(String)
    port = Column(Integer)
    transmission = Column(String)
    security = Column(String)
    public_key = Column(String)
    private_key = Column(String)
    fingerprint = Column(String)
    server_name = Column(String)
    short_id = Column(String)
    remark = Column(String)

    def __init__(self, server_url, create_info):
        stream_settings = json.loads(create_info.get('streamSettings'))
        reality_settings = stream_settings.get('realitySettings')

        self.id = create_info.get('id')
        self.url = server_url
        self.port = create_info.get('port')
        self.transmission = stream_settings.get('network')
        self.security = stream_settings.get('security')
        self.public_key = reality_settings.get('settings').get('publicKey')
        self.private_key = reality_settings.get('privateKey')
        self.fingerprint = reality_settings.get('settings').get('fingerprint')
        self.server_name = reality_settings.get('serverNames')[0]
        self.short_id = reality_settings.get('shortIds')[0]
        self.remark = create_info.get('remark')


class ConfigClient(Base):
    __tablename__ = 'config_client'

    id = Column(String, primary_key=True)
    url = Column(String)
    sub_id = Column(String)
    flow = Column(String)
    email = Column(String)
    inbound_id = Column(String)
    active = Column(Boolean)

    def __init__(self, server_url, client_id, sub_id, flow, email, inbound_id):
        self.url = server_url
        self.id = client_id
        self.sub_id = sub_id
        self.flow = flow
        self.email = email
        self.inbound_id = inbound_id
        self.active = True


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
