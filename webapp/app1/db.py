from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()

users = Table('users', metadata,
   Column('id', Integer, primary_key=True),
   Column('name', String(50)),
   Column('fullname', String(50)),
   Column('password', String(12))
)

# metadata.create_all(engine)