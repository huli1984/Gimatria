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

    def get_Bible_text(self, wanted_book="Bereshit_lines.txt"):
        my_Bible_book = open(wanted_book, "r")
        # importa il libro biblico sotto forma di array di linee
        my_bb = my_Bible_book.readlines()
        word_wrapper = []
        word_ref = []
        word_index = {}
        line_index = []
        line_addresses = []
        ref = set("0123456789: ")
        #analisi delle linee
        for index in range(0, len(my_bb)):
            # analisi delle singole parole
            # print(my_bb[index])
            for i_2 in range(0, len(my_bb[index])):
                item = my_bb[index][i_2]
                if item in ref:
                    line_address = None
                    if not " " in item:
                        # print("presenza di numeri o carattere \":\"", item)
                        line_index.append(item)
                    else:
                        line_address = ''.join(line_index)
                        line_index = []
                        h_index = i_2
                        # print("linea nel testo: ", line_address)
                        for i_3 in range(h_index, len(my_bb[index])):
                            item = my_bb[index][i_3]
                            if " " in item and line_address:
                                # print(item, "item in if \" \"");
                                c_word = sum(word_wrapper)
                                # print(c_word, "c_word");
                                ref_word = "".join(word_ref)
                                # print(ref_word, "ref word")
                                word_wrapper = []
                                word_ref = []
                                word_index[ref_word] = c_word
                                line_addresses.append(line_address)
                            elif line_address:
                                # print(item + " i", end=" ")
                                my_int = self.convert_letter(item)
                                word_ref.append(item)
                                if isinstance(my_int, int):
                                    word_wrapper.append(my_int)
                                else:
                                    # print(item, "item in else")
                                    pass
                            else:
                                # print("nothing to do")
                                pass
        return word_index, line_addresses

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
        elapsed = timeit.default_timer() - start_watch
        # print(elapsed)
        gim_word = sum(gim_word)
        word_array = [word, gim_word]
        c_1 = word_array
        #inserisci libri richiesti per il confronto DEFAULT = Bereshit
        c_2, c_3 = gm.get_Bible_text()

        for k, item in c_2.items():
            if item == c_1[1]:
                # print("my word value: " + str(c_1[1]), "my entered word: " + c_1[0], "found word: " + k, "word's value: " + str(item));
                print("word's value: " + str(item), "found word: " + k)
                pass
        print(c_3)
        word = input("immetti parola da calcolare e raffrontare;\noppure inserisci il valore numerico desiderato: \n_____\n(oppure scrivi exit per uscire dal programma)\n");
        if word == "exit":
            exit_word = True

if __name__ == "__main__":
    main()

