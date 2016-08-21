from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    hist_id = Column(Integer, unique=True)
    name = Column(String(10))
    dice = Column(String(5))
    value = Column(Integer)

    def __repr__(self):
        return "<User(id='%s', name='%s', dice='%s', value='%s')>" % (
                             self.id, self.name, self.dice, self.value)
