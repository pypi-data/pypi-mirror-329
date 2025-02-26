import os
from dotenv import dotenv_values

_magma_user_dir: str = os.path.join(os.path.expanduser('~'), '.magma')
os.makedirs(_magma_user_dir, exist_ok=True)

_default_config = {
    'TYPE': 'local',
    'DEBUG': True,
    'DATABASE_DRIVER': 'sqlite',
    'DATABASE_LOCATION': _magma_user_dir,
    'MYSQL_HOST': '127.0.0.1',
    'MYSQL_PORT': 3306,
    'MYSQL_DATABASE': 'seismic',
    'MYSQL_USERNAME': 'homestead',
    'MYSQL_PASSWORD': 'secret',
    'WINSTON_URL': '172.16.1.220',
    'WINSTON_PORT': 16032,
}


def env_local(filename: str = '.env.local') -> str:
    """Local environment variables set in .env.local file.

    Args:
        filename (str, optional): Environment variable name. Defaults to '.env.local'.

    Returns:
        str: Environment location
    """
    _env_local = os.path.join(os.getcwd(), filename)
    return _env_local


def env(filename: str = '.env'):
    """Production environment variables set in .env file.

    Args:
        filename (str, optional): Environment variable name. Defaults to '.env'.

    Returns:
        str: Environment location
    """
    _env = os.path.join(os.getcwd(), filename)
    return _env


config = {
    **_default_config,
    **dotenv_values(env_local()),
    **dotenv_values(env())
}


DATABASE_DRIVER = config['DATABASE_DRIVER']
DATABASE_LOCATION = config['DATABASE_LOCATION']


class Config:
    default = config
    local = dotenv_values(env_local())
    production = dotenv_values(env())

    def __repr__(self):
        return f'{self.__class__.__name__}({self.default})'
