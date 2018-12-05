#!usr/bin/env python
# coding=utf-8

"""
@company:
@version: ??
@author: linwl
@file: desTools.py
@time: 2017/8/2 9:13
@function：Des加密模块
"""

from pyDes import *
import binascii
import random
import string

key = "G3z(thhhh"
token_key = 'eNBrpdlf'

class DesTools(object):

    @staticmethod
    def encrypt(data):
        '''
        对字符串进行加密
        :param data:
        :return:
        '''
        try:
            key_ascii = key.encode('ascii')
            iv = key.encode('ascii')
            k = des(key_ascii, CBC, iv, pad=None, padmode=PAD_PKCS5)
            d = k.encrypt(data)
            print("Encrypted: %r" % binascii.hexlify(d))
            return binascii.hexlify(d)
        except Exception as e:
            raise e

    @staticmethod
    def decrypt(data):
        '''
        对密文进行解密成字符串
        :param data:
        :return:
        '''
        try:
            iv = key.encode('ascii')
            key_ascii = key.encode('ascii')
            t = binascii.unhexlify(data)
            k = des(key_ascii, CBC, iv, pad=None, padmode=PAD_PKCS5)
            d = k.decrypt(t)
            print ("Decrypted: %r" % d)
            return d
        except Exception as e:
            raise e

    @staticmethod
    def custom_decrypt(data,salt):
        '''
        对自定义salt密文进行解密成字符串
        :param data:
        :return:
        '''
        try:
            iv = salt.encode('ascii')
            key_ascii = salt.encode('ascii')
            t = binascii.unhexlify(data)
            k = des(key_ascii, CBC, iv, pad=None, padmode=PAD_PKCS5)
            d = k.decrypt(t)
            print("Decrypted: %r" % d)
            return d
        except Exception as e:
            raise e

    @staticmethod
    def custom_encrypt(data,salt):
        '''
        对字符串进行自定义salt加密
        :param data:
        :return:
        '''
        try:
            key_ascii = salt.encode('ascii')
            iv = salt.encode('ascii')
            k = des(key_ascii, CBC, iv, pad=None, padmode=PAD_PKCS5)
            d = k.encrypt(data)
            print("Encrypted: %r" % binascii.hexlify(d))
            return binascii.hexlify(d)
        except Exception as e:
            raise e

    @staticmethod
    def create_salt():
        '''
        随机生成密码存储salt
        :return:
        '''
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return salt

    @staticmethod
    def encrypt_keyType(data,keyType ='api'):
        '''
        根据key类型对字符串进行加密
        :param data:
        :return:
        '''
        try:
            key_ascii, iv=DesTools.__create_ivkey_ascii(keyType)
            k = des(key_ascii, CBC, iv, pad=None, padmode=PAD_PKCS5)
            d = k.encrypt(data)
            print("Encrypted: %r" % binascii.hexlify(d))
            return binascii.hexlify(d)
        except Exception as e:
            raise e

    @staticmethod
    def decrypt_keyType(data,keyType='api'):
        '''
        根据key类型对密文进行解密成字符串
        :param data:
        :return:
        '''
        try:
            key_ascii, iv = DesTools.__create_ivkey_ascii(keyType)
            t = binascii.unhexlify(data)
            k = des(key_ascii, CBC, iv, pad=None, padmode=PAD_PKCS5)
            d = k.decrypt(t)
            print("Decrypted: %r" % d)
            return d
        except Exception as e:
            raise e

    @staticmethod
    def __create_ivkey_ascii(keyType):
        if keyType == 'token':
            key_ascii = token_key.encode('ascii')
            iv = token_key.encode('ascii')
        elif keyType == 'api':
            key_ascii = key.encode('ascii')
            iv = key.encode('ascii')
        return key_ascii,iv