#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import timeit
import os
from MyDict import MyDict as md


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
        print(gim_word)
        return gim_word

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

        return super_word_index, super_booklist


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

            print(choosen_ones, "choosen ones")
            print(choosen_ones[0])
            # choosen_ones = f5(choosen_ones)
            for c in choosen_ones:
                if c.strip() in "12345":
                    ok = True
                else:
                    print(c.strip(), choosen_ones)
                    choosen_ones = input("\nin quali libri biblici effettuare la ricerca:" \
                                         "\n1- Bereshit\n2- Shemot\n3- Vaykra\n4- Bamidbar\n5- Devarim\n" \
                                         "Inserire i numeri dei libri desiderati separati da uno spazio.\n")
                    ok = False
                    choosen_ones = choosen_ones.split()

        selected_books = gm.choosen_books(choosen_ones)
        word_index, book_title = gm.get_Bible_text(selected_books)
        for n, element in enumerate(word_index):
            print("")
            for k, item in element.items():
                if item[0] == c_1[1]:
                    print("word: {}, val: {}, pos: {}, book: {}".format(k.replace("\n", ""), str(item[0]), str(', '.join(item[1:])), book_title[n]))

        # elapsed = timeit.default_timer() - start_watch
        # print(elapsed)

        word = input("\nimmetti parola da calcolare e raffrontare;\noppure inserisci il valore numerico desiderato: \n_____\n(oppure scrivi exit per uscire dal programma)\n");

        if word == "exit":
            exit_word = True

if __name__ == "__main__":
    main()

