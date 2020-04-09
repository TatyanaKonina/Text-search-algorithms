import requests
from bs4 import BeautifulSoup


def make_html(url):
    return BeautifulSoup(requests.get(url).content, 'lxml')


url = 'http://www.loyalbooks.com/Top_100'
main_link = 'http://www.loyalbooks.com'

make_html(url)
book = make_html(url).find('table', class_='layout2-blue').find_all('td',
                                                                    class_='layout2-blue')  # получили все книги на странице
number_books = int(input())
for i in range(0, number_books):
    if book[i].find('a'):
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
            file_name = name + '.txt'  # записываем в txt файл
            file = open(file_name, "w", encoding='utf-8')
            text = page_book_txt.find_all('p')
            file.write(name + ' ' + author)
            for p in text:
                file.write(p.text)
            file.close()
