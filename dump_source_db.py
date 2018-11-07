from sqlalchemy import create_engine, MetaData
from config import SOURCE_DB_URI
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from target_db_setup import NewOrders, destination_session


Base = automap_base()
source_engine = create_engine(SOURCE_DB_URI)
Base.prepare(source_engine, reflect=True)
Orders = Base.classes.orders
source_session = Session(source_engine)

def push_to_db():
    orders = source_session.query(Orders)
    for order in orders:
        target_order = NewOrders(
            order.id, order.created, order.status,
            order.confirmed, order.contact_phone,
            order.contact_email, order.contact_name,
            order.price, order.comment
        )
        destination_session.add(target_order)
        destination_session.commit()


if __name__ == '__main__':
    push_to_db()
