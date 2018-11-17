import time
from phonenumbers import carrier, parse, NumberParseException
from target_db_setup import engine, destination_session
from sqlalchemy import exc, MetaData, Table, Column, Integer, Unicode, Numeric

SLEEP_TIME = 10
metadata = MetaData()
fixed_orders = Table('formatted_orders', metadata,
                     Column('order_id', Integer),
                     Column('contact_phone', Unicode(255)),
                     Column('clean_number', Numeric(15, 0)))


def convert_to_national(phonenumber, country="RU"):
    try:
        clean_number = parse(phonenumber, country)
    except NumberParseException:
        try:
            clean_number = parse('+7{}'.format(phonenumber), country)
        except NumberParseException:
            return None
    return clean_number.national_number


def beautify_numbers(connection):
    transaction = connection.begin()
    target_orders = destination_session.query(fixed_orders). \
        filter(fixed_orders.c.clean_number.is_(None))
    for order in target_orders:
        clean_number = convert_to_national(order.contact_phone)
        inserted_number = fixed_orders.update(). \
            values(clean_number=clean_number). \
            where(fixed_orders.c.order_id == order.order_id)
        connection.execute(inserted_number)
    transaction.commit()


def main_import_cycle():
    connection = engine.connect()
    while True:
        try:
            beautify_numbers(connection)
            print('one shot')
            time.sleep(SLEEP_TIME)
        except exc.DBAPIError as err:
            print('error {}'.format(str(err)))
            if connection.connection_invalidated:
                connection = engine.connect()
        except KeyboardInterrupt:
            break
    connection.close()


if __name__ == "__main__":
    main_import_cycle()
    print("Finish after keyboard interrupt")