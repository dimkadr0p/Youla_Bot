# - *- coding: utf- 8 - *-
import requests
import json

def auth():

    session = requests.Session()
    link = 'https://youla.ru/web-api/auth/request_code'
    x = input('Введите номер телефона: ')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Referer': 'https://youla.ru/login'
    }

    data = {
        'phone': x
    }

    response = session.post(link, data=data, headers=headers).text
    print(response)

    links = 'https://youla.ru/web-api/auth/login'

    datas = {
        'code': input('Введите код: '),
        'phone': x
    }
    resp = session.post(links, data=datas, headers=headers).text
    print(resp)

    with open('Dmitry.json', 'w') as f:
        json.dump(requests.utils.dict_from_cookiejar(session.cookies), f)

auth()

input('Press ENTER to exit')

