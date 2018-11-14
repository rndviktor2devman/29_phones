from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, String, Integer, Unicode, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from config import DESTINATION_DB_URI


engine = create_engine(DESTINATION_DB_URI)
destination_session = Session(engine)
Base = declarative_base()


class FormattedOrders(Base):
    __tablename__ = 'formatted_orders'
    order_id = Column(Integer, primary_key=True)
    contact_phone = Column(Unicode(255))
    clean_number = Column(Numeric(15, 0), nullable=True)

    def __init__(self, order_id, contact_phone):
        self.order_id = order_id
        self.contact_phone = contact_phone


if __name__ == "__main__":
    Base.metadata.create_all(engine)
