import requests                     # Импортируем реквестс с помощью которого отправляем запросы
from bs4 import BeautifulSoup       # Импортируем БС для работы с html тегами

url_announcements = 'http://ed.kyrg.info/category/announcements/'  # Обьявили начальный юрл
last_link = ['http://ed.kyrg.info/vnimanie-vypuskniki-shkol-i-kolledzhej-vy-mozhete-prinyat-uchastie-v-olimpiade-sibupk-yarkaya-zhizn-2020/']  # Начальная ссылка последней записи
new_data = []  # Копим новые данные сюда (Его будем обновлять после отправки данных)


def parsing_new_posts():
    # Заходим на сайт и сохраняем результат
    html = requests.get(url_announcements)
    # Оборачиваем в элемент БС
    bs_html = BeautifulSoup(html.text, "html.parser")
    # Методом файнд ол находим все div'ы с классом post_div - это див статьи
    div_list = bs_html.findAll("div", {"class": "post_div"})
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
        data = {
            'title': title,
            'link': div.h2.a.get('href'),
            'excerpt': text,
            'date': date,
            'image': img,
            'type': 'announcements'
        }
        # Добавляем данные поста в список новых постов
        new_data.append(data)
    # Находим ссылку последнего поста
    last = bs_html.find("div", {"class": "post_div"}).find('a').get('href')
    # Очищаем список последнего поста
    last_link.clear()
    # Определяем последний пост
    last_link.append(last)

