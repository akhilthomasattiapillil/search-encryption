#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Crypto.Cipher import AES
from base64 import b64decode
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import datetime

def cbc_dec(sk, iv, ciphertxt):
    _cbc = AES. new(sk, AES.MODE_CBC, iv)
    # decd = unpad(_cbc.decrypt(ciphertxt), AES.block_size)
    decd = _cbc.decrypt(ciphertxt)
    return decd


def ecb_dec(sk, ciphertxt):
    _ecb = AES.new(sk,AES.MODE_ECB)
    decd = unpad(_ecb.decrypt(ciphertxt), AES.block_size)
    return decd


def cbc_enc(sk, iv, text):
    data = pad(text, AES.block_size)
    _cbc = AES.new(sk, AES.MODE_CBC, iv)
    ct_bytes = _cbc.encrypt(data)
    return ct_bytes


if __name__ == "__main__":
    """
    Given a token, to search the selected token among these encrypted files and output its corresponding files
    """
    with open(r'../data/token.txt', 'r') as token_in:
        token = token_in.read()
    total_file = []
    file_names = []
    begin_time = datetime.datetime.now()
    with open(r'../data/index.txt', 'r') as index_in:
        while 1: # given a token, find the corresponding file names
            lines = index_in.readline()
            if not lines:
                break
            words = ""
            for i in range(0, lines.__len__(), 1):
                if lines[i] != '\t':
                    words = words + lines[i]
                if lines[i] == '\t' or i == lines.__len__() - 1:
                    if words == token:
                        total_file = lines[i+1:]
                        break
                    else:
                        continue
    name = ''
    total_file = total_file.strip()
    for i in range(0, total_file.__len__(), 1):
        if total_file[i] != '\t':
            name = name + total_file[i]
        if total_file[i] == '\t' or i == total_file.__len__()-1:
            i = i+2
            name = name.strip('\n')
            file_names.append(name)
            name = ''

    with open(r'../data/iv.txt', 'r') as _iv_in:
        _iv = _iv_in.read()
        b_iv = b64decode(_iv)
    with open(r'../data/skprf.txt', 'r') as _sk1_in:
        _sk1 = _sk1_in.read()
        b_sk1 = b64decode(_sk1)
    cipher_w = ''
    for f in file_names: # decrypt the corresponding keywords and write them into result.txt
        with open(r'../data/result.txt', 'a') as result_in:
            result_in.write(f)
            result_in.write('.txt\t')
            with open(r'../data/ciphertextfiles' + '/' + f + '.txt', 'r') as text_in:
                lines = text_in.readline()
                for i in range(0, lines.__len__(), 1):
                    if lines[i] != '\t':
                        cipher_w = cipher_w + lines[i]
                    if lines[i] == '\t' or i == lines.__len__() - 1:
                        b_words = b64decode(cipher_w)
                        b_txt = ecb_dec(b_sk1, b_words)
                        txt = b_txt.decode('utf-8')
                        cipher_w = ''
                        result_in.write(txt)
                        result_in.write('\t')
                result_in.write('\n')
    end_time = datetime.datetime.now()
    running_time = end_time - begin_time
    print('running_time_of_search: ', running_time)