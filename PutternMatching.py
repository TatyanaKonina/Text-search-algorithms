from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from array import *

size=0.3
num=''
def SetNum(_):
    chooseText.set("Choose number of text")
    num=enterNum.get()
    ar = []
    for i in range (int(num)):
        ar.append(i+1)
    chooseText2['values']=ar
    chooseText2.set("Choose number of text")            #фунцкция заполнения выпадающих списков
    num = enterNum.get()
    ar = []
    for i in range(int(num)):
        ar.append(i + 1)
    chooseText['values'] = ar


def GenerateText():
    a=0



window = Tk()
window.title("Pattern Matching")                       #окно
window.geometry('900x600')




generatingFildLab=LabelFrame(window, text=" Text generation: ", width=175, height=150)
generatingFildLab.place(relx=0.05, rely=0.05)
method=0
fullRandomRadiobut=Radiobutton(window, text="Full Random", variable=method, value=0)
fullRandomRadiobut.place(relx=0.07, rely=0.095)                                             # поле выбора генерации текста ДОДЕЛАТЬ RADIOBUTTON!
randomWordsRadiobut=Radiobutton(window, text="Random Words", variable=method, value=0)
randomWordsRadiobut.place(relx=0.07, rely=0.135)
enterNum=ttk.Combobox(window, values=[1,2,3,4,5,6,7,8,9,10], width=19)
enterNum.set("Number of texts")
enterNum.place(relx=0.07, rely=0.185)
enterNum.bind("<<ComboboxSelected>>", SetNum)


inputLab = Label(window, text="Source text: ")
inputLab.place(relx=0.052, rely=0.33)
inputText = Text(window, width=48, height=19, bd=0)        #поле ввода
inputText.place(relx=0.052, rely=0.410)
chooseText=ttk.Combobox(window, width=61)
chooseText.set("Choose number of text")
chooseText.place(relx=0.052, rely=0.375)



generateBut=Button(window, text="GENERATE", width=18, command=GenerateText, relief=GROOVE, )
generateBut.place(relx=0.07, rely=0.240)

algorithmFildLab=LabelFrame(window, text=" Algorothm: ", width=175, height=150)
algorithmFildLab.place(relx=0.285, rely=0.052)       #0.525
algorithm=0
naiveMatcherCheck=Checkbutton(window, text="Naive Matcher", variable=algorithm)             #алгоритм ДОДЕЛАТЬ ФЛАЖКИ
naiveMatcherCheck.place(relx=0.293, rely=0.09)
rabinCarpCheck=Checkbutton(window, text="Rabin Karp", variable=algorithm)
rabinCarpCheck.place(relx=0.293, rely=0.13)
boyerMooreCheck=Checkbutton(window, text="Boyer-Moore-Horspool", variable=algorithm)
boyerMooreCheck.place(relx=0.293, rely=0.17)
boyerMooreCheck=Checkbutton(window, text="Что-то еще", variable=algorithm)
boyerMooreCheck.place(relx=0.293, rely=0.21)




resultLab=Label(window, text= "Result:")
resultLab.place(relx=0.525, rely=0.33)
outputText=Text(window, width=48, height=19, bd=0)                             #тексты результатов
outputText.place(relx=0.525, rely=0.41)
chooseText2=ttk.Combobox(window, width=60)
chooseText2.set("Choose number of text")
chooseText2.place(relx=0.525, rely=0.375)

wordFildLab=LabelFrame(window, text=" Research word: ", width=175, height=150)
method=0
wordFullRandomRadiobut=Radiobutton(window, text="Full Random", variable=method, value=0)
wordFullRandomRadiobut.place(relx=0.55, rely=0.095)                                             # поле выбора генерации слова ДОДЕЛАТЬ RADIOBUTTON!
wordRandomWordsRadiobut=Radiobutton(window, text="Random Word", variable=method, value=0)
wordRandomWordsRadiobut.place(relx=0.55, rely=0.14)
wordRandomWordsRadiobut=Radiobutton(window, text="Entered Word", variable=method, value=0)
wordRandomWordsRadiobut.place(relx=0.55, rely=0.185)
wordGenerateText=Text(window, width=16, heigh=1, bd=0)
wordGenerateText.place(relx=0.55, rely=0.240)
wordFildLab.place(relx=0.525, rely=0.05)


optionsFildLab=LabelFrame(window, text=" Options: ", width=175, height=150)
optionsFildLab.place(relx=0.76, rely=0.05)                                    #настройки


window.mainloop()


