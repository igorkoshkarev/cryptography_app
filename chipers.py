from collections import namedtuple
from enum import Enum
import abc
import re
import numpy as np
import random_generators
from keys import *
import random


class AlphabetName(Enum):
    RUSSIAN = 'russian'
    ENGLISH = 'english'
    RUSSIAN_UPPER = 'russian_upper'
    ENGLISH_UPPER = 'english_upper'
    RUSSIAN_AND_ENGLISH = 'russian_english'
    ENGLISH_FULL = 'english_full'
    RUSSIAN_FULL = 'russian_full'
    RUSSIAN_ENGLISH_NUMBERS = 'rus_eng_num'
    SYMBOLS_FOR_BYTE_CODING = '8 bits'

Alphabet = namedtuple("Alphabet", ['name', 'letters', 'length'])

ENGLISH = Alphabet(AlphabetName.ENGLISH, 'abcdefghijklmnopqrstuvwxyz', 26)
ENGLISH_UPPER = Alphabet(AlphabetName.ENGLISH_UPPER, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 26)
FULL_ENGLISH = Alphabet(AlphabetName.ENGLISH_FULL, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 52)
PLAYFAIR_ENGLISH = Alphabet(AlphabetName.ENGLISH, 'abcdefghiklmnopqrstuvwxyz', 25)
RUSSIAN = Alphabet(AlphabetName.RUSSIAN, 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя', 33)
RUSSIAN_UPPER = Alphabet(AlphabetName.RUSSIAN_UPPER, 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 33)
FULL_RUSSIAN= Alphabet(AlphabetName.RUSSIAN_UPPER, 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 66)
PLAYFAIR_RUSSIAN = Alphabet(AlphabetName.RUSSIAN, 'абвгдежзийклмнопрстуфхцчшщъыьэюя', 32)
RUSSIAN_AND_ENGLISH = Alphabet(AlphabetName.RUSSIAN_AND_ENGLISH, 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 118)
RUSSIAN_ENGLISH_NUMBERS = Alphabet(AlphabetName.RUSSIAN_ENGLISH_NUMBERS, 'abcdefghijklmnopqrstuvwxyzабвгдежзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890 .', 128)
SYMBOLS_FOR_BYTE_CODING = Alphabet(AlphabetName.SYMBOLS_FOR_BYTE_CODING, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀĂ", 256)


class Chiper(abc.ABC):
    
    def __init__(self):
        pass

    @abc.abstractmethod
    def encrypt(self, text, key):
        pass
    
    @abc.abstractmethod
    def decrypt(self, text, key):
        pass


class Atbash(Chiper):

    def __init__(self):    
        self.alphabets = [ENGLISH, ENGLISH_UPPER, RUSSIAN, RUSSIAN_UPPER]
    
    def _atbash(self, text: str) -> str:
        encrypt_text = ""
        for i in text:
            for alphabet in self.alphabets:
                if i in alphabet.letters:
                    letter_index = alphabet.letters.index(i)
                    encrypt_text += alphabet.letters[alphabet.length - (letter_index+1)]
                    break
            else:
                encrypt_text += i
        return encrypt_text
    
    def encrypt(self, text: str, key="") -> str:
        return self._atbash(text)
    
    def decrypt(self, text: str, key="") -> str:
        return self._atbash(text)


class Caesar(Chiper):

    def __init__(self):
        self.alphabets = [ENGLISH, ENGLISH_UPPER, RUSSIAN, RUSSIAN_UPPER]
    
    def encrypt(self, text: str, key: int) -> str:
        encrypt_text = ""
        for i in text:
            for alphabet in self.alphabets:
                if i in alphabet.letters:
                    letter_index = alphabet.letters.index(i)
                    encrypt_text += alphabet.letters[(letter_index+key) % alphabet.length]
                    break
            else:
                encrypt_text += i
        return encrypt_text
    
    def decrypt(self, text, key):
        decrypt_text = ""
        for i in text:
            for alphabet in self.alphabets:
                if i in alphabet.letters:
                    letter_index = alphabet.letters.index(i)
                    decrypt_text += alphabet.letters[(letter_index-key) % alphabet.length]
                    break
            else:
                decrypt_text += i
        return decrypt_text


class Rishelie(Chiper):

    def __init__(self):
        pass
    
    def encrypt(self, text, key):
        encrypt_text = ""
        base_index = 0
        assert re.fullmatch(r'(\((\d,?)+\))*', key), "Ваш ключ не подходит под шаблон."
        groups = re.split(r',\)\(|\)\(|\(|\)', key)
        for group in groups[1:-1]:
            nums = group.split(',')
            used_nums = set()
            for i in range(len(nums)):
                number = int(nums[i])-1
                assert 0 <= number < len(nums), 'Внутри группы у ключа неверные значения'
                assert base_index+number < len(text), 'Ваш ключ длиннее сообщения'
                assert number not in used_nums, 'Внутри группы у ключа обнаружены дубликаты'
                encrypt_text += text[base_index+number]
                used_nums.add(number)
            base_index += len(nums)
        for i in range(base_index, len(text)):
            encrypt_text += text[i]
        return encrypt_text
    
    def decrypt(self, text, key):
        decrypt_text = ""
        base_index = 0
        assert re.fullmatch(r'(\((\d,?)+\))*', key), "Ваш ключ не подходит под шаблон."
        groups = re.split(r',\)\(|\)\(|\(|\)', key)
        for group in groups[1:-1]:
            nums = group.split(',')
            decrypt = list(range(len(nums)))
            used_nums = set()
            for i in range(len(nums)):
                number = int(nums[i])-1
                assert 0 <= number < len(nums), 'Внутри группы у ключа неверные значения'
                assert base_index+number < len(text), 'Ваш ключ длиннее сообщения'
                assert number not in used_nums, 'Внутри группы у ключа обнаружены дубликаты'
                decrypt[number] = text[base_index+i]
                used_nums.add(number)
            base_index += len(nums)
            decrypt_text += ''.join(decrypt)
        for i in range(base_index, len(text)):
            decrypt_text += text[i]
        return decrypt_text


class Gronsfeld(Chiper):

    def __init__(self):
        self.alphabets = [ENGLISH, RUSSIAN, ENGLISH_UPPER, RUSSIAN_UPPER]

    def _key_is_valid(self, key):
        return key.isnumeric()

    def encrypt(self, text, key):
        encrypt_text = ""
        
        assert self._key_is_valid(key), "Ваш ключ содержит символы, которые не являются цифрами"

        for ind, letter in enumerate(text):
            key_num = int(key[ind % len(key)])
            for alphabet in self.alphabets:
                if letter in alphabet.letters:
                    ind_letter = alphabet.letters.index(letter)
                    encrypt_text += alphabet.letters[(ind_letter + key_num) % alphabet.length]
                    break
            else:
                encrypt_text += letter

        return encrypt_text
    
    def decrypt(self, text, key):
        decrypt_text = ""
        
        assert self._key_is_valid(key), "Ваш ключ содержит символы, которые не являются цифрами"
        
        for ind, letter in enumerate(text):
            key_num = int(key[ind % len(key)])
            for alphabet in self.alphabets:
                if letter in alphabet.letters:
                    ind_letter = alphabet.letters.index(letter)
                    decrypt_text += alphabet.letters[(ind_letter - key_num) % alphabet.length]
                    break
            else:
                decrypt_text += letter

        return decrypt_text


class Vigenere(Chiper):

    def __init__(self):
        self.alphabet = RUSSIAN_AND_ENGLISH

    def _key_is_valid(self, key):
        return key.isalpha()
    
    def encrypt(self, text, key):
        encrypt_text = ""

        assert self._key_is_valid(key), "Ключ содержит цифры или спец. символы."

        for ind, letter in enumerate(text):
            ind_k = self.alphabet.letters.index(key[ind % len(key)])
            if letter in self.alphabet.letters:
                ind_i = self.alphabet.letters.index(letter)
                encrypt_text += self.alphabet.letters[(ind_i + ind_k) % self.alphabet.length]
            else:
                encrypt_text += letter

        return encrypt_text
    
    def decrypt(self, text, key):
        decrypt_text = ""
        
        assert self._key_is_valid(key), "Ключ содержит цифры."
            
        for ind, letter in enumerate(text):
            ind_k = self.alphabet.letters.index(key[ind % len(key)])
            if letter in self.alphabet.letters:
                ind_i = self.alphabet.letters.index(letter)
                decrypt_text += self.alphabet.letters[(ind_i - ind_k) % self.alphabet.length]
            else:
                decrypt_text += letter
        
        return decrypt_text


class Playfair(Chiper):
    
    def __init__(self):
        pass
    
    def _create_playfair_matrix(self, key):
        lang = self._get_string_lang(key)
        if lang == PLAYFAIR_ENGLISH.name:
            alphabet = PLAYFAIR_ENGLISH
            shape = (5,5)
        elif lang == PLAYFAIR_RUSSIAN.name:
            alphabet = PLAYFAIR_RUSSIAN
            shape = (4,8)
        chiper_matrix = np.array(list(key) + sorted(set(alphabet.letters) - set(key)))
        chiper_matrix = chiper_matrix.reshape(shape)
        return chiper_matrix
    
    def _get_string_lang(self, string):
        if not string:
            return RUSSIAN_AND_ENGLISH.name
        is_english = False
        is_russian = False
        for i in string:
            if i in FULL_ENGLISH.letters:
                is_english = True
            elif i in FULL_RUSSIAN.letters:
                is_russian = True
            if is_english and is_russian:
                return RUSSIAN_AND_ENGLISH.name
        return ENGLISH.name if is_english else RUSSIAN.name

    def _key_is_valid(self, key):
        key = key.lower()
        return key.isalpha() and len(key) == len(set(key)) and self._get_string_lang(key) != RUSSIAN_AND_ENGLISH.name
    
    def _text_is_valid(self, text):
        text = text.replace(' ', '')
        return text.isalpha() and self._get_string_lang(text) != RUSSIAN_AND_ENGLISH.name
    
    def _format_data(self, data):
        data = data.lower()
        data = data.replace(' ', '')
        data = data.replace('j', 'i')
        data = data.replace('ё', 'е')
        return data
    
    def _get_bigrams(self, text):
        if self._get_string_lang(text) == PLAYFAIR_ENGLISH.name:
            spacer = 'x'
            another_spacer = 'q'
        elif self._get_string_lang(text) == PLAYFAIR_RUSSIAN.name:
            spacer = 'ъ'
            another_spacer = 'ь'
        else:
            raise AssertionError
        error = True
        bigrams = []
        base_index = 0
        while error:
            error = False
            for i in range(base_index, len(text), 2):
                if i == len(text)-1:
                    if text[i] != spacer:
                        b = text[i] + spacer
                    else:
                        b = text[i] + another_spacer
                elif text[i] == text[i+1]:
                    if text[i] != spacer:
                        b = text[i] + spacer
                        text = text[:i+1] + spacer + text[i+1:]
                    else:
                        b = text[i] + another_spacer
                        text = text[:i+1] + another_spacer + text[i+1:]
                    error = True
                else:
                    b = text[i] + text[i+1]
                
                base_index += 2
                bigrams.append(b)
                if error:
                    break
        return bigrams
    
    def encrypt(self, text, key):
        encrypt_text = ""

        assert self._key_is_valid(key), "Ваш ключ неверный"
        assert self._text_is_valid(text), "Ваш текст не подходит для шифровки"
        assert self._get_string_lang(key) == self._get_string_lang(text), "Язык вашего ключа не совпадает с языком текста"
        
        key = self._format_data(key)
        text = self._format_data(text)

        matrix = self._create_playfair_matrix(key)
        print(matrix)
        bigrams = self._get_bigrams(text)
        print(bigrams)
        for bigram in bigrams:
            shape = matrix.shape
            first_letter = bigram[0]
            pos_first = np.where(matrix == first_letter)
            pos_first = (int(pos_first[0]), int(pos_first[1]))

            second_letter = bigram[1]
            pos_second = np.where(matrix == second_letter)
            pos_second = (int(pos_second[0]), int(pos_second[1]))

            if pos_first[0] == pos_second[0]:
                pos_first, pos_second = (pos_first[0], (pos_first[1]+1) % shape[1]), (pos_second[0], (pos_second[1]+1) % shape[1])
            elif pos_first[1] == pos_second[1]:
                pos_first, pos_second = ((pos_first[0]+1) % shape[0], pos_first[1]), ((pos_second[0]+1) % shape[0], pos_second[1])
            else:
                pos_first, pos_second = (pos_first[0], pos_second[1]), (pos_second[0], pos_first[1])
            
            print(pos_first, pos_second)
            encrypt_text += matrix[pos_first[0]][pos_first[1]]
            encrypt_text += matrix[pos_second[0]][pos_second[1]]
        
        return encrypt_text
    
    def decrypt(self, text, key):
        decrypt_text = ""

        assert self._key_is_valid(key), "Ваш ключ неверный"
        assert self._text_is_valid(text), "Ваш текст не подходит для шифровки"
        assert self._get_string_lang(key) == self._get_string_lang(text), "Язык вашего ключа не совпадает с языком текста"
        
        key = self._format_data(key)
        text = self._format_data(text)

        matrix = self._create_playfair_matrix(key)
        print(matrix)
        bigrams = self._get_bigrams(text)
        print(bigrams)
        for bigram in bigrams:
            shape = matrix.shape
            first_letter = bigram[0]
            pos_first = np.where(matrix == first_letter)
            pos_first = (int(pos_first[0]), int(pos_first[1]))

            second_letter = bigram[1]
            pos_second = np.where(matrix == second_letter)
            pos_second = (int(pos_second[0]), int(pos_second[1]))

            if pos_first[0] == pos_second[0]:
                pos_first, pos_second = (pos_first[0], (pos_first[1]-1) % shape[1]), (pos_second[0], (pos_second[1]-1) % shape[1])
            elif pos_first[1] == pos_second[1]:
                pos_first, pos_second = ((pos_first[0]-1) % shape[0], pos_first[1]), ((pos_second[0]-1) % shape[0], pos_second[1])
            else:
                pos_first, pos_second = (pos_first[0], pos_second[1]), (pos_second[0], pos_first[1])

            decrypt_text += matrix[pos_first[0]][pos_first[1]]
            decrypt_text += matrix[pos_second[0]][pos_second[1]]
        
        return decrypt_text


class Gamming(Chiper):

    def __init__(self):
        self.alphabet = RUSSIAN_ENGLISH_NUMBERS

    def _text_is_valid(self, text):
        for i in text:
            if i not in self.alphabet.letters:
                return False
        return True
    
    def gamming(self, text, key):
        encrypt_text = ""

        rand_generator = random_generators.LinearCongruentialGenerator(*key)
        assert self._text_is_valid(text), "В используемом алфавите нет символов которые есть в тексте."

        for ind, letter in enumerate(text):
            ind_k = self.alphabet.letters.index(letter) ^ rand_generator.get_random_number_on_range(0, self.alphabet.length-1)
            encrypt_text += self.alphabet.letters[ind_k]

        return encrypt_text
    
    def encrypt(self, text, key):
        return self.gamming(text, key)
    
    def decrypt(self, text, key):      
        return self.gamming(text, key)

class GammingFile(Chiper):
    
    def gamming(self, text, key):
        encrypt_text = []

        rand_generator = random_generators.LinearCongruentialGenerator(*key)

        for letter_code in text:
            encrypt_text.append(letter_code ^ int(bin(rand_generator.get_random_number_on_range(0, 2**8-1)), base=2))

        return encrypt_text
    
    def encrypt(self, text, key):
        return self.gamming(text, key)
    
    def decrypt(self, text, key):      
        return self.gamming(text, key)

class DES(Chiper):

    IP = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17,  9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    FP = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41,  9, 49, 17, 57, 25
    ]

    E = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    P = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]
    S = [
        [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],

        [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],

        [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],

        [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],

        [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],

        [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],

        [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],

        [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
    ]
    
    def _permutation(self, table, value, size):
        res = 0
        for pos in table:
            res = (res << 1) | (value >> (size - pos)) & 1
        return res
    
    def _feisteil(self, R, key):
        R = self._permutation(self.E, R, 32)
        R = R ^ key
        res = 0
        for i in range(8):
            six_bits = (R >> (42-(i*6))) & 0b111111
            row = ((six_bits & 0b100000) >> 4) | (six_bits & 1)
            col = (six_bits >> 1) & 0b01111
            four_bit = self.S[i][row][col]
            res = (res << 4) | four_bit
        res = self._permutation(self.P, res, 32)
        return res
    
    def string_to_bit_array(self, text):
        return int.from_bytes(text.encode(), 'big')
    
    def bits_to_string(self, bits, length):
        return bits.to_bytes(length, 'big').decode(errors='ignore')

    def encrypt(self, text, key):
        k = DESKey()
        if key == -1:
            init_key = None
        else:
            init_key = key
        keys = k.gen(init_key)
        text_bytes = self.string_to_bit_array(text)

        T_arr = []

        while text_bytes:
            K = 0
            K = self._permutation(self.IP, text_bytes, 64)
            L = (K >> 32) & 0xFFFFFFFF
            R = K & 0xFFFFFFFF
            
            for i in range(16):
                tmp_R = R
                tmp_L = L
                L = tmp_R
                R = tmp_L ^ self._feisteil(tmp_R, keys[i])
            
            T = (R << 32) | L
            T = self._permutation(self.FP, T, 64)
            T_arr.append(T)

            text_bytes >>= 64
        
        return " ".join(map(str, T_arr))


    def decrypt(self, text, key):
        k = DESKey()
        if key == -1:
            init_key = None
        else:
            init_key = key
        keys = k.gen(init_key)
        
        keys = list(reversed(keys))

        enc_text = ""

        for block in text.split():
            block = int(block)

            while block:
                K = 0
                K = self._permutation(self.IP, block, 64)
                L = (K >> 32) & 0xFFFFFFFF
                R = K & 0xFFFFFFFF
                
                for i in range(16):
                    tmp_R = R
                    tmp_L = L
                    L = tmp_R
                    R = tmp_L ^ self._feisteil(tmp_R, keys[i])
                
                T = (R << 32) | L
                T = self._permutation(self.FP, T, 64)

                length = (T.bit_length() + 7) // 8
                enc_text = self.bits_to_string(T, length) + enc_text

                block >>= 64
        
        return enc_text
    

class DESFile(DES):

    def string_to_bit_array(self, text):
        return int.from_bytes(text, 'big')
    
    def encrypt(self, text, key):
        k = DESKey()
        if key == -1:
            init_key = None
        else:
            init_key = key
        keys = k.gen(init_key)
        text_bytes = self.string_to_bit_array(text)

        res = []
        c = 0

        while text_bytes:
            K = 0
            K = self._permutation(self.IP, text_bytes, 64)
            L = (K >> 32) & 0xFFFFFFFF
            R = K & 0xFFFFFFFF
            
            for i in range(16):
                tmp_R = R
                tmp_L = L
                L = tmp_R
                R = tmp_L ^ self._feisteil(tmp_R, keys[i])
            
            T = (R << 32) | L
            T = self._permutation(self.FP, T, 64)
            for i in range(8):
                b = T & 0b11111111
                res = [b] + res
                T >>= 8
            text_bytes >>= 64
        
        return res


    def decrypt(self, text, key):
        k = DESKey()
        if key == -1:
            init_key = None
        else:
            init_key = key
        keys = k.gen(init_key)
        
        keys = list(reversed(keys))

        text_bytes = self.string_to_bit_array(text)

        res = []

        while text_bytes:
            K = 0
            K = self._permutation(self.IP, text_bytes, 64)
            L = (K >> 32) & 0xFFFFFFFF
            R = K & 0xFFFFFFFF
            
            for i in range(16):
                tmp_R = R
                tmp_L = L
                L = tmp_R
                R = tmp_L ^ self._feisteil(tmp_R, keys[i])
            
            T = (R << 32) | L
            T = self._permutation(self.FP, T, 64)
            if text_bytes >> 64 == 0:
                length = (T.bit_length() + 7) // 8
            else:
                length = 8
            for i in range(length):
                b = T & 0b11111111
                res = [b] + res
                T >>= 8
            text_bytes >>= 64
        
        return res


class RSA(Chiper):
    
    def __init__(self):
        super().__init__()
        self.alphabet = RUSSIAN_ENGLISH_NUMBERS


    def encrypt(self, text, key):
        n, e = key
        encrypted_text = []
        for i in text:
            index = self.alphabet.letters.index(i)
            print(index, e, n)
            enc = pow(index, e, n)
            encrypted_text.append(str(enc))
        return ' '.join(encrypted_text)
        

    def decrypt(self, text, key):
        text = text.split(' ')
        n, d = key
        decrypted_text = ""
        for i in text:
            print(i, d, n)
            enc = pow(int(i), d, n)
            decrypted_text += self.alphabet.letters[enc]
        return decrypted_text
        

class DH(Chiper):
    
    def __init__(self):
        super().__init__()
        self.alphabet = RUSSIAN_ENGLISH_NUMBERS


    def encrypt(self, text, key):
        A, b, p = key
        text = int(text.strip())
        encrypted_text = pow(A, b, p)
        return str(encrypted_text)
        

    def decrypt(self, text, key):
        B, a, p = key
        text = int(text.strip())
        decrypted_text = pow(B, a, p)
        return str(decrypted_text)
        

if __name__ == '__main__':
    a = RSA()
    sdfsdf = 1234
    n = 859420
    e = 853
    d = 840277

    print((e * d) % n)

    sdfsdf = pow(sdfsdf, e, n)
    print(sdfsdf)
    sdfsdf = pow(sdfsdf, d, n)
    print(sdfsdf)