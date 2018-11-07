from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, String, Integer, Unicode, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from config import DESTINATION_DB_URI


engine = create_engine(DESTINATION_DB_URI)
destination_session = Session(engine)
Base = declarative_base()


class NewOrders(Base):
    __tablename__ = 'fixed_orders'
    orders_id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    status = Column(String)
    confirmed = Column(DateTime)
    contact_phone = Column(Unicode(255))
    clean_number = Column(Numeric(15, 0), nullable=True)
    contact_email = Column(String)
    contact_name = Column(String)
    price = Column(Integer)
    comment = Column(String)

    def __init__(self, orders_id, created, status, confirmed,
                 contact_phone, contact_email, contact_name, price, comment):
        self.orders_id = orders_id
        self.created = created
        self.status = status
        self.confirmed = confirmed
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.contact_name = contact_name
        self.price = price
        self.comment = comment


if __name__ == "__main__":
    Base.metadata.create_all(engine)
