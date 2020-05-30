import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal



class Tab(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("myproj")
        self.resize(1200, 750)

        vbox=QVBoxLayout()
        tabWidget=QTabWidget()
        tabWidget.setTabPosition(QTabWidget.South)

        tabWidget.addTab(TextGeneration(), "Text Generation")
        vbox.addWidget(tabWidget)
        self.setLayout(vbox)

        tabWidget.addTab(FindWord(), "Algorithms")
        tabWidget.addTab(Result(), "Result")

        vbox.addWidget(tabWidget)
        self.setLayout(vbox)
#обработка нажатия на текстовое поле
class cQLineEdit(QLineEdit):
    clicked= pyqtSignal()
    def __init__(self,widget):
        super().__init__(widget)
    def mousePressEvent(self,QMouseEvent):
        self.clicked.emit()

class TextGeneration(QWidget):

    def __init__(self):
        super().__init__()

        label=QLabel("Text Generation")
        label.setFont(QtGui.QFont("Calibri", 8))

        global comboBox
        comboBox = QComboBox()
        comboBox.addItems(["Full Random", "Random words", "Text"])
        comboBox.currentTextChanged.connect(self.FormatSize)

        onlyNum = QtGui.QIntValidator(0, 10000)

        global sizeLine
        sizeLine=cQLineEdit(self)
        sizeLine.setValidator(onlyNum)
        sizeLine.clicked.connect(self.printText)
        sizeLine.setText('Number of words')

        global countLine
        countLine = QLineEdit()
        countLine.setValidator(onlyNum)

        labelSourceText = QLabel("SourceText")

        sourceText=QTextEdit()

        global textCombobox
        textCombobox=QComboBox()

        buttonOk=QPushButton("OK")
        buttonOk.clicked.connect(self.PushOK)


#расположение виджетов на вкладке Text Generation
        fbox=QFormLayout()
        gbox=QGridLayout()
        fbox1=QFormLayout()
        vbox=QVBoxLayout()

        fbox.addRow(label)
        fbox.addRow(comboBox)
        fbox.addRow("Size of text: ", sizeLine)
        fbox.addRow("Text count:    ", countLine)
        vbox.addLayout(fbox)
        vbox.addWidget(buttonOk)
        fbox1.addRow(labelSourceText)
        fbox1.addRow(textCombobox)
        fbox1.addRow(sourceText)
        gbox.setColumnStretch(1,1)
        gbox.addLayout(vbox,0,0)
        gbox.addLayout(fbox1,0,1)

        self.setLayout(gbox)
        sizeLine.setStyleSheet("""
        color: gray;
        font: italic""")
        sizeLine.setText("number of symbols")



    def FormatSize(self):
        sizeLine.setStyleSheet("""
                color: gray;
                font: italic""")
        if comboBox.currentText()=="Full Random":
            sizeLine.setText("number of symbols")

        else:
            sizeLine.setText("number of words")
        #self.setLayout(hbox)
    def ClearEditLine(self):
        sizeLine.clear()
        print("Ну")

    def PushOK(self):
        textCombobox.clear()
        textComboboxAl.clear()
        textComboboxRes.clear()
        countText=countLine.text()
        a=int (countText)
        for i in range (a):
            textCombobox.addItem("Text " + str(i+1))
            textComboboxAl.addItem("Text " + str(i + 1))
            textComboboxRes.addItem("Text " + str(i+1))

    def printText(self):
        sizeLine.clear()
        sizeLine.setStyleSheet("""
                color: black;
                """)






class FindWord(QWidget):
    def __init__(self):
        super().__init__()

        algorithmsLabel=QLabel("Algorithm")

        algorithmCombobox=QComboBox()
        algorithmCombobox.addItems(["Naive Matcher", "Rabin Karp", "Boyer Moor Horspool", "KMP", "Ukkornen's algorithm"])

        setWordLabel=QLabel("Setting Word")

        global settingWordCombobox
        settingWordCombobox=QComboBox()
        settingWordCombobox.addItems(["Manual", "Generate"])


        labelSourceText = QLabel("SourceText")

        global textComboboxAl
        textComboboxAl = QComboBox()

        sourceText = QTextEdit()
        sourceText.setReadOnly(True)

        global fbox
        fbox=QFormLayout()
        fbox1 = QFormLayout()
        gbox = QGridLayout()
        global vbox
        vbox=QVBoxLayout()

        fbox.addRow(algorithmsLabel)
        fbox.addRow(algorithmCombobox)
        fbox.addRow(setWordLabel)
        fbox.addRow(settingWordCombobox)
        fbox1.addRow(labelSourceText)
        fbox1.addRow(textComboboxAl)
        fbox1.addRow(sourceText)
        settingWordCombobox.currentTextChanged.connect(self.SetWord)
        enterWordEdit = QLineEdit()
        btnOKGen = QPushButton("ОК")
        fbox.addRow("Search word: ", enterWordEdit)
        vbox.addLayout(fbox)
        vbox.addWidget(btnOKGen)


        gbox.setColumnStretch(1, 1)
        gbox.addLayout(vbox, 0, 0)
        gbox.addLayout(fbox1, 0, 1)

        self.setLayout(gbox)

    def SetWord(self):
        fbox.removeRow(4)
        fbox.removeRow(4)

        enterWordEdit=QLineEdit()
        if settingWordCombobox.currentText()=="Generate":
            randomCombobox=QComboBox()
            randomCombobox.addItems(["Full random", "Random word"])   #отсюда вызывать фуннкцию генерации слов
            fbox.addRow(randomCombobox)
            enterWordEdit.setReadOnly(True)
        fbox.addRow("Search word: ", enterWordEdit)










class Result(QWidget):
    def __init__(self):
        super().__init__()
        global textComboboxRes
        textComboboxRes=QComboBox()
        resulText=QTextEdit()

        fbox=QFormLayout()
        gbox=QGridLayout()

        fbox.addWidget(textComboboxRes)
        fbox.addWidget(resulText)
        gbox.setColumnStretch(1,0)
        gbox.addLayout(fbox, 0,0)
        self.setLayout(gbox)




if __name__ == '__main__':
    app = QApplication(sys.argv)   #создание объекта класса QApplication
    tabDialog=Tab()



    tabDialog.show()
    sys.exit(app.exec_())