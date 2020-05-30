import requests
from bs4 import BeautifulSoup
import random

def make_html(url):
    return BeautifulSoup(requests.get(url).content, 'lxml')

def book_parser ():
    s =""
    url = 'http://www.loyalbooks.com/Top_100'
    main_link = 'http://www.loyalbooks.com'

    random_link = random.randint(1, 50)
    if (random_link != 1):
        url = url + '/' + str(random_link) + '/'

    make_html(url)
    book = make_html(url).find('table', class_='layout2-blue').find_all('td',
                                                                    class_='layout2-blue')  # получили все книги на странице
    i = random.randint(0, 99)

    while (s == ""):
        if  (len(book) - 1 > i) & (book[i].find('a') != -1):
            book_link = book[i].find('a').get('href')  # первая ссылка
            name = book[i].find('b').text  # нашли название книги
            link = main_link + book_link
            page_book_html = make_html(link)  # перешли на страницу книги
            if len(page_book_html.find_all('table',
                                       class_='book')) > 4:  # проверка на случай если на сайте нет онлайн версии
                author = page_book_html.find('font', class_='book-author').text  # нашли автора
                e_book_link = page_book_html.find_all('table', class_='book')[4].find_all('td', class_='book2')[2].find(
                'a').get('href')
            # нашли ссылку на которой онлайн книга
                page_book_txt = make_html(e_book_link)
                s = name + ' ' + author
                text = page_book_txt.find_all('p')
                for p in text:
                    s = s + p.text
                g = s.encode('utf-8')
                return g
        i = random.randint(0, 99)