from collections import namedtuple
from enum import Enum
import abc
import re
import numpy as np
import random_generators

class AlphabetName(Enum):
    RUSSIAN = 'russian'
    ENGLISH = 'english'
    RUSSIAN_UPPER = 'russian_upper'
    ENGLISH_UPPER = 'english_upper'
    RUSSIAN_AND_ENGLISH = 'russian_english'
    ENGLISH_FULL = 'english_full'
    RUSSIAN_FULL = 'russian_full'
    RUSSIAN_ENGLISH_NUMBERS = 'rus_eng_num'

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

    def __init__(self):
        self.alphabet = RUSSIAN_ENGLISH_NUMBERS

    def _text_is_valid(self, text):
        for i in text:
            if i not in self.alphabet.letters:
                return False
        return True
    
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