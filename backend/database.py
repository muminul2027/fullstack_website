#server_project
#handle:    _MUMINUL__ISLAM___

from sqlalchemy import create_engine,Column,Integer
from sqlalchemy.orm import declarative_base,sessionmaker

engine=create_engine('sqlite:///test.db',echo=True)

Base=declarative_base()

class info(Base):
    __tablename__='info_table'

    customerID=Column(Integer,primary_key=True)
    orderID=Column(Integer)
    orderPrice=Column(Integer)

Base.metadata.create_all(engine)

create_session=sessionmaker(bind=engine)

#creating random data
for x in range(1,30,1):
    session=create_session()
    new_row=info(orderID=x*12, orderPrice=x*6)
    session.add(new_row)
    session.commit()
    session.close()
#closed

#search operation

#closed