import requests
from bs4 import BeautifulSoup
import random
import re

def make_html(url):
    return BeautifulSoup(requests.get(url).content, 'lxml')

def book_parser (size):
    books_num = 99
    book_box =4
    link_box = 2
    s =""
    url = 'http://www.loyalbooks.com/Top_100/'
    main_link = 'http://www.loyalbooks.com'
    max_word_len = 10
    size = size * max_word_len
    make_html(url)
    book = make_html(url).find('table', class_='layout2-blue').find_all('td',
                                                                    class_='layout2-blue')  # получили все книги на странице
    i = random.randint(0,books_num)

    while (s == ""):
        if  (len(book) - 1 > i) & (book[i].find('a') != -1):
            book_link = book[i].find('a')# первая ссылка
            if(book_link != None):
                book_link = book[i].find('a').get('href')
                name = book[i].find('b').text  # нашли название книги
                link = main_link + book_link
                page_book_html = make_html(link)  # перешли на страницу книги
                if len(page_book_html.find_all('table',
                                       class_='book')) >book_box:  # проверка на случай если на сайте нет онлайн версии
                    author = page_book_html.find('font', class_='book-author').text  # нашли автора
                    e_book_link = page_book_html.find_all('table', class_='book')[book_box].find_all('td', class_='book2')[link_box].find(
                    'a').get('href')
            # нашли ссылку на которой онлайн книга
                    page_book_txt = make_html(e_book_link)
                    s = name + ' ' + author
                    text = page_book_txt.find_all('p')
                    for p in text:
                        if (len(s) > size) :
                            break
                        s = s + p.text
                        s = " ".join(re.split("\s+", s, flags=re.UNICODE))
                    return s
        i = random.randint(0, books_num)
