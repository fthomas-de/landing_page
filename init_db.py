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


from sqlalchemy import create_engine

engine = create_engine('sqlite:///history.sqlite')

from sqlalchemy.orm import sessionmaker

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

s = session()

for i in xrange(0, 10):
    if len(list(s.query(History).filter(History.hist_id == i))) == 0:
        print "inserting", i
        h = History(hist_id=i, value=-1, dice="dice" + str(i), name="name" + str(i))
        s.add(h)
    else:
        print "existing:", i

s.commit()

print s.query(History).order_by(History.hist_id.desc()).all()
print ''
print list(s.query(History).order_by(History.hist_id.desc()).limit(10).all())[1]
print map(str, list(s.query(History).with_entities(History.name).order_by(History.hist_id.desc()).limit(10).all()))
print list(s.query(History).order_by(History.hist_id.desc()).limit(10).all())[1].name
print list(s.query(History).order_by(History.hist_id.desc()).limit(10).all())[1].value
print list(s.query(History).order_by(History.hist_id.desc()).limit(10).all())[1].dice
print ''
print type([x[0] for x in
            list(s.query(History).with_entities(History.value).order_by(History.hist_id.desc()).limit(10).all())][0])

lst = s.query(History).filter(History.name == 'Flo').filter(History.dice == "d4").with_entities(
            History.value).order_by(History.value.desc()).all()
cc_d4 = lst.count(4) / len(lst)

print lst