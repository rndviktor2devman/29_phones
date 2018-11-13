import time
from phonenumbers import carrier, parse, NumberParseException
from target_db_setup import engine, destination_session
from sqlalchemy import exc, MetaData, Table, Column, Integer

SLEEP_TIME = 10
metadata = MetaData()
fixed_orders = Table('fixed_orders', metadata,
                     Column('contact_phone', Integer),
                     Column('clean_number', Integer))


def convert_to_national(phonenumber, country="RU"):
    try:
        clean_number = parse(phonenumber, country)
    except NumberParseException:
        try:
            clean_number = parse(f'+7{phonenumber}', country)
        except NumberParseException:
            return None
    return clean_number.national_number


def beautify_numbers():
    connection = engine.connect()
    try:
        transaction = connection.begin()
        target_orders = destination_session.query(fixed_orders).\
            filter(fixed_orders.c.clean_number.is_(None))
        for order in target_orders:
            clean_number = convert_to_national(order.contact_phone)
            inserted_number = fixed_orders.update().\
                values(clean_number=clean_number).\
                where(fixed_orders.c.contact_phone == order.contact_phone)
            connection.execute(inserted_number)
        transaction.commit()
        connection.close()
    except exc.DBAPIError:
        if connection.connection_invalidated:
            connection = engine.connect()
    time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    while True:
        try:
            beautify_numbers()
        except KeyboardInterrupt:
            print('  Finish after keyboard interrupt')
            break
