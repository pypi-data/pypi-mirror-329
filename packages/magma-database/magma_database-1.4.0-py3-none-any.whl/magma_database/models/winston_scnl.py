import pandas as pd
import datetime
from .station import Station
from ..config import config
from ..database import db
from ..resources import channels_df
from playhouse.migrate import *


WINSTON_MENU_URL = f"http://{config['WINSTON_URL']}:{config['WINSTON_PORT']}/menu"


class WinstonSCNL(Station):
    pin = IntegerField(index=True, unique=True)
    earliest = DateTimeField(index=True)
    latest = DateTimeField(index=True)
    type = CharField(index=True, max_length=2)

    class Meta:
        table_name = 'winston_scnl'

    @staticmethod
    def fill_database(from_server: bool = False) -> None:
        """Fill winston_scnl table with data from Winston endpoint URL.
        
        Args:
            from_server (bool, optional): Whether to fill the database from server. Defaults to False.

        Returns:
            None
        """
        df = channels_df
        json = df.to_dict(orient='records')

        try:
            db.create_tables([WinstonSCNL])
            WinstonSCNL.insert_many(json).execute()
            db.close()
            print('✅ Winston SCNL database inserted successfully.')
        except Exception as e:
            print(f'❌ Winston SCNL database insert error: {e}')
            print(json)

    @staticmethod
    def update_database(winston_url_menu: str = None) -> None:
        if winston_url_menu is None:
            winston_url_menu = WINSTON_MENU_URL

        db.create_tables([WinstonSCNL])

        columns = {
            "Pin": "pin",
            "S ▴": "station",
            "C": "channel",
            "N": "network",
            "L": "location",
            "Earliest": "earliest",
            "Most Recent": "latest",
            "Type": "type"
        }

        try:
            df = pd.read_html(winston_url_menu)[0]

            # Renaming columns readable
            df.rename(columns=columns, inplace=True)

            # Fix location column value
            df['location'] = '00'

            # Add nslc column
            df['nslc'] = df.apply(lambda row: f"{row['network']}.{row['station']}.{row['location']}.{row['channel']}", axis=1)
            json = df.to_dict(orient='records')

            # Insert to database
            for winston in json:
                _winston, created = WinstonSCNL.get_or_create(
                    nslc=winston['nslc'],
                    latest=winston['latest'],
                    defaults={
                        'network': winston['network'],
                        'station': winston['station'],
                        'channel': winston['channel'],
                        'location': winston['location'],
                        'pin': winston['pin'],
                        'earliest': winston['earliest'],
                        'type': winston['type'],
                    }
                )

                if created is True:
                    continue

                _winston.nslc = winston['nslc']
                _winston.network = winston['network']
                _winston.station = winston['station']
                _winston.location = winston['location']
                _winston.channel = winston['channel']
                _winston.pin = winston['pin']
                _winston.earliest = winston['earliest']
                _winston.latest = winston['latest']
                _winston.type = winston['type']
                _winston.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
                _winston.save()

        except Exception as e:
            print(f"⚠️ Cannot connect to Winston server. {e}")
