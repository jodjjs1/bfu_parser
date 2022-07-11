import requests

# https://abitstat.kantiana.ru/static/rating_bak.json
# https://abitstat.kantiana.ru/api/applicants/get/
class Napravleniya():

    def __init__(self):
        self.__URL = 'https://abitstat.kantiana.ru/static/rating_bak.json'
        self.konkurs = requests.get(self.__URL).json()

        self.__URL_ALL = 'https://abitstat.kantiana.ru/api/applicants/get/'
        self.all_abits = requests.get(self.__URL_ALL).json()

        self.snils = ''

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
                abits = self.__clear_abits(napr['Abits'])
                for abit in range(len(abits)):
                    if abits[abit]['Snils'] == self.snils:
                        abit_mesto = abit + 1
                        mesta.append({'napr_id': napr_id, 'napr_name': napr_name, 'abit_mesto': abit_mesto})
        return mesta

    # ---- PRIVAT FUCTIONS ----
    def __clear_abits(self, abits):
            clear_data = []
            for i in range(len(abits)-1):
                if abits[i]['Finansirovanie'] == 'Бюджетная основа':
                    clear_data.append(abits[i])

            return clear_data

    def __is_int_in_str(self, n:str):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if n in numbers:
            return True
        else:
            return False
