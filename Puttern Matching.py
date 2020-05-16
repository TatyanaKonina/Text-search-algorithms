import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

class Tab(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("myproj")
        self.resize(900, 450)

        vbox=QVBoxLayout()
        tabWidget=QTabWidget()
        tabWidget.setTabPosition(QTabWidget.South)

        tabWidget.addTab(TextGeneration(), "Text Generation")
        vbox.addWidget(tabWidget)
        self.setLayout(vbox)

        tabWidget.addTab(FindWord(), "Algorithms")

        vbox.addWidget(tabWidget)
        self.setLayout(vbox)



class TextGeneration(QWidget):
    def __init__(self):
        super().__init__()

        label=QLabel("Text Generation")
        label.setFont(QtGui.QFont("Calibri", 8))

        comboBox = QComboBox()
        comboBox.addItems(["Full Random", "Random words", "Text"])
       # comboBox.setFont(QtGui.QFont("Calibri", 9))

        sourceText=QTextEdit()


        textCombobox=QComboBox()
        textCombobox.addItems(["Text 1", "Text 2", "Text 3", "Text 4"])

        sizeLine=QLineEdit()
        countLine=QLineEdit()
        labelSourceText=QLabel("SourceText")
        buttonOk=QPushButton("OK")



        fbox=QFormLayout()
        gbox=QGridLayout()
        fbox1=QFormLayout()


        fbox.addRow(label)

        fbox.addRow(comboBox)
        fbox.addRow("Size of text: ", sizeLine)
        fbox.addRow("Text count: ", countLine)
        fbox.addRow("            ", buttonOk)
        fbox1.addRow(labelSourceText)
        fbox1.addRow(textCombobox)
        fbox1.addRow(sourceText)
        gbox.setColumnStretch(1,1)
        gbox.addLayout(fbox,0,0)
        gbox.addLayout(fbox1,0,1)

       # hbox.addWidget(sourceText)



        self.setLayout(gbox)
        #self.setLayout(hbox)





class FindWord(QWidget):
    def __init__(self):
        super().__init__()


class Result(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':


    app = QApplication(sys.argv)   #создание объекта класса QApplication
    tabDialog=Tab()


    tabDialog.show()
    sys.exit(app.exec_())