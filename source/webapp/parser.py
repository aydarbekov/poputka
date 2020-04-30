import os
import requests
from bs4 import BeautifulSoup
import json
from django.core.files import File
from main.settings import BASE_DIR

# функция цикла для каждого дива статьи, принимает список дивов, посл публикацию и текст для отправки
# Достаем атрибут href из ссылки в заголовке и если он является последней старой записью то останавливаем цикл и
# зря не переходит по старым и экономим время


def parse_and_send(divs, last_publication, string):
    for div in divs:
        if div.h2.a.get('href') == last_publication:
            break
        title = div.h2.a.get_text()  # берем заголовок из h1
        data = {  # формируем данные для отправки и посылаем пост запрос
            "notification": {
                "title": "У вас новое уведомление в разделе «{}»".format(string),
                "body": title,
                "image": "https://firebasestorage.googleapis.com/v0/b/abiturient-master.appspot.com/o/Logo-black-64.png?alt=media&token=b8e0ec25-a1ce-4d63-8b2e-3731e1c13349"
            },
            "condition": "!('topic' in topics)"
        }
        headers = {
            "Content-Type": 'application/json',
            "Authorization": 'key=AAAABtVeTA4:APA91bFZheRnDp1OEV3hzzVcn7rrRDBqyPgfcq0ElpPnaPEct-A5rwu8Nn5YiUfHV6KbpwMTRTa_fthshkFyq9FsJNvsPck0yNyy9I1ZHiSp_fxeyZs8OXLUAeLAjrtoboQZ-plsLKsc'
        }
        r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)


def parsing_new_posts():               # запихнули осноную логику в функцию для периодического вызова
    print('start parsing')
    url_announcements = 'http://ed.kyrg.info/category/announcements/'   # Обьявили начальный юрл объявлений
    url_news = 'http://ed.kyrg.info/category/news-events/'              # Объявили начальный юрл новостей

    with open(os.path.join(BASE_DIR, 'parser_last_publications.json')) as f:    # Открываем json файл где храним последние обьявления и новости
        templates = json.load(f)                        # Вытаскиваем оттуда данные
    last_link = templates['last_link']                  # Объявляем последнее обьявление'http://ed.kyrg.info/uchastie-v-olimpiade-sibupk-yarkaya-zhizn-2020/'
    last_link_news = templates['last_link_news']        # Объявляем последнюю новость 'http://ed.kyrg.info/nasha-pamyat/'

    html = requests.get(url_announcements)  # Заходим на объявления и сохраняем результат
    html_news = requests.get(url_news)      # Заходим на новости и сохраняем результат

    bs_html = BeautifulSoup(html.text, "html.parser")               # Оборачиваем в элемент БС
    bs_html_news = BeautifulSoup(html_news.text, "html.parser")     # Оборачиваем в элемент БС

    div_list = bs_html.findAll("div", {"class": "post_div"})                # Методом файнд ол находим все div'ы с классом post_div - это див статьи
    div_list_news = bs_html_news.findAll("div", {"class": "post_div"})      # Методом файнд ол находим все div'ы с классом post_div - это див статьи

    parse_and_send(div_list, last_link, 'О важном')             # запускаем функцию парса и отпраки с дивами обьявлений, последним обьявлением и текстом
    parse_and_send(div_list_news, last_link_news, 'Новости')    # запускаем функцию парса и отпраки с дивами новостей, последней новостью и текстом

    last = bs_html.find("div", {"class": "post_div"}).find('a').get('href')             # С сайта берем посл обьявление
    last_news = bs_html_news.find("div", {"class": "post_div"}).find('a').get('href')   # С сайта берем посл новость

    if last != last_link or last_news != last_link_news:
        json_link = {'last_link': last, 'last_link_news': last_news}    # формируем словать для сохранения в json

        print('saving to file')
        with open(os.path.join(BASE_DIR, 'parser_last_publications.json'), 'w') as f:    # открываем документ
            myfile = File(f)                                                             # так надо оказывается)
            json_string = json.dumps(json_link, indent=2)                                # создаем json строку
            myfile.write(json_string)                                                    # записываем в файл
