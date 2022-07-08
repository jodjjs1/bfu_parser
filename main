import requests

# https://abitstat.kantiana.ru/static/rating_bak.json
# https://abitstat.kantiana.ru/api/applicants/get/

def clear_abits(abits):
    clear_data = []
    for i in range(len(abits)-1):
        if abits[i]['Finansirovanie'] == 'Бюджетная основа':
            clear_data.append(abits[i])

    return clear_data

URL = 'https://abitstat.kantiana.ru/static/rating_bak.json'
konkurs = requests.get(URL).json()

URL_ALL = 'https://abitstat.kantiana.ru/api/applicants/get/'
all_abits = requests.get(URL_ALL).json()

my_snils = ''

napravleniya = []

for abit in all_abits:
    if abit['FIO'] == my_snils:
        number_of_napr = abit['Napravlenie'][:8]
        napravleniya.append(number_of_napr)

with open('abit_names.txt', 'w') as f:
    for napr in konkurs:
        napr_name = napr['Napravlenie']
        if napr_name[:8] in napravleniya:
            abits = clear_abits(napr['Abits'])
            for abit in range(len(abits)):
                if abits[abit]['Snils'] == my_snils:
                    abit_mesto = abit + 1
                    print(napr_name, abit_mesto, file=f)
