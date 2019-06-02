# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtQuick
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidget, QListWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtGui
import gimatria
from gimatria import *
from DicObj import PandasModel


class gimatria_gui(QMainWindow):
    def __init__(self):
        wanted_book_list = []
        self.wbl = wanted_book_list
        wanted_book_string = ""
        self.wbs = wanted_book_string
        self.method = 0
        QtWidgets.QMainWindow.__init__(self)
        mainWindow = loadUi("utilities/gimatria_gui.ui", self)
        self.mainWindow = mainWindow
        self.setWindowTitle("gimatria Torah calculator")
        self.my_text = ""
        self.correct = set("אבגדהוּזחטיכךלמםנןסעפףצץקרשת")
        # lcd output boxes
        self.lcdBereshit = mainWindow.lcdBereshit
        self.lcdShemot = mainWindow.lcdShemot
        self.lcdVaykra = mainWindow.lcdVaykra
        self.lcdBamidbar = mainWindow.lcdBamidbar
        self.lcdDevarim = mainWindow.lcdDevarim
        self.lcdSomma = mainWindow.lcdSomma
        #output window - list
        self.listOutput = mainWindow.listOutput
        #sezione checkboxes per la gestione dei libri in cui effettuare la ricerca:
        #checkBox per selezione Bereshit: sensore sul checked yes or not
        mainWindow.checkBereshit.stateChanged.connect(lambda state=mainWindow.checkBereshit.isChecked(), check_name=["1", str(mainWindow.checkBereshit.text())]: self.selectBooks(state, check_name))
        # checkBox per selezione Shemot: sensore sul checked yes or not
        mainWindow.checkShemot.stateChanged.connect(lambda state=mainWindow.checkShemot.isChecked(), check_name=["2", str(mainWindow.checkShemot.text())]: self.selectBooks(state, check_name))
        # checkBox per selezione Bereshit: sensore sul checked yes or not
        mainWindow.checkVaykra.stateChanged.connect(lambda state=mainWindow.checkVaykra.isChecked(), check_name=["3", str(mainWindow.checkVaykra.text())]: self.selectBooks(state, check_name))
        # checkBox per selezione Bereshit: sensore sul checked yes or not
        mainWindow.checkBamidbar.stateChanged.connect(lambda state=mainWindow.checkBamidbar.isChecked(), check_name=["4", str(mainWindow.checkBamidbar.text())]: self.selectBooks(state, check_name))
        # checkBox per selezione Bereshit: sensore sul checked yes or not
        mainWindow.checkDevarim.stateChanged.connect(lambda state=mainWindow.checkDevarim.isChecked(), check_name=["5", str(mainWindow.checkDevarim.text())]: self.selectBooks(state, check_name))
        #sezione per i radio buttons: metodi di indagine:
        #  1- classic gimatria
        #  2- gimatria moderna (consonanti sofit valutate come multiplo di 100
        mainWindow.radioButtonClassic.clicked.connect(lambda state=mainWindow.radioButtonClassic.isChecked(), check_method=[1, "classic"]: self.selectMethod(state, check_method))
        mainWindow.radioButtonModern.clicked.connect(lambda state=mainWindow.radioButtonModern.isChecked(), check_method=[2, "modern"]: self.selectMethod(state, check_method))
        #importa testo (o numero) scelto per iniziare la ricerca
        mainWindow.pushButton.clicked.connect(lambda: self.startApplication(mainWindow.textImmission))

    def selectBooks(self, state, s_data):
        if state == QtCore.Qt.Checked:
            self.wbl.append(s_data[0])
            self.wbs = ' '.join(str(self.wbl)).replace("[", "").replace("]", "")
            print('Checked ' + str(s_data))
            print(self.wbl, self.wbs)
        else:
            self.wbl.remove(s_data[0])
            print('Unchecked' + str(s_data))
            self.wbs = ' '.join(str(self.wbl)).replace("[", "").replace("]", "")
            print(self.wbl, self.wbs)

    def selectMethod(self, state, met):
        my_method = met[0]
        print(met)
        self.method = my_method

    def startApplication(self, source):
        my_text = source.text()
        self.my_text = my_text
        print("my_text", my_text, len(my_text))
        if int(self.method) != 1 and int(self.method) != 2:
            print("insert a valid search method", self.method)
            method_go = False
        else:
            method_go = True
        if len(self.my_text) == 0:
            print("insert a valid text string for search, or an integer number")
        else:
            if (set(self.my_text) <= self.correct and self.my_text.isdecimal()):
                print("usare solo caratteri ebraici o numeri arabi, per favore.\n")
                text_go = False
            else:
                text_go = True
        if not method_go or not text_go:
            print("cannot start")
        else:
            print("start main")
            valuesMix, valuesLines, searched_word_indices = mainProgram(self.method, self.wbl, self.my_text)
            self.printAppResult(valuesMix, valuesLines, searched_word_indices)

    @staticmethod
    def sumVals(val_1, val_2, val_3, val_4, val_5):
        if val_1 is None:
            val_1 = 0
        if val_2 is None:
            val_2 = 0
        if val_3 is None:
            val_3 = 0
        if val_4 is None:
            val_4 = 0
        if val_5 is None:
            val_5 = 0
        return val_1 + val_2 + val_3 + val_4 + val_5

    def printAppResult(self, vals, lines, searched_word_indices):
        val_1 = val_2 = val_3 = val_4 = val_5 = 0
        self.lcdBereshit.display(vals[0])
        self.lcdShemot.display(vals[1])
        self.lcdVaykra.display(vals[2])
        self.lcdBamidbar.display(vals[3])
        self.lcdDevarim.display(vals[4])
        self.lcdSomma.display(sum(vals))

        #immette il modello (i dati elaborati da Pandas) nella QTableView "listOutput"
        lines.data(lines.index(7, 2), role=QtCore.Qt.BackgroundRole)
        self.listOutput.setModel(lines)
        # self.listOutput.setShowGrid(False)


        # -> pyhton pandas code per lista di index di valori in tabella -> df.index[df["column name"] == "wanted_data"]
        #list cohomprension per ottenere lista di indici relativi alla parola cercata (identità di lemma) nel df di output
        # NB: 2 è il numero della colonna "words" -> cambia solo se si riduce il numero di colonne! Al posto di "2" immettere SOLO il numero della colonna "words"
        # (col count starts from "0")
        # lista come oggetto QT
        searched_word_matches = [QtCore.QPersistentModelIndex(self.listOutput.model().index(item, 2)) for item in searched_word_indices]
        # lista resa leggibile con le funzioni index.row() ..column() e ...data()
        # struttura lista: lvl1: gruppo [row, column, word] lvl2: 0 riga, 1, colonna, 2 parola. la visualizzazione in console viene ribaltata a causa dell'uso dei caratteri ebraici
        searched_word_matches = [[item.row(), item.column(), item.data()] for item in searched_word_matches]
        # print(searched_word_matches, "searched word matches - linea 146\n", searched_word_matches[0])


def mainProgram(method, choosen_list, my_text):
    exit_word = False
    print("inserisci:\n     1 - per conversione classica Ebraico - valori\n     2 - per conversione estesa (le lettere sofit hanno valori di x*100)")
    choice = method
    dictionary = md(choice).make_dictionary()
    # print(dictionary)
    gm = GimValue(dictionary)
    #correct = set("אבגדהוּזחטיכךלמםנןסעפףצץקרשת")
    word = my_text

    #word = input("immetti parola da calcolare e raffrontare;\noppure inserisci il valore numerico desiderato: \n_____\n(oppure scrivi exit per uscire dal programma)\n");
    if word == "exit":
        exit_word = True
    while not exit_word:

    #    while not (set(word) <= correct or word.isdecimal()):
    #        print("usare solo caratteri ebraici o numeri arabi, per favore.\n")
    #        word = input()

        start_watch = timeit.default_timer()
        gim_word = gm.convert_word(word)
        gim_word = sum(gim_word)
        word_array = [word, gim_word]
        c_1 = word_array
        check = set("12345 ")
        choosen_ones = choosen_list
        ok = False
        result_list = []
        while not ok:
            # choosen_ones = f5(choosen_ones)
            for c in choosen_ones:
                if c.strip() in "12345":
                    ok = True
                else:
                    choosen_ones = input("\nin quali libri biblici effettuare la ricerca:" \
                                         "\n1- Bereshit\n2- Shemot\n3- Vaykra\n4- Bamidbar\n5- Devarim\n" \
                                         "Inserire i numeri dei libri desiderati separati da uno spazio.\n"\
                                         "Premi semplicemente invio per cercare in tutti i testi")
                    if choosen_ones == "":
                        choosen_ones = "1 2 3 4 5"
                    ok = False
                    choosen_ones = choosen_ones.split()

        selected_books = gm.choosen_books(choosen_ones)
        word_index, book_title, my_data = gm.get_Bible_text(selected_books)
        # print(my_data, "my data in gui")
        # print(my_data.loc[my_data['values'] == c_1[1]], "matches")

        lines = my_data.loc[my_data['values'] == c_1[1]]

        #esempio ritrovamento numero di ricorrenze per parola cercata nel df estratto di riferimento
        linez = lines.reset_index()
        searched_word_indeces = linez.index[linez["words"] == word]
        # print(searched_word_indeces, "searched word index")

        # elapsed = timeit.default_timer() - start_watch
        # print(elapsed)
        count_Bereshit = sum(lines.loc[my_data["books"] == "Bereshit"].applymap(lambda x: 'Bereshit' in str(x)).sum())
        count_Shemot = sum(lines.loc[my_data["books"] == "Shemot"].applymap(lambda x: 'Shemot' in str(x)).sum())
        count_Vaykra = sum(lines.loc[my_data["books"] == "Vaykra"].applymap(lambda x: 'Vaykra' in str(x)).sum())
        count_Bamidbar = sum(lines.loc[my_data["books"] == "Bamidbar"].applymap(lambda x: 'Bamidbar' in str(x)).sum())
        count_Devarim = sum(lines.loc[my_data["books"] == "Devarim"].applymap(lambda x: 'Devarim' in str(x)).sum())

        #Lista contenente il numero di ricorrenze trovate per ogni volume della Torah
        valuesBox = [count_Bereshit, count_Shemot, count_Vaykra, count_Bamidbar, count_Devarim]
        #converte la tabella pandas in un formato leggibile dalla QTableView
        valuesLines = PandasModel(lines)
        #print(len(valuesLines))
        return valuesBox, valuesLines, searched_word_indeces
        # word = input("\nimmetti parola da calcolare e raffrontare;\noppure inserisci il valore numerico desiderato: \n_____\n(oppure scrivi exit per uscire dal programma)\n");
        exit_word = True


app = QApplication(sys.argv)
widget = gimatria_gui()
widget.show()
sys.exit(app.exec_())

