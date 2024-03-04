from sqlalchemy import Column, String, Text, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from api import config

Base = declarative_base()

mysql_username = config.mysql_username
mysql_password = config.mysql_password
mysql_database = config.mysql_database
mysql_port = config.mysql_port

engine = create_engine(
    f'mysql+pymysql://{mysql_username}:{mysql_password}@localhost:{mysql_port}/{mysql_database}?charset=utf8mb4',
    max_overflow=0,
    pool_size=5,
    echo=False
)

Session = sessionmaker(bind=engine)
session = scoped_session(Session)


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    article_date = Column(String(32))
    detail = Column(String(255))


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    password = Column(String(32))


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    blog_title = Column(String(50))
    contact_information1 = Column(String(100))
    contact_information2 = Column(String(100))
    contact_name1 = Column(String(50))
    contact_name2 = Column(String(50))
    blog_icon = Column(String(255))
    index_title = Column(String(50))
    contact_link1 = Column(String(255))
    contact_link2 = Column(String(255))


if __name__ == '__main__':
    Base.metadata.create_all(engine)
