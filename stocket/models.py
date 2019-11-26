# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, String, Boolean, Text
from sqlalchemy.orm import relationship

# database engine and session factory
engine = create_engine('postgresql://sock-user:sock-password@10.6.3.29:15432/sock-db')

DBSession = sessionmaker(bind=engine)

BaseModel = declarative_base()


def init_db():
    print('Init DB ...')
    BaseModel.metadata.create_all(engine)

def drop_db():
    print('Drop DB ...')
    BaseModel.metadata.drop_all(engine)


# metadata = BaseModel.metadata

class TicksData(BaseModel):

    __tablename__ = 'ticks_table'

    id = Column(Integer, primary_key=True)
    time = Column(Text)
    price = Column(Float)
    pchange = Column(Text)
    change = Column(Float)
    volume = Column(Integer)
    amount = Column(Integer)
    type = Column(Text)
    code = Column(Text)
    date = Column(Text)

    def __repr__(self):
        return "<TicksData(code= '%s', date='%s')>" % (self.code, self.date)

class StockList(BaseModel):

    __tablename__ = 'stocks_list'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    code = Column(Text)

    def __repr__(self):
        return "<StockList(code= '%s', name='%s')>" % (self.code, self.name)

class StockHisData(BaseModel):

    __tablename__ = 'stock_his_data'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    code = Column(Text)
    date = Column(Text)
    open = Column(Float)
    high = Column(Float)
    close = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    percentage = Column(Float, default=0)
    ma5 = Column(Float, default=0)

    def __repr__(self):
        return "<StockList(code= '%s', name='%s')>" % (self.code, self.name)


