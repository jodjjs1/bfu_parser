from importlib.resources import path
import requests
import json
from pathlib import Path
# https://abitstat.kantiana.ru/static/rating_bak.json
# https://abitstat.kantiana.ru/api/applicants/get/

#TODO: место в списка за минусом тех, кто подал согласия на другие специальности
#TODO: моё место среди подавших согласия
#TODO: залить на сервер
#TODO: ссылка на списки бфу по специальности
#TODO: отдельный кеш сервер, где хранятся данные 20м
class Napravleniya():

    def __init__(self):
        try:
            self.__URL = 'https://abitstat.kantiana.ru/static/rating_bak.json'
            self.konkurs = requests.get(self.__URL).json()
            self.__make_cache(self.konkurs, 'konkurs')

            self.__URL_ALL = 'https://abitstat.kantiana.ru/api/applicants/get/'
            self.all_abits = requests.get(self.__URL_ALL).json()
            self.__make_cache(self.all_abits, 'all_abits')

            print('loadin from web')
        except requests.exceptions.ConnectionError:
            self.konkurs = self.__read_cache('konkurs')
            self.all_abits = self.__read_cache('all_abits') # получение данных из файла если нет интернета
            print('loading from cache')

    # ------ SETTERS ------
    def set_snils(self, snils):
        right_snils = ''
        count = 0
        for i in snils:
            if self.__is_int_in_str(i):
                right_snils += i
                count += 1
            if count == 3 or count == 7:
                right_snils += '-'
                count += 1
            if count == 11:
                right_snils += ' '
                count += 1
        
        self.snils = right_snils

    # ------ GETTERS ------
    def get_data(self):
        data = {}
        return data


    def get_mesto(self):

        napravleniya = []
        mesta = []

        for abit in self.all_abits:
            if abit['FIO'] == self.snils:
                number_of_napr = abit['Napravlenie'][:8]
                napravleniya.append(number_of_napr)

        for napr in self.konkurs:
            napr_name = napr['Napravlenie'][8:]
            napr_id = napr['Napravlenie'][:8]
            if napr_id in napravleniya:
                sogl_num = self.__get_sogl_num(napr_id)
                sogl_mesto = self.__get_sogl_mesto(napr_id)

                abits = self.__clear_abits(napr['Abits'])
                for abit in range(len(abits)):
                    if abits[abit]['Snils'] == self.snils:
                        abit_mesto = abit + 1

                        mesta.append({
                            'napr_id': napr_id, 
                            'napr_name': napr_name, 
                            'abit_mesto': abit_mesto, 
                            'sogl_num': sogl_num,
                            'your_sogl': abits[abit]['Soglasie'],
                            'sogl_mesto': sogl_mesto})
        return mesta

    # ---- PRIVAT FUCTIONS ----
    def __get_sogl_mesto(self, napr_id):
        for napr in self.konkurs:
            if napr['Napravlenie'][:8] == napr_id:
                count = 0
                abits = self.__clear_abits(napr['Abits'])
                for abit in range(len(abits)):
                    if abits[abit]['Soglasie']:
                        count += 1
                        if abits[abit]['Snils'] == self.snils:
                            sogl_mesto = count
                            return sogl_mesto
        return -1


    def __get_sogl_num(self, napr_id_fc:str) -> int:
        count = 0
        for napr in self.konkurs:
            napr_id = napr['Napravlenie'][:8]
            if napr_id == napr_id_fc:
                abits = self.__clear_abits(napr['Abits'])
                for abit in abits:
                    if abit['Soglasie']:
                        count += 1
        return count

    def __clear_abits(self, abits) -> list:
            clear_data = []
            for i in range(len(abits)-1):
                if abits[i]['Finansirovanie'] == 'Бюджетная основа':
                    clear_data.append(abits[i])

            return clear_data

    def __is_int_in_str(self, n:str) -> bool:
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if n in numbers:
            return True
        else:
            return False

    def __make_cache(self, data, name:str):
        path = Path('cache', f'{name}.json')
        with open(path, 'w') as cache_file:
            json.dump(data, cache_file)
        

    def __read_cache(self, name:str) -> dict:
        path = Path('cache', f'{name}.json')
        with open(path) as cache_file:
            cache = json.load(cache_file)
        return cache