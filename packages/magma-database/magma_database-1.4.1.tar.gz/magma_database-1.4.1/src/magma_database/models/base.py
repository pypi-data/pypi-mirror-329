import datetime
import pandas as pd
from ..database import db
from playhouse.migrate import *
from typing import Any, Dict, List


class MagmaBaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))

    class Meta:
        database = db

    @classmethod
    def recreate_table(cls, force: bool = False) -> None:
        """Drop and create tables."""
        if (not cls.table_exists()) or (force is True):
            print("Dropping tables...")
            db.drop_tables([cls])
            print("Creating tables...")
            db.create_tables([cls])
        print(f"Table {cls._meta.table_name} already exists. "
              f"Plase use `recreate_tables(force=True)` to recreate tables.")

    @staticmethod
    def fill_database(**kwargs) -> None:
        """Fill database with default values."""
        pass

    @staticmethod
    def to_list(**kwargs) -> List[Dict[str, Any]]:
        """Return field table to list"""
        pass

    @staticmethod
    def to_df(**kwargs) -> pd.DataFrame:
        """Return field table to dataframe"""
        pass

    @staticmethod
    def to_csv(**kwargs) -> bool:
        """Save to CSV file"""
        return False
