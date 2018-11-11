# Microservice for Search Index of Phone Numbers

Main purpose of the project is normalization of phone numbers from source database into national format.
For migration purposes was used `alembic`, for phone numbers normalization was used `phonenumbers`

## Using scenario

* Install all dependencies `pipenv install`
* Modify `alembic.ini` and `config.py` - replace `URI` with your psql options (postgresql://postgres:pass@localhost/dbname)
* Download source db with script `target_db_setup.py`
* Run `alembic upgrade head`
* Run script `beautify_numbers.py` to normalize numbers(fills column `clean_number` with normalized numbers in db)

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
