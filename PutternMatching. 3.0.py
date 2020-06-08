import sys
import requests
import random
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
import ctypes as ct


path1=b'C:\Users\Polina\\repos\\text-search-algorithms\str.txt'
path2=b'C:\Users\Polina\\repos\\text-search-algorithms\\vocabular.txt'
# #---------------------path to dll-------------------------------------
path = r"C:\Users\Polina\source\repos\dll\Debug\dll.dll"  # or full path
lib = ct.CDLL(path)
encoding = 'utf-8'
#--------- ------------------------------------------

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()

sys.excepthook = log_uncaught_exceptions
def make_html(url):
    return BeautifulSoup(requests.get(url).content, 'lxml')
#-----------------------------parser------------------------------
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
    _fields_ = [("matchedShifts", ct.POINTER(ct.c_int)),      #
                ("numberOfMatches", ct.c_int),
                ("numOfCompares",ct.c_int),
                ("numOfExtraOps",ct.c_int),
                ("workTime", ct.c_double),
                ("memoryWaste",ct.c_int)]

#------------------------------------- define c functions-------------------------------
lib.make_text_storage.argtype = [ct.c_int, ct.c_int, ct.c_char_p, ct.c_char_p, ct.c_int, ct.c_int]
lib.make_text_storage.restype = ct.POINTER(SearchRequest)

lib.make_result_storage.argtype = [ct.POINTER(SearchRequest), ct.c_int, ct.c_int]
lib.make_result_storage.restype = ct.POINTER(SearchResult)

lib.make_statictic.argtype = [ct.POINTER(SearchResult), ct.c_int ]
lib.make_statictic.restype = ct.POINTER(SearchResult)

lib.make_parser_storage.argtype = [(ct.c_char_p),ct.c_char_p,ct.c_int,ct.c_int]
lib.make_parser_storage.restype = ct.POINTER(SearchRequest)

#---------------------tabs--------------------------

class Tab(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pattern Matching")
        self.resize(900, 600)
        tabWidget = QTabWidget()
        tabWidget.setTabPosition(QTabWidget.South)

        vbox=QVBoxLayout()

        tabWidget.addTab(TextGeneration(), "Text Generation")
        vbox.addWidget(tabWidget)
        self.setLayout(vbox)

        tabWidget.addTab(Result(), "Result")
        vbox.addWidget(tabWidget)
        self.setLayout(vbox)

#---------------обработка нажатия на текстовое поле-----------------
class cQLineEdit(QLineEdit):
    clicked= pyqtSignal()
    def __init__(self,widget):
        super().__init__(widget)
    def mousePressEvent(self,QMouseEvent):
        self.clicked.emit()
#------------------tab "TextGeneration--------------------------
class TextGeneration(QWidget):

    def __init__(self):
        super().__init__()

        label=QLabel("Text Generation", alignment=QtCore.Qt.AlignCenter)
        label.setStyleSheet("""
        font: bold""")

        self.comboBox = QComboBox()
        self.comboBox.addItems(["Full Random", "Random words", "Text"])
        self.comboBox.currentTextChanged.connect(self.FormatSize)

        onlyNum = QtGui.QIntValidator(0, 10000)


        self.sizeLine=cQLineEdit(self)
        self.sizeLine.setValidator(onlyNum)
        self.sizeLine.clicked.connect(self.printText)
        self.sizeLine.setText('Number of words')

        self.countLine = QLineEdit()
        self.countLine.setValidator(onlyNum)

        labelSourceText = QLabel("SourceText",alignment=QtCore.Qt.AlignCenter)
        labelSourceText.setStyleSheet("""
        font: bold""")

        self.sourceText=QTextEdit()

        global textCombobox
        textCombobox=QComboBox()
        global settingWordCombobox
        settingWordCombobox = QComboBox()
        settingWordCombobox.addItems(["Manual", "Generate"])

        buttonOk=QPushButton("OK")
        settingWordCombobox.currentTextChanged.connect(self.SetWord)
        setWordLabel=QLabel("Algorothms Settings", alignment=QtCore.Qt.AlignCenter)
        setWordLabel.setStyleSheet("""
                font: bold""")


        self.algorithmCombobox = QComboBox()
        self.algorithmCombobox.addItems(
            ["Naive Matcher", "Rabin Karp", "Boyer Moor Horspool", "KMP"])

        putternSettings=QLabel("Pattern Settings", alignment=QtCore.Qt.AlignCenter)
        putternSettings.setStyleSheet("""
        font: bold""")
        self.numberPuttern=cQLineEdit(self)

        self.numberPuttern.setStyleSheet("""
                        color: gray;
                        font: italic""")
        self.numberPuttern.setText("only for random words")
        self.numberPuttern.setValidator(onlyNum)


        self.enterWordEdit = cQLineEdit(self)

        global sourceTextAlg
        sourceTextAlg = QTextEdit()
        sourceTextAlg.setReadOnly(True)
        buttonOk.clicked.connect(self.PushOK)

        self.sourceText.setReadOnly(True)

        self.fbox2=QFormLayout()
        gbox=QGridLayout()
        fbox1=QFormLayout()
        vbox=QVBoxLayout()

        self.fbox2.addRow(label)
        self.fbox2.addRow(self.comboBox)
        self.fbox2.addRow("Size of text: ", self.sizeLine)
        self.fbox2.addRow("Text count:    ", self.countLine)
        self.fbox2.addRow(setWordLabel)

        self.fbox2.addRow(self.algorithmCombobox)
        self.fbox2.addRow(putternSettings)
        self.fbox2.addRow("Number of patterns", self.numberPuttern)
        self.fbox2.addRow(settingWordCombobox)
        vbox.addLayout(self.fbox2)


        self.fbox2.addRow("Search word: ", self.enterWordEdit)
        vbox.addWidget(buttonOk)

        fbox1.addRow(labelSourceText)
        fbox1.addRow(textCombobox)
        fbox1.addRow(self.sourceText)
        gbox.setColumnStretch(1,1)
        gbox.addLayout(vbox,0,0)
        gbox.addLayout(fbox1,0,1)

        self.setLayout(gbox)
        self.sizeLine.setStyleSheet("""
        color: gray;
        font: italic""")
        self.sizeLine.setText("number of symbols")

    def SetWord(self):
        self.fbox2.removeRow(10)
        if settingWordCombobox.currentText() == "Generate":
            self.randomCombobox = QComboBox()
            self.randomCombobox.addItems(["Full random", "Random word"])
            self.fbox2.addRow(self.randomCombobox)


#----------------------------press the button OK--------------------------------


    def PushOK(self):
        if self.sizeLine.text=='number of words' or self.sizeLine.text()=='number of symbols' or self.countLine.text()=='' or self.numberPuttern.text()=='' or self.enterWordEdit.text()=='':
            return
        textCombobox.clear()
        textComboboxRes.clear()
        self.sourceText.clear()
        self.sourceText.clear()
        self.sourceText.clear()
        resulText.clear()
        countText = self.countLine.text()
        a = int(countText)
        for i in range(a):
            textCombobox.addItem("Text " + str(i + 1))
            textComboboxRes.addItem("Text " + str(i + 1))

        text_num = a
        puttern_num=0
        if self.comboBox.currentText()=="Random words":
            puttern_num=self.numberPuttern.text()
        pattern = self.enterWordEdit.text()
        c_pattern = ct.c_char_p(pattern.encode(encoding))
        #self.text=0
        if self.comboBox.currentText() == "Text":

            list_ = []
            for i in range(text_num):
                list_.append(book_parser())
                new_list = (ct.c_char_p * text_num)(*map(str.encode, list_))
            self.text=lib.make_parser_storage(new_list, c_pattern, text_num, len)
            for i in range(text_num):
                print((self.text[i].Text.contents.haystack).decode('utf-8'))

        else:
            text_num = a
            text_type = 0
            puttern_num=0
            path=path1

            if self.comboBox.currentText() == "Full Random":
                text_type=0
                path=path1
            if self.comboBox.currentText() == "Random words":
                text_type=1
                path=path2
                puttern_num = self.numberPuttern.text()

            puttern_num=int(puttern_num)
            len = int(self.sizeLine.text())
            self.text = (lib.make_text_storage(text_num, text_type, path, c_pattern, puttern_num, len))
        self.sourceText.append(self.text[0].Text.contents.haystack.decode(encoding))

        resulText.append(self.text[0].Text.contents.haystack.decode(encoding))

        numAlg=1
        if self.algorithmCombobox.currentText=="Boyer Moor Horspool":
            numAlg=0
        elif self.algorithmCombobox.currentText=="Naive Matcher":
            numAlg=1
        elif self.algorithmCombobox.currentText=="Rabin Karp":
            numAlg=2
        elif self.algorithmCombobox.currentText=="KMP":
            numAlg=3

        self.algorithm_res = lib.make_result_storage(self.text, numAlg , text_num)

        statictic = lib.make_statictic(self.algorithm_res, text_num)

        numberOfMatches.setText("Number of matches: " + str(self.algorithm_res[0].numberOfMatches))
        numOfComparises.setText("Number of comparisons: " + str(self.algorithm_res[0].numOfCompares))
        numOfExtraOps.setText("Number of extra operations: " + str(self.algorithm_res[0].numOfExtraOps))
        memoryWaste.setText("Memory waste: " + str(self.algorithm_res[0].memoryWaste))
        genNumberOfMatches.setText("Number of matches: " + str(statictic.contents.numberOfMatches))

        genNumOfComparises.setText("Number of comparisons: " + str(statictic.contents.numOfCompares))
        genNumOfExtraOps.setText("Number of extra operations: " + str(statictic.contents.numOfExtraOps))
        genMemoryWaste.setText("Memory waste: " + str(statictic.contents.memoryWaste))
        #print(statictic.contents.numberOfMatches)
        textCombobox.currentTextChanged.connect(self.ChooseText)
        textComboboxRes.currentTextChanged.connect(self.ChooseTextRes)






    def ChooseText(self):
        self.sourceText.clear()
        #self.sourceText.clear()

        b = textCombobox.currentText()
        print(len(b))
        if b=='':
            return
        c = ''
        for i in range(5, len(b)):
            c += b[i]
        h=int(c)-1
        self.sourceText.append(self.text[h].Text.contents.haystack.decode(encoding))
        h+=1

    def ChooseTextRes(self):
        resulText.clear()
        b = textComboboxRes.currentText()
        if b=='':
            return
        c = ''
        for i in range(5, len(b)):
            c += b[i]
        h=int(c)-1
        resulText.append(self.text[h].Text.contents.haystack.decode(encoding))
        numberOfMatches.setText("Number of matches: " + str(self.algorithm_res[h].numberOfMatches))
        numOfComparises.setText("Number of comparisons: " + str(self.algorithm_res[h].numOfCompares))
        numOfExtraOps.setText("Number of extra operations: " + str(self.algorithm_res[h].numOfExtraOps))
        memoryWaste.setText("Memory waste: " + str(self.algorithm_res[h].memoryWaste))


    def FormatSize(self):
        self.sizeLine.setStyleSheet("""
                color: gray;
                font: italic""")
        if self.comboBox.currentText()=="Full Random":
            self.sizeLine.setText("number of symbols")
        if self.comboBox.currentText()=="Full Random" or self.comboBox.currentText()=="Text":
            self.numberPuttern.setStyleSheet("""
                color: gray;
                font: italic""")
            self.numberPuttern.setText("only for random words")
            self.numberPuttern.setReadOnly(True)
        if self.comboBox.currentText()=="Random words":
            self.numberPuttern.clear()
            self.numberPuttern.setReadOnly(False)
            self.numberPuttern.setStyleSheet("""
                           color: black;""")



        else:
            self.sizeLine.setText("number of words")
        #self.setLayout(hbox)
    def ClearEditLine(self):
        self.sizeLine.clear()


    def printText(self):
        self.sizeLine.clear()
        self.sizeLine.setStyleSheet("""
                color: black;
                """)




    # def EnterPattern(self):
    #     if self.randomCombobox=="Full random":


# class FindWord(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         # algorithmsLabel=QLabel("Algorithm")
#         #
#         # algorithmCombobox=QComboBox()
#         # algorithmCombobox.addItems(["Naive Matcher", "Rabin Karp", "Boyer Moor Horspool", "KMP", "Ukkornen's algorithm"])
#
#         labelSourceText = QLabel("SourceText")
#
#         global textComboboxAl
#         textComboboxAl = QComboBox()
#
#
#        # sourceText.append(text[0].Text.contents.haystack.decode(encoding))
#
#         global fbox
#         fbox=QFormLayout()
#         fbox1 = QFormLayout()
#         gbox = QGridLayout()
#         global vbox
#         vbox=QVBoxLayout()
#
#         fbox.addRow(algorithmsLabel)
#         fbox.addRow(algorithmCombobox)
#        # fbox.addRow(setWordLabel)
#         #
#         fbox1.addRow(labelSourceText)
#         fbox1.addRow(textComboboxAl)
#         fbox1.addRow(sourceTextAlg)
#        # settingWordCombobox.currentTextChanged.connect(self.SetWord)
#         #enterWordEdit = QLineEdit()
#         btnOKGen = QPushButton("ОК")
#         #fbox.addRow("Search word: ", enterWordEdit)
#         vbox.addLayout(fbox)
#         vbox.addWidget(btnOKGen)
#
#
#         gbox.setColumnStretch(1, 1)
#         gbox.addLayout(vbox, 0, 0)
#         gbox.addLayout(fbox1, 0, 1)
#
#         self.setLayout(gbox)





class Result(QWidget):
    def __init__(self):
        super().__init__()
        global textComboboxRes
        textComboboxRes=QComboBox()
        global resulText
        resulText=QTextEdit()
       # global matchedShifts
        #matchedShifts=QLabel()
        global genNumberOfMatches
        global genNumOfComparises
        global genNumOfExtraOps
        global genMemoryWaste
        global numberOfMatches
        global numOfComparises
        global numOfExtraOps
        global memoryWaste


        generalResultsLabel=QLabel("General results", alignment=QtCore.Qt.AlignCenter)
        generalResultsLabel.setStyleSheet("""
        font: bold""")
        genNumberOfMatches = QLabel("Number of pattern: -")
        genNumOfComparises = QLabel("Number of comparisons: -")
        genNumOfExtraOps = QLabel("Number of extra operations: -")
        genMemoryWaste = QLabel("Memory waste: -")
        resultsLabel=QLabel("Current text result", alignment=QtCore.Qt.AlignCenter)
        resultsLabel.setStyleSheet("""
        font: bold""")
        numberOfMatches=QLabel("Number of pattern: -")
        numOfComparises=QLabel("Number of comparisons: -")
        numOfExtraOps=QLabel("Number of extra operations: -")
        memoryWaste=QLabel("Memory waste: -")

        fbox1=QFormLayout()
        fbox2=QFormLayout()
        gbox=QGridLayout()
        fbox1.addWidget(generalResultsLabel)
        fbox1.addWidget(genNumberOfMatches)
        fbox1.addWidget(genNumOfComparises)
        fbox1.addWidget(genNumOfExtraOps)
        fbox1.addWidget(genMemoryWaste)
        fbox2.addWidget(resultsLabel)
        fbox2.addWidget(textComboboxRes)
        fbox2.addWidget(resulText)
        fbox2.addWidget(numberOfMatches)
        fbox2.addWidget(numOfComparises)
        fbox2.addWidget(numOfExtraOps)
        fbox2.addWidget(memoryWaste)

        gbox.setColumnStretch(1,0)
        gbox.addLayout(fbox1, 0,0)
        gbox.addLayout(fbox2, 0, 1)
        self.setLayout(gbox)

if __name__ == '__main__':
    app = QApplication(sys.argv) #создание объекта класса QApplication
    tabDialog=Tab()
    tabDialog.show()
    sys.exit(app.exec_())
    app = QtWidgets.QApplication(sys.argv)