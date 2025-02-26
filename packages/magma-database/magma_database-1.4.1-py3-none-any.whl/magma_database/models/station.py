import pandas as pd
from .base import MagmaBaseModel
from .volcano import Volcano
from pandas.errors import EmptyDataError
from playhouse.migrate import *
from typing import Any, Dict, List


class Station(MagmaBaseModel):
    nslc = CharField(index=True, unique=True, max_length=14)
    network = CharField(index=True)
    station = CharField(index=True)
    channel = CharField(index=True)
    location = CharField()
    volcano_code = ForeignKeyField(model=Volcano, field='code', on_delete='SET NULL',
                                   on_update='CASCADE', backref='stations', null=True)
    latitude = DecimalField(max_digits=12, decimal_places=8, null=True)
    longitude = DecimalField(max_digits=12, decimal_places=8, null=True)
    elevation = DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        table_name = 'stations'

    @classmethod
    def to_list(cls, nslc: str = None) -> List[Dict[str, Any]]:
        if nslc is None:
            stations = [dict(station) for station in cls.select().dicts()]
            return stations

        stations = cls.select().where(cls.nslc == nslc.upper())
        stations = [dict(station) for station in stations.dicts()]

        if len(stations) == 0:
            raise EmptyDataError(f"⛔ No data for stations. Check your code parameters.")

        return stations

    @classmethod
    def to_df(cls, nslc: str) -> pd.DataFrame:
        df = pd.DataFrame(cls.to_list(nslc))
        df.set_index('id', inplace=True)
        return df
