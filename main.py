#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import timeit
import os


def dic_conv(argument):
    switcher = {"א": 1,
                "ב": 2,
                "ג": 3,
                "ד": 4,
                "ה": 5,
                "ו": 6,
                "ז": 7,
                "ח": 8,
                "ט": 9,
                "י": 10,
                "כ": 20,
                "ך": 20,
                "ל": 30,
                "מ": 40,
                "ם": 40,
                "נ": 50,
                "ן": 50,
                "ס": 60,
                "ע": 70,
                "פ": 80,
                "ף": 80,
                "צ": 90,
                "ץ": 90,
                "ק": 100,
                "ר": 200,
                "ש": 300,
                "ת": 400
                }
    # print(switcher.get(argument, "invalid char"));
    return switcher.get(argument, lambda: "invalid character: use only hebrew characters.");


def main():
    word = input("immetti parola da calcolare e raffrontare;\noppure inserisci il valore numerico desiderato: \n_____\n");
    start_watch = timeit.default_timer();
    gim_word = convert_word(word);
    elapsed = timeit.default_timer() - start_watch;
    print(elapsed);
    gim_word = sum(gim_word);
    #print(str(gim_word) + " gim_word");
    word_array = [word, gim_word];
    return word_array;


def convert_word(word):
    gim_word = [];
    correct = set("אבגדהוּזחטיכךלמםנןסעפףצץקרשת");
    # print(word);
    if set(word) <= correct:
        for i in word:
            j = dic_conv(i);
            #print(str(j))
            gim_word.append(int(j));
    else:
        if word.isdecimal:
            gim_word.append(int(word));
            gim_word.append(0);
        else:
            print("usare solo caratteri ebraici o numeri arabi, per favore.\n");
            main();
    return gim_word;


def convert_letter(w):
    j = dic_conv(w);
    return j;


def get_Bible_text():
    my_Bible_book = open("Bereshit.txt", "r", encoding="utf8");
    my_bb = my_Bible_book.read();
    word_wrapper = [];
    word_ref = [];
    word_index = {};
    for item in my_bb:
        #print(item + "item in root")
        if " " in item:
            #print(item, "item in if \" \"");
            c_word = sum(word_wrapper);
            ref_word = "".join(word_ref);
            word_wrapper = [];
            word_ref = [];
            word_index[ref_word] = c_word;
        else:
            my_int = convert_letter(item);
            word_ref.append(item);
            if isinstance(my_int, int):
                word_wrapper.append(my_int);
            else:
                #print(item, "item in else")
                pass;
    return word_index;


c_1 = main();
c_2 = get_Bible_text();
print(c_2)

for k, item in c_2.items():
    if item == c_1[1]:


        #print("my word value: " + str(c_1[1]), "my entered word: " + c_1[0], "found word: " + k, "word's value: " + str(item));

        print("word's value: " + str(item), "found word: " + k);

