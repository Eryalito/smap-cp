import datetime
import json
import time
from typing import List
import pytz
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
                lower = int(pricedict['Hora'].split('-')[0])
                lowerDT = datetime.datetime.strptime(pricedict['Dia'] + ' ' + str(lower), '%d/%m/%Y %H')
                lowerDTLocal = self.getDateLocal().localize(lowerDT, is_dst=None)
                lowerDTUTC = lowerDTLocal.astimezone(pytz.utc)
                prices.append(Price(day=pricedict['Dia'], start=lowerDTUTC.strftime('%Y-%m-%d %H:%M:%S'), length=3600, price=pricedict['PCB']))

        return response.status_code, prices

    def getDateLocal(self):
        return pytz.timezone('CET')

    def getDatetimeOffset(self):
        return 3600  # UTC + 1
