import datetime
import json
import time
from typing import List

import requests
from price import Price


class ReeES:

    DATE_FORMAT = '%Y-%m-%d'
    BASE_URL = 'https://api.esios.ree.es/archives/70/download_json'

    def __init__(self) -> None:
        pass

    def _currentDay(self) -> str:
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime(self.DATE_FORMAT)

    def getDataForDay(self, day: str):
        response = requests.get(url=self.BASE_URL + '?date=' + day)
        if response.status_code != 200:
            return response.status_code, None
        data = json.loads(response.content)
        prices = []
        if 'PVPC' in data:
            pvpc = data['PVPC']
            for pricedict in pvpc:
                if 'Dia' not in pricedict or 'Hora' not in pricedict or 'PCB' not in pricedict:
                    return response.status_code, None
                prices.append(Price(day=pricedict['Dia'], hour=pricedict['Hora'], price=pricedict['PCB']))

        return response.status_code, prices

    def getDatetimeOffset(self):
        return 3600  # UTC + 1
