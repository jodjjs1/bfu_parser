import requests
import json
from pathlib import Path
import time

URL_K = 'https://abitstat.kantiana.ru/static/rating_bak.json'
URL_ALL = 'https://abitstat.kantiana.ru/api/applicants/get/'

def Get_data():
    print('statt caching')
    while True:
        try:
            konkurs = requests.get(URL_K).json()
            all_abits = requests.get(URL_ALL).json()


            path1 = Path('cache','konkurs.json')
            with open(path1, 'w') as cache_file:
                json.dump(konkurs, cache_file)

            path2 = Path('cache','all_abits.json')
            with open(path2, 'w') as cache_file:
                json.dump(all_abits, cache_file)
            print('got all data')
            time.sleep(20 * 60)
            print('wake up')
        except requests.exceptions.ConnectionError:
            print('Bad conection')
            time.sleep(30)