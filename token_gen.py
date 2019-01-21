#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Crypto.Cipher import AES
from base64 import b64encode
from base64 import b64decode
from Crypto.Util.Padding import pad


def ecb_enc(sk, w):
    data = pad(w, AES.block_size)
    _ecb = AES.new(sk, AES.MODE_ECB)
    ct_bytes = _ecb.encrypt(data)
    return ct_bytes


if __name__ == "__main__":

    with open(r'../data/skprf.txt','r') as _sk1_in:
        _sk1 = _sk1_in.read()
        b_sk1 = b64decode(_sk1)
    # token generation
    token_ecb = ecb_enc(b_sk1, 'packers'.encode('utf-8'))
    token_str = b64encode(token_ecb).decode('utf-8')
    with open(r'../data/token.txt', 'w') as token_out:
        token_out.write(token_str)
