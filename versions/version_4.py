#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import timeit
import os
from MyDict import MyDict as md
import PyQt5


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
                # print(str(j))
                gim_word.append(int(j))
        return gim_word

    def convert_letter(self, w):
        j = self.dic_conv(w)
        return j

    def get_Bible_text(self, selected_book="utilities/Bereshit_lines.txt"):
        my_Bible_book = open(selected_book, "r")
        my_bb_line = my_Bible_book.readlines()

        word_wrapper = []
        word_ref = []
        word_index = {}

        for item in my_bb:
            # print(item + "item in root")
            if " " in item:
                # print(item, "item in if \" \"");
                c_word = sum(word_wrapper)
                # print(c_word, "c_word");
                ref_word = "".join(word_ref)
                # print(ref_word, "ref word")
                word_wrapper = []
                word_ref = []
                word_index[ref_word] = c_word
            else:
                # print(item + " i", end=" ")
                my_int = self.convert_letter(item)
                word_ref.append(item)
                if isinstance(my_int, int):
                    word_wrapper.append(my_int)
                else:
                    pass
        return word_index


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
        elapsed = timeit.default_timer() - start_watch
        # print(elapsed)
        gim_word = sum(gim_word)
        word_array = [word, gim_word]
        c_1 = word_array
        input("in quali libri biblici effettuare la ricerca:"\
              "\n1- Bereshit\n2- Shemot\n3\n\n")
        c_2 = gm.get_Bible_text()

        for k, item in c_2.items():
            ref = "\n"
            if item == c_1[1]:
                #print("my word value: " + str(c_1[1]), "my entered word: " + c_1[0], "found word: " + k, "word's value: " + str(item));
                if str(k[-1]) in ref:
                    l = k.replace("\n", "")
                    print(str(l))
                else:
                    print(str(k))
                #print("word's value: " + str(item), "found word: " + k)
                pass
        word = input("\nimmetti parola da calcolare e raffrontare;\noppure inserisci il valore numerico desiderato: \n_____\n(oppure scrivi exit per uscire dal programma)\n");
        if word == "exit":
            exit_word = True

if __name__ == "__main__":
    main()

