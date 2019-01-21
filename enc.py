#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode
from Crypto.Util.Padding import pad
import datetime
import os


def encode(s):
    return ''.join([bin(ord(c)).replace('0b', '') for c in s])


def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])


def ecb_enc(sk, w):
    data = pad(w, AES.block_size)
    _ecb = AES.new(sk, AES.MODE_ECB)
    ct_bytes = _ecb.encrypt(data)
    return ct_bytes


def cbc_enc(sk, iv, name):
    data = pad(name, AES.block_size)
    _cbc = AES.new(sk, AES.MODE_CBC, iv)
    ct_bytes = _cbc.encrypt(data)
    return ct_bytes


if __name__ == "__main__":
    """
    To generate secret keys. At the same time, it encrypts keywords and the file names
    """
    #generate secret keys and iv
    _sk1 = get_random_bytes(32)
    _sk2 = get_random_bytes(32)
    _iv = get_random_bytes(16)
    begin_time = datetime.datetime.now()
    plain_path = r'../data/files'
    cipher_path = r"../data/ciphertextfiles"
    files = os.listdir(plain_path) # read the original files and the corresponding keywords
    for file in files:
        file_name = file[0:-4]
        print(file_name)
        file_cipher = cbc_enc(_sk2, _iv, file_name.encode('utf-8'))# encrypt the file name
        f_str = b64encode(file_cipher).decode('utf-8')
        f = encode(f_str)
        cipherwords = []
        words = ""
        if not os.path.isdir(file):
            with open(plain_path + '/' + file, 'r') as read_txt:
                lines = read_txt.readline()
            for i in range(0, lines.__len__(), 1):
                if lines[i] != ' ':
                    words = words + lines[i]
                if lines[i] == ' ' or i == lines.__len__()-1:

                    ecb = ecb_enc(_sk1, words.encode('utf-8')) #encrypt keywords
                    print(ecb, '\n')
                    ecb_str = b64encode(ecb).decode('utf-8')
                    with open(cipher_path + '/' + f + '.txt', 'a') as write_encd:
                        write_encd.write(ecb_str)
                        write_encd.write('\t')
                    words = ""
    end_time = datetime.datetime.now()
    running_time = end_time - begin_time
    print('running_time_of_enc: ', running_time)
# write secret keys and iv into txt files#
    _iv_str = b64encode(_iv).decode('utf-8')
    _sk_str1 = b64encode(_sk1).decode('utf-8')
    _sk_str2 = b64encode(_sk2).decode('utf-8')
    with open(r'../data/iv.txt', 'w') as _iv_in:
        _iv_in.write(_iv_str)
    with open(r'../data/skaes.txt', 'w') as _key_in:
        _key_in.write(_sk_str2)
    with open(r'../data/skprf.txt', 'w') as _key_in:
        _key_in.write(_sk_str1)

