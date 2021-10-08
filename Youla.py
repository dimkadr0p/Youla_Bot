import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time


class Bot():
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaBrowser/21.6.4.786 Yowser/2.5 Safari/537.36'
        })
        self.host = 'https://api.youla.io/api/v1/services-request/'
        self.host2 = '/create-response'
        self.HOST = 'https://youla.ru'
        self.lists_Name = []
        self.lists_Price = []
        self.lists_link = []
        self.list_id = []
        with open('Dmitry.json') as f:
           self.session.cookies.update(json.load(f))

    def get_pars(self, url):
        self.session.headers.update({
            'Referer': url
        })
        response = self.session.get(url)
        print(response)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('li', class_='product_item')
        for i in range(len(items)):
            Name = items[i].find('div', class_='product_item__title').text
            price = items[i].find('div', class_='product_item__description').text.strip().replace('₽', '')
            link = items[i].find('a').get('href')
            id = [x['data-id'] for x in items]
            self.lists_link.append(self.HOST + link)
            self.lists_Name.append(Name)
            self.lists_Price.append(price)
            self.list_id = id
        return self.lists_Name, self.lists_Price, self.lists_link, self.list_id

    def write_excel(self):
        df = pd.DataFrame({'Name': self.lists_Name,'Price': self.lists_Price,'id': self.list_id,'Link': self.lists_link})
        df.to_excel('./files.xlsx',sheet_name='Good',index=False)

    def get_token(self):
        raw = self.session.get("https://youla.ru/web-api/chat/credentials").headers
        self.token = raw["Set-Cookie"].split("; expires")[0].split("youla_auth=")[1]
        return self.token

    def post(self, text):
        data = {
            'comment': text
        }
        self.session.headers.update({
            'Authorization': 'Bearer ' + self.token,
        })
        for i in self.list_id:
            go = self.host + i + self.host2
            time.sleep(5)
            response = self.session.post(go, data=data).json()
            time.sleep(5)
            if response['status'] == 200:
                print(response)


def main():
    try:
        start = Bot()
        url = input('Вставьте ссылку для операций: ')
        print('Выбирите действие для бота: ')
        print('1.Парсинг, 2.Отлик на заказы')
        a = int(input('Напишите цифру: '))
        if a == 1:
            start.get_pars(url)
            start.write_excel()
        if a == 2:
            text = input('Введите текст для рассылки: ')
            while True:
                start.get_pars(url)
                start.get_token()
                start.post(text)
    except UnicodeEncodeError:
        print('Остановка работы программы, так как в задании найден недопустимый для программы символ')
    except:
        print('Что-то пошло не так...')

if __name__ == '__main__':
    main()



