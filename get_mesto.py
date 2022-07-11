import requests

# https://abitstat.kantiana.ru/static/rating_bak.json
# https://abitstat.kantiana.ru/api/applicants/get/
class GetMesto():

    def __init__(self, snils:str) -> None:
        self.URL = 'https://abitstat.kantiana.ru/static/rating_bak.json'
        self.konkurs = requests.get(self.URL).json()

        self.URL_ALL = 'https://abitstat.kantiana.ru/api/applicants/get/'
        self.all_abits = requests.get(self.URL_ALL).json()

        self.snils = ''

    def set_snils(self, snils):
        right_snils = ''
        count = 0
        for i in snils:
            count += 1
            if i != '-' and i != ' ':
                right_snils += i
            if count == 3 or count == 6:
                right_snils += '-'
            if count == 9:
                right_snils += ' '
        print(right_snils)

        self.snils = right_snils

    def clear_abits(self, abits):
        clear_data = []
        for i in range(len(abits)-1):
            if abits[i]['Finansirovanie'] == 'Бюджетная основа':
                clear_data.append(abits[i])

        return clear_data

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
            if napr_name[:8] in napravleniya:
                abits = self.clear_abits(napr['Abits'])
                for abit in range(len(abits)):
                    if abits[abit]['Snils'] == self.snils:
                        abit_mesto = abit + 1
                        mesta.append({'napr_id': napr_id, 'napr_name': napr_name, 'abit_mesto': abit_mesto})

        return mesta
