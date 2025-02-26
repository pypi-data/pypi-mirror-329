import os
from .config import config, DATABASE_DRIVER, DATABASE_LOCATION
from playhouse.migrate import *


def sqlite(db_name: str = 'magma.db') -> str:
    """Database location

    Args:
        db_name: database name. Default magma.db

    Returns:
        str: Database location
    """
    if os.path.isfile(DATABASE_LOCATION):
        return DATABASE_LOCATION

    if not os.path.isdir(DATABASE_LOCATION):
        os.makedirs(DATABASE_LOCATION)
    return os.path.join(DATABASE_LOCATION, db_name)


def database():
    """Database initialization"""
    _db = MySQLDatabase(host=config['MYSQL_HOST'],
                        port=int(config['MYSQL_PORT']),
                        database=config['MYSQL_DATABASE'],
                        user=config['MYSQL_USERNAME'],
                        password=config['MYSQL_PASSWORD'])

    if DATABASE_DRIVER == 'sqlite':
        sqlite_db = sqlite()

        _db = SqliteDatabase(database=sqlite_db, pragmas={
            'foreign_keys': 1,
            'journal_mode': 'wal',
            'cache_size': -32 * 1000
        })

    return _db


def test() -> bool:
    """Test database connection.

    Returns:
        bool: True if database connection is successful, False otherwise.
    """
    db_proxy = DatabaseProxy()
    _db = database()

    try:
        print('🏃‍♂️ Checking database connection...')
        print(f'➡️ Using {DATABASE_DRIVER}')
        db_proxy.initialize(_db)
        _db.connect()
        _db.close()
        print('✅ Database connection successful.')
        return True
    except Exception as e:
        print(f"❌ Cannot connect to database: {e}")
        return False


db = database()
