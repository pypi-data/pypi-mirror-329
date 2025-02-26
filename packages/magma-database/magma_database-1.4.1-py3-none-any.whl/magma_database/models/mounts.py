import pandas as pd
from .base import MagmaBaseModel
from .volcano import Volcano
from pandas.errors import EmptyDataError
from playhouse.migrate import *
from typing import Any, Dict, List


class MountsSO2(MagmaBaseModel):
    volcano_code = ForeignKeyField(model=Volcano, field='code', on_delete='SET NULL',
                                   on_update='CASCADE', backref='stations', null=True)
    datetime = DateTimeField(index=True, unique=True)
    value = DecimalField(max_digits=12, decimal_places=4)
    image = CharField(null=True)
    downloaded_at = DateTimeField(null=True)

    class Meta:
        table_name = 'mounts_so2'

    @staticmethod
    def to_list(code: str = None) -> List[Dict[str, Any]]:
        if code is None:
            mounts = [dict(mount) for mount in MountsSO2.select().dicts()]
            return mounts

        mounts = MountsSO2.select().where(MountsSO2.volcano_code == code.upper())
        mounts = [dict(mount) for mount in mounts.dicts()]

        if len(mounts) == 0:
            raise EmptyDataError(f"⛔ No data for mounts_so2. Check your code parameters.")

        return mounts

    @staticmethod
    def to_df(code: str = None) -> pd.DataFrame:
        df = pd.DataFrame(MountsSO2.to_list(code=code))
        df.set_index('id', inplace=True)
        return df


class MountsThermal(MagmaBaseModel):
    volcano_code = ForeignKeyField(model=Volcano, field='code', on_delete='SET NULL',
                                   on_update='CASCADE', backref='stations', null=True)
    datetime = DateTimeField(index=True, unique=True)
    value = DecimalField(max_digits=12, decimal_places=4)
    image = CharField(null=True)
    downloaded_at = DateTimeField(null=True)

    class Meta:
        table_name = 'mounts_thermal'

    @staticmethod
    def to_list(code: str = None) -> List[Dict[str, Any]]:
        if code is None:
            mounts = [dict(mount) for mount in MountsThermal.select().dicts()]
            return mounts

        mounts = MountsThermal.select().where(MountsThermal.volcano_code == code.upper())
        mounts = [dict(mount) for mount in mounts.dicts()]

        if len(mounts) == 0:
            raise EmptyDataError(f"⛔ No data for mounts_so2. Check your code parameters.")

        return mounts

    @staticmethod
    def to_df(code: str = None) -> pd.DataFrame:
        df = pd.DataFrame(MountsThermal.to_list(code=code))
        df.set_index('id', inplace=True)
        return df
