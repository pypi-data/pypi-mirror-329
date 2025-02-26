import os
import datetime
import shutil
from .config import DATABASE_LOCATION, DATABASE_DRIVER
from .database import db
from .models.volcano import Volcano
from .models.station import Station
from .models.sds import Sds
from .models.rsam_csv import RsamCSV
from .models.winston_scnl import WinstonSCNL
from .models.mounts import MountsSO2, MountsThermal
from importlib_resources import files


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


def reset(models=None) -> bool | None:
    """Reset database.

    Returns:
        True | None
    """
    if models is None:
        models = [Volcano, Station, Sds, RsamCSV, WinstonSCNL, MountsSO2, MountsThermal]

    if DATABASE_DRIVER == 'sqlite':
        database_location = sqlite(DATABASE_LOCATION)
        if os.path.exists(database_location):
            if not db.is_closed():
                db.close()

            os.remove(database_location)
            db.connect(reuse_if_open=True)
            db.create_tables(models)
            db.close()
            print(f"⌛ Reset database: {database_location}")
            return True

    if DATABASE_DRIVER == 'mysql':
        db.connect(reuse_if_open=True)
        db.drop_tables(models)
        db.create_tables(models)
        db.close()

    Volcano.fill_database()

    return None


def backup(backup_dir: str = None) -> str | None:
    """Backup database before run

    Args:
        backup_dir: directory to back up

    Returns:
        str: backup file location
    """
    if DATABASE_DRIVER == 'sqlite':
        print("Backing up database...")
        source_database = sqlite()
        source_filename = os.path.basename(source_database)

        if backup_dir is None:
            backup_dir = os.path.dirname(source_database)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{source_filename}-{timestamp}.bak"

        backup_database = os.path.join(backup_dir, backup_filename)
        shutil.copy(source_database, backup_database)
        print(f"Backup database saved to: {backup_database}")
        return backup_database

    print('For now, only sqlite backup is supported.')


def copy_env(overwrite: bool = False) -> None:
    """Copy .env.local example to working directory.

    Args:
        overwrite (bool, optional): Whether to overwrite existing files. Defaults to False.

    Returns:
        None
    """
    source_env_file = str(files("magma_database.resources").joinpath(".env.local.example"))
    destination_env_file = os.path.join(os.getcwd(), "env.local.example")

    if os.path.exists(destination_env_file) and not overwrite:
        print(f"{destination_env_file} already exists, skipping. Use overwrite=True to overwrite.")
        return None

    try:
        # Backup existing env file
        local_env = os.path.join(os.getcwd(), ".env.local")
        if os.path.exists(local_env):
            current_datetime = datetime.datetime.now()
            print(f"[{current_datetime}] Backup {local_env} to .env.local.bak")
            shutil.copy(local_env, os.path.join(os.getcwd(), "env.local.bak"))

        os.remove(destination_env_file)
        shutil.copy(source_env_file, destination_env_file)
        current_datetime = datetime.datetime.now()
        print(f"[{current_datetime}] Env file: .env.local.example copied to {destination_env_file}")
        return None
    except PermissionError:
        print("❌ Permission denied.")
        return None
