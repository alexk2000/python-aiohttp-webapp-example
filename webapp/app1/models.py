# NOT IN USE

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)


    def __repr__(self):
       return "<User(name='%s', fullname='%s', password='%s')>" % (
                            self.name, self.fullname, self.password)

if __name__ == '__main__':
    engine = create_engine("postgresql://web1:web1@localhost/web1")
    Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    # session.add(ed_user)
    # session.commit()

