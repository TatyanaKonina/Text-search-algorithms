import requests
from bs4 import BeautifulSoup
import random
import ctypes as ct
#---------------------path to dll-------------------------------------
path = r"D:\dll\Debug\dll.dll"  # or full path
lib = ct.CDLL(path)
# --------------- define c structs ------------------------------------------
class Text (ct.Structure):
    _fields_ = [("haystack", ct.c_char_p),
                ("haystackSize", ct.c_int),
                ("text_type", ct.c_int)]

class Pattern(ct.Structure):
    _fields_ = [("needle", ct.c_char_p),
                ("needleSize", ct.c_int)]

class SearchRequest (ct.Structure):
    _fields_ = [("Pattern", ct.POINTER(Pattern)),
               ("Text", ct.POINTER(Text))]

class SearchResult (ct.Structure):
    _fields_ = [("matchedShifts", ct.POINTER(ct.c_int)),
                ("numberOfMatches", ct.c_int),
                ("numOfCompares",ct.c_int),
                ("numOfExtraOps",ct.c_int),
                ("memoryWaste",ct.c_int),
                ("workTime",ct.c_double)]

#------------------------------------- define c functions-------------------------------
lib.make_text_storage.argtype = [ct.c_int, ct.c_int, ct.c_char_p, ct.c_char_p, ct.c_int, ct.c_int]
lib.make_text_storage.restype = ct.POINTER(SearchRequest)

lib.make_result_storage.argtype = [ct.POINTER(SearchResult), ct.c_int, ct.c_int]
lib.make_result_storage.restype = ct.POINTER(SearchResult)

lib.make_statictic.argtype = [ct.POINTER(SearchResult), ct.c_int ]
lib.make_statictic.restype = ct.POINTER(SearchResult)

lib.make_parser_storage.argtype = [(ct.c_char_p),ct.c_char_p,ct.c_int,ct.c_int]
lib.make_parser_storage.restype = ct.POINTER(SearchRequest)

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
    i = random.randint(0,50)

    while (s == ""):
        if  (len(book) - 1 > i) & (book[i].find('a') != -1):

            book_link = book[i].find('a').get('href')# первая ссылка
            if(book_link != None):
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
                    return s
        i = random.randint(0, 50)

def example():
    path1 = b'D:\dll\str1.txt'# your own path to file str.txt
    path2 = b'D:\dll\\vocabular.txt' # your own path to file vocabular.txt
    encoding = 'utf-8'
    #------------------------ rules-------------------------------- :
    # 1. all strokes must be bytes strokes
    # example :
    pattern = 'man'
    # do bytes and convert pythom stroke into 'c' type
    str_pattern = ct.c_char_p(pattern.encode(encoding))
    # 2. use '.contents'   to assess to the structs and arrays(look print(text[i].contents.Text.haystack.decode(encoding)) example)
    # 3 do not forget to decode the string
    # ------------------------------------------------ how to make stroke or text array
    # 1 param = number of text, 2 param = text type (0 = stroke, 1 = text)
    texts_num = 2
    text_type = 0
    # 3 param = path to txt file (for stroke = ppath1, for text = path2)
    # 4 param = pattern(do not forget first rule)
    # 5 param = patterns num (always 0 for stroke, user number for text)
    pattern_num = 0
    # 6 param = requested length
    len = 100
    # example:
    text = lib.make_text_storage(texts_num, text_type, path1, str_pattern, pattern_num, len)
    for i in range(texts_num):
        print(text[i].Text.contents.haystack.decode(encoding))
    #---------------------------------------how to use parser -----------------------------------
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    # before call parser function install libraries : bs4, lxml, requests



    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    # make empty list
    list_ = []
    #call parser in loop and append new book

    for i in range(texts_num):
        list_.append(book_parser())
    # them do this important thing to convert list_ into 'c' type
    new_list = (ct.c_char_p * texts_num)(*map(str.encode, list_))
    #then make_parser_storage
    # 1 param = conver list, 2 param = pattern, 3 param = texts_num; 4 param = requested length
    parser_text = lib.make_parser_storage(new_list, str_pattern, texts_num, len)
    for i in range(texts_num):
         print((parser_text[i].Text.contents.haystack).decode('utf-8'))
    # -------------------------------how to call algorithm---------------------------------------
    # 1 param = the result of 'make_parser_storage' or 'make_text_storage' ('text' or 'parser_text' in our example)
    # 2 param = algorithm_type (0 - boyerMooreHorspoolMatcher; 1 - naiveStringMatcher; 2 -rabinKarpMatcher; 3 -knuthMorrisPrattMatcher)
    # 3 param = texts_num
    algorithm_res = lib.make_result_storage(parser_text, 1, texts_num)
    for i in range(texts_num):
       print((algorithm_res[i].numberOfMatches))
    # -----------------------------------------------how to do statistic------------------------------
    # 1 param = result of   'make_result_storage' func (algorithm_res in your example)
    statictic = lib.make_statictic(algorithm_res, texts_num)
    #remebmer 'make_statictic' function return NOT an array, but one single 'SearchResult' object
    print(statictic.contents.numberOfMatches)
example()



