import datetime
import csv
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def collect_data(city_code='2398'):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }

    cookies = {
        'mg_geo_id': f'{city_code}'
    }

    # создает новый файл index.html

    # response = requests.get(url='https://magnit.ru/promo/', headers=headers, cookies=cookies)
    # with open(f'index.html', 'w', encoding="utf-8") as file:
    #     file.write(response.text)

    with open('index.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    city = soup.find('a', class_='header__contacts-link_city').text.strip()
    cards = soup.find_all('a', class_='card-sale-new__catalogue')

    data = []

    for card in cards:
        card_title = card.find('p', class_='card-sale-new__title').text.strip()

        try:
            card_discount = card.find('div', class_='card-sale-new__progress card-sale-new__progress_red').text.strip()
        except AttributeError:
            continue

        card_price_old_all = card.find('div', class_='card-sale-new__price-old').find_all('span')
        card_price_old_price = f'{card_price_old_all[0].text}.{card_price_old_all[1].text}'

        card_price_new_all = card.find('div',
                                       class_='card-sale-new__price-container card-sale-new__price-current').find_all(
            'span')
        card_price_new_price = f'{card_price_new_all[0].text}.{card_price_new_all[1].text}'

        card_sale_date = card.find('div', class_='card-sale-new__date').text.strip().replace('\n', ' ')

        data.append(
            [card_title, card_discount, card_price_old_price, card_price_new_price, card_sale_date]
        )

    with open(f'{city}_{cur_time}.csv', 'w', encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                'Продукт',
                'Старая цена',
                'Новая цена',
                'Процент скидки',
                'Время акции',
            ]
        )
        writer.writerows(
            data
        )


def main():
    collect_data(city_code='2398')


if __name__ == '__main__':
    main()
