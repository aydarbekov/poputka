import requests                     # Импортируем реквестс с помощью которого отправляем запросы
from bs4 import BeautifulSoup       # Импортируем БС для работы с html тегами
from rest_framework.utils import json

url_announcements = 'http://ed.kyrg.info/category/announcements/'  # Обьявили начальный юрл
url_news = 'http://ed.kyrg.info/category/news-events/'
last_link = ['http://ed.kyrg.info/priglashaem-na-videokonferencziyu-s-predstavitelem-irkutskogo-naczionalnogo-issledovatelskogo-tehnicheskogo-universiteta/']  # Начальная ссылка последней записи
last_link_news = ['http://ed.kyrg.info/osnovnye-voprosy-testov-ort/']


def parsing_new_posts():
    # Заходим на сайт и сохраняем результат
    html = requests.get(url_announcements)
    html_news = requests.get(url_news)

    # Оборачиваем в элемент БС
    bs_html = BeautifulSoup(html.text, "html.parser")
    bs_htmls_news = BeautifulSoup(html_news.text, "html.parser")
    # Методом файнд ол находим все div'ы с классом post_div - это див статьи
    div_list = bs_html.findAll("div", {"class": "post_div"})
    div_list_news = bs_htmls_news.findAll("div", {"class": "post_div"})
    # цикл для каждого дива статьи
    for div in div_list:
        # Достаем атрибут href из ссылки в заголовке и если он является последней старой записью то останавливаем цикл
        # сначала идут новые и когда подходит к последней старой записанной то
        # останавливает и зря не переходит по старым и экономим время
        if div.h2.a.get('href') in last_link:
            break
        # Берем часть текста
        text = div.p.get_text()
        # переходим по ссылке поста для детейл вью
        page = requests.get(div.h2.a.get('href'))
        # оборачиваем результат в БС
        bs_page = BeautifulSoup(page.text, "html.parser")
        # берем заголовок из h1
        title = bs_page.find('h1').get_text()
        # Берем дату и обрезаем пробелы
        date = bs_page.find('div', {'class': 'entry-meta'}).get_text().strip()
        # Пробуем из контента вытащить фото
        try:
            img = bs_page.find('div', {'class': 'entry-content'}).find('img')['src']
        # Если нет фото то фото = None
        except:
            img = None
        # Собираем данные
        # data = {
        #     'title': title,
        #     'link': div.h2.a.get('href'),
        #     'excerpt': text,
        #     'date': date,
        #     'image': img,
        #     'type': 'announcements'
        # }
        data = {
            "notification": {
                "title": "У вас новое уведомление в разделе «О важном»",
                "body": title
            },
            "condition": "!('topic' in topics)"
        }
        headers = {
            "Content-Type": 'application/json',
            "Authorization": 'key=AAAAC4Z_o20:APA91bHKy4VSdLvB1yJQU6CVeVbe81zLzn6WPkN-SuFfnojzGDoBj3sURlyGbzQSgT0x3-JaEVV1t4TFMdFRK33aYuvuGK7b-k2GlX-Mk1xXlRiXeaMdRDMO6vFOSFiudrcIViehBt7Q'
        }
        r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)
    for div in div_list_news:
        # Достаем атрибут href из ссылки в заголовке и если он является последней старой записью то останавливаем цикл
        # сначала идут новые и когда подходит к последней старой записанной то
        # останавливает и зря не переходит по старым и экономим время
        if div.h2.a.get('href') in last_link:
            break
        # Берем часть текста
        text = div.p.get_text()
        # переходим по ссылке поста для детейл вью
        page = requests.get(div.h2.a.get('href'))
        # оборачиваем результат в БС
        bs_page = BeautifulSoup(page.text, "html.parser")
        # берем заголовок из h1
        title = bs_page.find('h1').get_text()
        # Берем дату и обрезаем пробелы
        date = bs_page.find('div', {'class': 'entry-meta'}).get_text().strip()
        # Пробуем из контента вытащить фото
        try:
            img = bs_page.find('div', {'class': 'entry-content'}).find('img')['src']
        # Если нет фото то фото = None
        except:
            img = None
        # Собираем данные
        # data = {
        #     'title': title,
        #     'link': div.h2.a.get('href'),
        #     'excerpt': text,
        #     'date': date,
        #     'image': img,
        #     'type': 'announcements'
        # }
        data = {
            "notification": {
                "title": "У вас новое уведомление в разделе «Новости»",
                "body": title
            },
            "condition": "!('topic' in topics)"
        }
        headers = {
            "Content-Type": 'application/json',
            "Authorization": 'key=AAAAC4Z_o20:APA91bHKy4VSdLvB1yJQU6CVeVbe81zLzn6WPkN-SuFfnojzGDoBj3sURlyGbzQSgT0x3-JaEVV1t4TFMdFRK33aYuvuGK7b-k2GlX-Mk1xXlRiXeaMdRDMO6vFOSFiudrcIViehBt7Q'
        }
        r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)
    # Находим ссылку последнего поста
    last = bs_html.find("div", {"class": "post_div"}).find('a').get('href')
    last_news = bs_htmls_news.find("div", {"class": "post_div"}).find('a').get('href')
    # Очищаем список последнего поста
    last_link.clear()
    last_link_news.clear()
    # Определяем последний пост
    last_link.append(last)
    last_link_news.append(last_news)

