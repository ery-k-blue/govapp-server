from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,Text

USER = 'root'
PASSWORD = 'password'
HOST = 'localhost'
DATABASE = 'shugiin_db'
ENCODING = 'utf8'

engine = create_engine("mysql://{}:{}@{}/{}?charset={}".format(USER, PASSWORD, HOST, DATABASE, ENCODING))
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


base = declarative_base()
base.query = session.query_property()

class DIET_MEMBERS(base):
    __tablename__ = 'DIET_MEMBERS'
    MEMBER_ID = Column(Integer, primary_key=True, autoincrement=True)
    KANJI_NAME = Column(Text, unique=False)
    HIRAGANA_NAME = Column(Text, unique=False)
    PARTY_ID = Column(Integer, unique=False)
    CONSTITUECY_ID = Column(Integer, unique=False)
    WON_COUNT = Column(Integer, unique=False)
    PROFILE_URL = Column(Text, unique=False)

    def __init__(self, kanji_name, hiragana_name, party_id, constituecy_id, won_count, profile_url):
        self.KANJI_NAME = kanji_name
        self.HIRAGANA_NAME = hiragana_name
        self.PARTY_ID = party_id
        self.CONSTITUECY_ID = constituecy_id
        self.WON_COUNT = won_count
        self.PROFILE_URL = profile_url

base.metadata.create_all(bind=engine)

session.add(DIET_MEMBERS('橋本', 'はしもと',1,1,10,'google.com'))
session.commit()
