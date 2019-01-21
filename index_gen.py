#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from collections import defaultdict
import datetime


def create_index(data):
    d = defaultdict(list)
    for key, val in data:
        d[val].append(key)
    return d


if __name__ == "__main__":
    """
    Given the encrypted files and their encrypted keywords, to generate the inverted index
    """
    begin_time = datetime.datetime.now()
    cipher_path = r"../data/ciphertextfiles"
    files = os.listdir(cipher_path)
    token_index = {}
    initial_index = []
    for file in files:
        file_name = file[0:-4]
        words = ""
        if not os.path.isdir(file):
            with open(cipher_path + '/' + file, 'r') as read_txt:
                lines = read_txt.readline()
            for i in range(0, lines.__len__(), 1):
                if lines[i] != '\t':
                    words = words + lines[i]
                else:
                    item = (file_name, words)
                    initial_index.append(item)
                    words = ""
    abc = create_index(initial_index) # create the inverted index
    for k, v in abc.items():  #write the inverted index into text file
        with open(r'../data/index.txt', 'a') as token_in:
            token_in.write(k)
            token_in.write('\t')
        for item in v:
            with open(r'../data/index.txt', 'a') as file_in:
                file_in.write(item)
                file_in.write('\t')
        with open(r'../data/index.txt', 'a') as n_in:
            n_in.write('\n')

    end_time = datetime.datetime.now()
    running_time = end_time - begin_time
    print('running_time_of_index_gen: ', running_time)