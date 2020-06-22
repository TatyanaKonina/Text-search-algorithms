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
path = r"C:\Users\Polina\source\repos\dll2\Debug\dll2.dll"  # or full path
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
def book_parser():
    pages_num = 50
    book_box = 4
    link_box = 2
    s = ""
    url = 'http://www.loyalbooks.com/Top_100'
    main_link = 'http://www.loyalbooks.com'

    random_link = random.randint(1, pages_num)
    if (random_link != 1):
        url = url + '/' + str(random_link) + '/'

    make_html(url)
    book = make_html(url).find('table', class_='layout2-blue').find_all('td',
                                                                        class_='layout2-blue')  # получили все книги на странице
    i = random.randint(0, pages_num)

    while (s == ""):
        if (len(book) - 1 > i) & (book[i].find('a') != -1):

            book_link = book[i].find('a').get('href')  # первая ссылка
            if (book_link != None):
                name = book[i].find('b').text  # нашли название книги
                link = main_link + book_link
                page_book_html = make_html(link)  # перешли на страницу книги
                if len(page_book_html.find_all('table',
                                               class_='book')) > book_box:  # проверка на случай если на сайте нет онлайн версии
                    author = page_book_html.find('font', class_='book-author').text  # нашли автора
                    e_book_link = page_book_html.find_all('table', class_='book')[book_box].find_all('td', class_='book2')[
                        link_box].find(
                        'a').get('href')
                    # нашли ссылку на которой онлайн книга
                    page_book_txt = make_html(e_book_link)
                    s = name + ' ' + author
                    text = page_book_txt.find_all('p')
                    for p in text:
                        s = s + p.text
                    return s
        i = random.randint(0, pages_num)

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

        onlyNum = QtGui.QIntValidator(1, 10000)


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


        self.textCombobox=QComboBox()
        self.settingWordCombobox = QComboBox()
        self.settingWordCombobox.addItems(["Manual", "Generate"])

        buttonOk=QPushButton("OK")
        buttonClear=QPushButton("Clear")
        self.settingWordCombobox.currentTextChanged.connect(self.SetWord)
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


        self.enterWordEdit = cQLineEdit(self)

        global sourceTextAlg
        sourceTextAlg = QTextEdit()
        sourceTextAlg.setReadOnly(True)
        buttonOk.clicked.connect(self.PushOK)
        buttonClear.clicked.connect(self.Clear)

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
        self.fbox2.addRow(self.settingWordCombobox)
        vbox.addLayout(self.fbox2)

        self.fbox2.addRow("Search word: ", self.enterWordEdit)

        vbox.addWidget(buttonOk)
        vbox.addWidget(buttonClear)

        fbox1.addRow(labelSourceText)
        fbox1.addRow(self.textCombobox)
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
        if self.settingWordCombobox.currentText() == "Generate":
            self.enterWordEdit.setStyleSheet("""
        color: gray;
        font: italic""")
            self.enterWordEdit.setReadOnly(True)
            self.enterWordEdit.setText("random word")
        else:
            self.enterWordEdit.clear()
            self.enterWordEdit.setReadOnly(False)
            self.enterWordEdit.setStyleSheet("""
                    color: black;
                    font: normal""")

        

# ----------------------------press the button OK--------------------------------


    def PushOK(self):
        if self.sizeLine.text=='number of words' or self.sizeLine.text()=='number of symbols' or self.countLine.text()=='' or self.numberPuttern.text()=='':
           return
        self.textCombobox.clear()
        textComboboxRes.clear()
        self.sourceText.clear()
        # self.sourceText.clear()
        # self.sourceText.clear()
        resulText.clear()
        countText = self.countLine.text()
        a = int(countText)
        for i in range(a):
            self.textCombobox.addItem("Text " + str(i + 1))
            textComboboxRes.addItem("Text " + str(i + 1))
        text_num = a
        puttern_num=0
        if self.comboBox.currentText()=="Random words":
            puttern_num=self.numberPuttern.text()
        if self.settingWordCombobox.currentText()=="Manual":
            self.pattern = self.enterWordEdit.text()
            c_pattern = ct.c_char_p(self.pattern.encode(encoding))
        else:
            c_pattern=0

        if self.comboBox.currentText() == "Text":

            list_ = []
            for i in range(text_num):
                list_.append(book_parser())
                new_list = (ct.c_char_p * text_num)(*map(str.encode, list_))
            self.text=lib.make_parser_storage(new_list, c_pattern, text_num, len)
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
            length = int(self.sizeLine.text())
            print(length)
            if self.settingWordCombobox.currentText() == "Generate":
                self.text = (lib.make_text_storage(text_num, text_type, path, 0, puttern_num, length))
            else:
                self.text = (lib.make_text_storage(text_num, text_type, path, c_pattern, puttern_num, length))
        textik=self.text[0].Text.contents.haystack.decode(encoding)
        self.sourceText.append(self.text[0].Text.contents.haystack.decode(encoding))
        if self.settingWordCombobox.currentText()=="Generate":
            self.enterWordEdit.clear()
            self.enterWordEdit.setStyleSheet("""font: normal; color: black""")
            self.enterWordEdit.setText(self.text[0].Pattern.contents.needle.decode(encoding))
        numAlg=1
        if self.algorithmCombobox.currentText()=="Boyer Moor Horspool":
            numAlg=0
        elif self.algorithmCombobox.currentText()=="Naive Matcher":
            numAlg=1
        elif self.algorithmCombobox.currentText()=="Rabin Karp":
            numAlg=2
        elif self.algorithmCombobox.currentText()=="KMP":
            numAlg=3

        self.algorithm_res = lib.make_result_storage(self.text, numAlg, text_num)
        numPatrern=0
        i=0
        printRes=''
        numPattern = 0
        printRes = ''

        text = self.text[0].Text.contents.haystack.decode(encoding)
        i = 0
        if self.comboBox.currentText() == "Random words":
            if self.algorithm_res[0].numberOfMatches != 0:
                while i < len(text):
                    if i == self.algorithm_res[0].matchedShifts[numPattern]:
                        for j in range(i,  len(self.text[0].Pattern.contents.needle.decode(encoding))+i):
                            redText = "<span style=\" font: bold; color: #ffa500;\">"
                            redText += (text[j])

                            printRes += (redText)
                        numPattern += 1
                        i += len(self.text[0].Pattern.contents.needle.decode(encoding))
                    else:
                        blackText = "<span style=\" font: normal; color: black;\">"
                        blackText += text[i]
                        printRes += (blackText)
                        i += 1
                resulText.append(printRes)
            else:
                resulText.append(self.text[0].Text.contents.haystack.decode(encoding))
        else:
            if self.algorithm_res[0].numberOfMatches != 0:
                while i < len(text):
                    if i == self.algorithm_res[0].matchedShifts[numPattern]:
                        if i+1==self.algorithm_res[0].matchedShifts[numPattern+1]:
                            redText = "<span style=\" font: bold; color: #ffa500;\">"
                            redText += (text[i])
                            printRes += (redText)
                            i+=1
                        else:
                            for j in range(i, i + len(self.text[0].Pattern.contents.needle.decode(encoding))):
                                redText = "<span style=\" font: bold; color: #ffa500;\">"
                                redText += (text[j])
                                printRes += (redText)
                            i+=len(self.text[0].Pattern.contents.needle.decode(encoding))
                        numPattern += 1
                    else:
                        blackText = "<span style=\" font: normal; color: black;\">"
                        blackText += text[i]
                        printRes += (blackText)
                        i += 1
                resulText.append(printRes)
            else:
                resulText.append(self.text[0].Text.contents.haystack.decode(encoding))

        statictic = lib.make_statictic(self.algorithm_res, text_num)

        numberOfMatches.setText("Number of matches: " + str(self.algorithm_res[0].numberOfMatches))
        numOfComparises.setText("Number of comparisons: " + str(self.algorithm_res[0].numOfCompares))
        numOfExtraOps.setText("Number of extra operations: " + str(self.algorithm_res[0].numOfExtraOps))
        workTime.setText("Work time: " + str(self.algorithm_res[0].workTime))
        memoryWaste.setText("Memory waste: " + str(self.algorithm_res[0].memoryWaste))
        genPattern.setText("Pattern: "+ self.enterWordEdit.text())
        genNumOfComparises.setText("Number of comparisons: " + str(statictic.contents.numOfCompares))
        genNumOfExtraOps.setText("Number of extra operations: " + str(statictic.contents.numOfExtraOps))
        genWorkTime.setText("Work time: " + str(statictic.contents.workTime))
        genMemoryWaste.setText("Memory waste: " + str(statictic.contents.memoryWaste))
        self.textCombobox.currentTextChanged.connect(self.ChooseText)
        textComboboxRes.currentTextChanged.connect(self.ChooseTextRes)






    def ChooseText(self):
        self.sourceText.clear()
        b = self.textCombobox.currentText()
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
        numberOfMatches.setText("Number of matches: " + str(self.algorithm_res[h].numberOfMatches))
        numOfComparises.setText("Number of comparisons: " + str(self.algorithm_res[h].numOfCompares))
        numOfExtraOps.setText("Number of extra operations: " + str(self.algorithm_res[h].numOfExtraOps))
        workTime.setText("Work time: "+ str(self.algorithm_res[h].workTime))
        memoryWaste.setText("Memory waste: " + str(self.algorithm_res[h].memoryWaste))
        numPattern=0
        printRes = ''
        text=self.text[h].Text.contents.haystack.decode(encoding)
        i=0
        if self.comboBox.currentText() == "Random words":
            if self.algorithm_res[h].numberOfMatches != 0:
                while i < len(text):
                    if i == self.algorithm_res[h].matchedShifts[numPattern]:
                        for j in range(i,  len(self.text[h].Pattern.contents.needle.decode(encoding))+i):
                            redText = "<span style=\" font: bold; color: #ffa500;\">"
                            redText += (text[j])

                            printRes += (redText)
                        numPattern += 1
                        i += len(self.text[h].Pattern.contents.needle.decode(encoding))
                    else:
                        blackText = "<span style=\" font: normal; color: black;\">"
                        blackText += text[i]
                        printRes += (blackText)
                        i += 1
                resulText.append(printRes)
            else:
                resulText.append(self.text[h].Text.contents.haystack.decode(encoding))
        else:
            if self.algorithm_res[h].numberOfMatches != 0:
                while i < len(text):
                    if i == self.algorithm_res[h].matchedShifts[numPattern]:
                        if i+1==self.algorithm_res[h].matchedShifts[numPattern+1]:
                            redText = "<span style=\" font: bold; color: #ffa500;\">"
                            redText += (text[i])
                            printRes += (redText)
                            i+=1
                        else:
                            for j in range(i, i + len(self.text[h].Pattern.contents.needle.decode(encoding))):
                                redText = "<span style=\" font: bold; color: #ffa500;\">"
                                redText += (text[j])
                                printRes += (redText)
                            i+=len(self.text[h].Pattern.contents.needle.decode(encoding))
                        numPattern += 1
                    else:
                        blackText = "<span style=\" font: normal; color: black;\">"
                        blackText += text[i]
                        printRes += (blackText)
                        i += 1
                resulText.append(printRes)
            else:
                resulText.append(self.text[h].Text.contents.haystack.decode(encoding))



    def Clear(self):
        self.comboBox.setCurrentText("Full Random")
        self.countLine.clear()
        self.algorithmCombobox.setCurrentText("Naive Matcher")
        self.settingWordCombobox.setCurrentText('Manual')
        self.numberPuttern.clear()
        self.textCombobox.clear()
        textComboboxRes.clear()
        self.enterWordEdit.clear()
        self.sourceText.clear()
        resulText.clear()

        genPattern.setText("Pattern: -")
        genNumOfComparises.setText("Number of comparisons: -")
        genNumOfExtraOps.setText("Number of extra operations: -")
        genWorkTime.setText("Work time: -")
        genMemoryWaste.setText("Memory waste: -")

        numberOfMatches.setText("Number of pattern: -")
        numOfComparises.setText("Number of comparisons: -")
        numOfExtraOps.setText("Number of extra operations: -")
        workTime.setText("Work time: -")
        memoryWaste.setText("Memory waste: -")



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



    def ClearEditLine(self):
        self.sizeLine.clear()



    def printText(self):
        self.sizeLine.clear()
        self.sizeLine.setStyleSheet("""
                color: black;
                """)

class Result(QWidget):
    def __init__(self):
        super().__init__()
        global textComboboxRes
        textComboboxRes=QComboBox()
        global resulText
        resulText=QTextEdit()
        global genPattern
        global genNumberOfMatches
        global genNumOfComparises
        global genNumOfExtraOps
        global genWorkTime
        global genMemoryWaste
        global numberOfMatches
        global numOfComparises
        global numOfExtraOps
        global workTime
        global memoryWaste

        generalResultsLabel=QLabel("General results", alignment=QtCore.Qt.AlignCenter)
        generalResultsLabel.setStyleSheet("""
        font: bold""")
        genPattern = QLabel("Pattern: -")
        genNumOfComparises = QLabel("Number of comparisons: -")
        genNumOfExtraOps = QLabel("Number of extra operations: -")
        genWorkTime=QLabel("Work time: -")
        genMemoryWaste = QLabel("Memory waste: -")
        resultsLabel=QLabel("Current text result", alignment=QtCore.Qt.AlignCenter)
        resultsLabel.setStyleSheet("""
        font: bold""")
        numberOfMatches=QLabel("Number of pattern: -")
        numOfComparises=QLabel("Number of comparisons: -")
        numOfExtraOps=QLabel("Number of extra operations: -")
        workTime = QLabel("Work time: -")
        memoryWaste=QLabel("Memory waste: -")

        fbox1=QFormLayout()
        fbox2=QFormLayout()
        gbox=QGridLayout()
        fbox1.addWidget(generalResultsLabel)
        fbox1.addWidget(genPattern)
        fbox1.addWidget(genNumOfComparises)
        fbox1.addWidget(genNumOfExtraOps)
        fbox1.addWidget(genWorkTime)
        fbox1.addWidget(genMemoryWaste)
        fbox2.addWidget(resultsLabel)
        fbox2.addWidget(textComboboxRes)
        fbox2.addWidget(resulText)
        fbox2.addWidget(numberOfMatches)
        fbox2.addWidget(numOfComparises)
        fbox2.addWidget(numOfExtraOps)
        fbox2.addWidget(workTime)
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
