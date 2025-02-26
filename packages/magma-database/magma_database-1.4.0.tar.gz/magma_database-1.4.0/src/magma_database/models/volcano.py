import pandas as pd
import numpy as np
from .base import MagmaBaseModel
from ..database import db
from ..resources import volcanoes_df
from pandas.errors import EmptyDataError
from playhouse.migrate import *
from typing import Any, Dict, List


class Volcano(MagmaBaseModel):
    code = CharField(unique=True, max_length=3)
    name = CharField(index=True)
    type = CharField(index=True, max_length=1)
    latitude = DecimalField(max_digits=12, decimal_places=8)
    longitude = DecimalField(max_digits=12, decimal_places=8)
    elevation = DecimalField(null=True)
    time_zone = CharField(default='Asia/Jakarta')
    regional = CharField(index=True)
    is_submarine = BooleanField(default=False)
    causing_tsunami = BooleanField(default=False)
    smithsonian_number = CharField(null=True)

    class Meta:
        table_name = 'volcanoes'

    @staticmethod
    def fill_database() -> None:
        """Fill volcano table with data from database."""
        dict_list = []
        df = volcanoes_df

        df = df.drop(columns=[
            'Code Stasiun',
            'Prioritas Pemantauan',
            'Alias',
            'District',
            'Province ID',
            'Province EN',
            'District',
            'Nearest City',
            'Sering Dikunjungi',
            'Pengelola Kawasan Gunung Api',
            'Link Pengelola',
        ])

        df = df.rename(columns={
            'Tipe': 'type',
            'Code': 'code',
            'Smithsonian Number': 'smithsonian_number',
            'Name': 'name',
            'Time Zone': 'time_zone',
            'Regional': 'regional',
            'Latitude (LU)': 'latitude',
            'Longitude (BT)': 'longitude',
            'Elevation': 'elevation',
            'Bawah Laut': 'is_submarine',
            'Pernah Menyebabkan Tsunami': 'causing_tsunami',
        })

        df['smithsonian_number'] = df['smithsonian_number'].apply(lambda x: f'{x:.0f}')
        df['is_submarine'] = df['is_submarine'].apply(lambda x: True if x == 'Ya' else False)
        df['causing_tsunami'] = df['causing_tsunami'].apply(lambda x: True if x == 'Ya' else False)

        df = df.replace(np.nan, None)

        for _, row in df.iterrows():
            dictionary = {}
            for column in df.columns:
                dictionary[column] = row[column]
                if column == 'smithsonian_number':
                    dictionary[column] = None if row[column] == 'nan' else row[column]
            dict_list.append(dictionary)

        try:
            db.create_tables([Volcano])
            Volcano.insert_many(dict_list).execute()
            db.close()
            print('✅ Volcano database inserted successfully.')
        except Exception as e:
            print(f'❌ Volcano database insert error: {e}')
            print(dict_list)

    @staticmethod
    def to_list(code: str = None) -> List[Dict[str, Any]]:
        """Returns a list of Volcano objects from a Volcano code.

        Args:
            code (str, optional): Volcano code. Defaults to None.

        Returns:
            List[Dict[str, Any]] : A list of Volcano objects.
        """
        if code is None:
            volcanoes = [dict(volcano) for volcano in Volcano.select().dicts()]
            return volcanoes

        volcanoes = Volcano.select().where(Volcano.code == code.upper())
        volcanoes = [dict(volcano) for volcano in volcanoes.dicts()]

        if len(volcanoes) == 0:
            raise EmptyDataError(f"⛔ No data for volcanoes. Check your code parameters.")

        return volcanoes

    @staticmethod
    def to_df(code: str = None) -> pd.DataFrame:
        df = pd.DataFrame(Volcano.to_list(code=code))
        df.set_index('id', inplace=True)
        return df
