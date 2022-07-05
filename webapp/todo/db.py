from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

metadata = MetaData()

class RecordNotFound(Exception):
    """Requested record in database was not found"""


tasks = Table('tasks', metadata,
   Column('id', Integer, primary_key=True),
   Column('title', String(50)),
   Column('description', String(150)),
   Column('done', Boolean())
)

users = Table('users', metadata,
   Column('user_id', Integer, primary_key=True),
   Column('name', String(50)),
   Column('password', String(150)),
   Column('disabled', Boolean())
)

if __name__ == '__main__':
    # table creation
    engine = create_engine('postgresql://web1:web1@localhost:5432/web1')
    metadata.create_all(engine)

