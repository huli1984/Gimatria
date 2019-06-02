#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import timeit
import os
from MyDict import MyDict as md
import pandas as pd
from DicObj import DicObj as DicObj
import os

class GimValue:

    def __init__(self, switcher):
        self.switcher = switcher

    def dic_conv(self, argument):
        switcher = self.switcher
        return switcher.get(argument, lambda: "invalid character: use only hebrew characters.")

    def convert_word(self, word):
        gim_word = [];
        if word.isdigit():
            gim_word.append(int(word))
            gim_word.append(0)
        else:
            for i in word:
                j = self.dic_conv(i)
                gim_word.append(int(j))
        print(gim_word)
        return gim_word

    def convert_list(self, word_list):
        gim_word = []
        gim_word_list = []
        for word in word_list:
            if word.isdigit():
                gim_word.append(int(word))
                gim_word.append(0)
            else:
                for i in word:
                    j = self.dic_conv(i)
                    gim_word.append(int(j))
                summa_parziale = sum(gim_word)
                # print(summa_parziale, "somma parziale")
                gim_word_list.append(summa_parziale)
                gim_word = []
        summa = gim_word_list
        # print(summa, "summa")
        return summa

    def convert_letter(self, w):
        if w.isdigit() or w == ":":
            j_in = w
        else:
            j_in = None
        j = self.dic_conv(w)
        return j_in, j

    def choosen_books(self, choosen_ones):
        choosen_books = []
        book_list= ["utilities/Bereshit_lines.txt",  "utilities/Shemot_lines.txt", "utilities/Vaykra_lines.txt", "utilities/Bamidbar_lines.txt", "utilities/Devarim_lines.txt" ]
        # choosen_ones = choosen_ones.split(' ')
        for item in choosen_ones:
            item = int(item) - 1
            choosen_books.append(book_list[item])
        return choosen_books

    def get_Bible_text(self, selected_books=["utilities/Bereshit_lines.txt"]):
        super_word_index = []
        super_booklist = []

        '''parte per creazione csv dizionario
        controllo se il dizionario esiste: se esiste nessuna azione'''
        if not os.path.isfile("Bible_data.csv"):
            combo_book = []
            combo_lines = []
            combo_index = []
            combo_values = []
            for selected_book in selected_books:
                my_Bible_book = open(selected_book, "r")
                my_bb_lines = my_Bible_book.readlines()
                for my_bb_line in my_bb_lines:
                    splitted_line = my_bb_line.split()
                    single_index = str(splitted_line[0]).replace("[", "").replace("]", "").replace("\u200f", "")
                    index_list = [str(splitted_line[0]).replace("[", "").replace("]", "").replace("\u200f", "")]*len(splitted_line[1:])
                    values_converted = self.convert_list(splitted_line[1:])
                    book_list = [str(selected_book).replace("utilities/", "").replace("_lines.txt", "") for i in range(len(index_list))]
                    # print(len(splitted_line[1:]), len(values_converted), len(index_list))
                    combo_book.extend(book_list)
                    combo_index.extend(index_list)
                    combo_lines.extend(splitted_line[1:])
                    combo_values.extend(values_converted)

                    '''
                    db = pd.DataFrame({"lines in text": ["erda", "capodoglio", "cazzo"], "words": ["11:18", "22:45", "74:98"], "values":[1,2,3]})
                    if not (db["values"] == 246).empty:
                    print(db)
                    '''
                    #crea oggetto dictionary con incluso link a morfix o pealim (poi deve divenire cliccabile)
            print("")
            print(len(combo_book))
            print(len(combo_values))
            print(len(combo_index))
            print(len(combo_lines))

            my_data = DicObj(combo_lines, combo_values, combo_index, combo_book)
            my_data.print_this()
            my_data.save_this() #stampa dizionario in csv su file

            '''fine parte creazione dizionario'''
        else:
            print("dictionary csv exists")
            my_data = DicObj.read_csv("Bible_data.csv");
            #print(my_data, "print existing one")

        for selected_book in selected_books:

            my_Bible_book = open(selected_book, "r")
            my_bb_line = my_Bible_book.readlines()

            word_wrapper = []
            bb_wrapper = []
            word_ref = []
            word_index = {}
            word_index_value = []
            word_index_line = []

            for my_bb in my_bb_line:
                for n, item in enumerate(my_bb):
                    # print(item + "item in root")
                    if " " in item:
                        # print(item, "item in if \" \"");
                        if bb_wrapper:
                            bb_index = ''.join(bb_wrapper)
                            word_index_line.append(bb_index)
                        else:
                            if word_index_line:
                                word_index_line.append(word_index_line[-1])

                        c_word = sum(word_wrapper)
                        # print(c_word, "c_word");
                        ref_word = "".join(word_ref)
                        ref_word = str(ref_word).replace("\u200f", "")
                        word_wrapper = []
                        bb_wrapper = []
                        word_ref = []
                        if ref_word in word_index:
                            word_index[ref_word].append(word_index_line[-1])
                        else:
                            word_index[ref_word] = [c_word, word_index_line[-1]]
                    else:

                        my_index, my_int = self.convert_letter(item)
                        word_ref.append(item)
                        if isinstance(my_int, int):
                            word_wrapper.append(my_int)
                        else:
                            if my_index:
                                bb_wrapper.append(my_index)
                            pass
            super_word_index.append(word_index)
            super_booklist.append(selected_book.replace("_lines.txt", "").replace("utilities/", ""))

        return super_word_index, super_booklist, my_data


def f5(seq, idfun=None):
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

def main():
    exit_word = False
    print("inserisci:\n     1 - per conversione classica Ebraico - valori\n     2 - per conversione estesa (le lettere sofit hanno valori di x*100)")
    choice = ""
    while not (choice == "1" or choice == "2"):
        choice = input("\ninserisci solo 1 o 2: ")
    choice = int(choice)
    dictionary = md(choice).make_dictionary()
    # print(dictionary)
    gm = GimValue(dictionary)
    correct = set("אבגדהוּזחטיכךלמםנןסעפףצץקרשת")

    word = input("immetti parola da calcolare e raffrontare;\noppure inserisci il valore numerico desiderato: \n_____\n(oppure scrivi exit per uscire dal programma)\n");
    if word == "exit":
        exit_word = True
    while not exit_word:

        while not (set(word) <= correct or word.isdecimal()):
            print("usare solo caratteri ebraici o numeri arabi, per favore.\n")
            word = input()

        start_watch = timeit.default_timer()
        gim_word = gm.convert_word(word)
        gim_word = sum(gim_word)
        word_array = [word, gim_word]
        c_1 = word_array
        check = set("12345 ")
        choosen_ones = "0"
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
        if my_data.loc["values"] == c_1[1]:
            print(my_data.loc["values"], "matches")
        for n, element in enumerate(word_index):
            print("")
            for k, item in element.items():
                #if item[0] == c_1[1]:
                #    print("word: {}, val: {}, pos: {}, book: {}".format(k.replace("\n", ""), str(item[0]), str(', '.join(item[1:])), book_title[n]))

                pass
        # elapsed = timeit.default_timer() - start_watch
        # print(elapsed)

        word = input("\nimmetti parola da calcolare e raffrontare;\noppure inserisci il valore numerico desiderato: \n_____\n(oppure scrivi exit per uscire dal programma)\n");

        if word == "exit":
            exit_word = True

if __name__ == "__main__":
    main()

