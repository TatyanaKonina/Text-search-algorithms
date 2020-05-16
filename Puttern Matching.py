import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

if __name__ == '__main__':

    app = QApplication(sys.argv)      #создание объекта класса QApplication

    w = QWidget()
    w.resize(1200, 685)
    w.move(200, 200)
    w.setWindowTitle('Pattern Matching')

    textGen=QLabel(w)
    textGen.setText("Text Generation")
    textGen.setFont(QtGui.QFont("Calibri", 13, QtGui.QFont.Bold))
    textGen.move(65,45)

    comboBox=QComboBox(w)
    comboBox.move(20, 80)
    comboBox.addItems(["Full Random", "Random words", "Text"])
    comboBox.setFont(QtGui.QFont("Calibri", 10))
    comboBox.resize(250,50)

    textCountLab=QLabel(w)
    textCountLab.setText("Text count")
    textCountLab.setFont(QtGui.QFont("Calibri", 10))
    textCountLab.move(20, 140)

    numText=QLineEdit(w)
    numText.move(100, 140)
    numText.setFixedWidth(170)

    algLab= QLabel(w)
    algLab.setText("Algorithms")
    algLab.setFont(QtGui.QFont("Calibri", 13, QtGui.QFont.Bold))
    algLab.move(90, 195)

    algComboBox = QComboBox(w)
    algComboBox.move(20, 230)
    algComboBox.addItems(["Naive matcher", "Rabin-Karp", "Boyer-Moor-Horspool", "Knuth-Morris-Pratt", "Ukkonen's algorithm"])
    algComboBox.setFont(QtGui.QFont("Calibri", 10))
    algComboBox.resize(250, 50)

    wordLab = QLabel(w)
    wordLab.setText("Finded word")
    wordLab.setFont(QtGui.QFont("Calibri", 13, QtGui.QFont.Bold))
    wordLab.move(75, 315)

    algComboBox = QComboBox(w)
    algComboBox.move(20, 350)
    algComboBox.addItems(
        ["Full Random", "Random Word", "Entered Word"])
    algComboBox.setFont(QtGui.QFont("Calibri", 10))
    algComboBox.resize(250, 50)

    enterWord=QLineEdit(w)
    enterWord.move(20, 410)
    enterWord.setFixedWidth(250)


    optLab = QLabel(w)
    optLab.setText("Options")
    optLab.setFont(QtGui.QFont("Calibri", 13, QtGui.QFont.Bold))
    optLab.move(100, 470)

    sourceText=QTextEdit(w)
    sourceText.move(290, 80)
    sourceText.resize(440, 585)

    resultText = QTextEdit(w)
    resultText.move(740, 80)
    resultText.resize(440, 585)

    sourceLab = QLabel(w)
    sourceLab.setText("Source text")
    sourceLab.setFont(QtGui.QFont("Calibri", 13, QtGui.QFont.Bold))
    sourceLab.move(450, 45)

    resultLab = QLabel(w)
    resultLab.setText("Result")
    resultLab.setFont(QtGui.QFont("Calibri", 13, QtGui.QFont.Bold))
    resultLab.move(920, 45)
    w.show()
    sys.exit(app.exec_())