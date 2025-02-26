from .base import MagmaBaseModel
from .station import Station
from pandas.errors import EmptyDataError
from playhouse.migrate import *
from typing import Any, Dict, List


class RsamCSV(MagmaBaseModel):
    # combination between nslc, sampling and filter
    # ex: VG.LEKR.00.EHZ_2021-10-23_10min_5.0_18.0
    key = CharField(unique=True, index=True)
    nslc = ForeignKeyField(Station, field='nslc', backref='rsam_csvs')
    date = DateField(index=True)
    resample = CharField()
    freq_min = DecimalField(max_digits=10, decimal_places=4, null=True)
    freq_max = DecimalField(max_digits=10, decimal_places=4, null=True)
    file_location = CharField()

    class Meta:
        table_name = 'rsam_csvs'

    @classmethod
    def to_list(cls, nslc: str = None) -> List[Dict[str, Any]]:
        if nslc is None:
            stations = [dict(station) for station in cls.select().dicts()]
            return stations

        rsams = cls.select().where(cls.nslc == nslc.upper())
        rsams = [dict(rsam) for rsam in rsams.dicts()]

        if len(rsams) == 0:
            raise EmptyDataError(f"⛔ No data for RSAM. Check your code parameters.")

        return rsams
