import random
from random import getrandbits


class Key:

    def __init__(self, *args, **kwargs):
        pass

    def gen(self, *args, **kwargs):
        pass


class DESKey(Key):

    TABLE_FOR_KEY_PERM_C0 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36]
    TABLE_FOR_KEY_PERM_D0 = [63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

    TABLE_FOR_BYTE_SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    TABLE_FOR_FINAL_PERM = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
                            26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
                            51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
                            

    def __init__(self):
        super().__init__()

    def gen_init_key(self):
        return getrandbits(56)
    
    def _count_ones(self, num):
        n = 0
        while num:
            if num % 2:
                n += 1
            num >>= 1
        return n
    
    def _expand_to_64(self, key):
        res = 0
        for i in range(8):
            seven_bits = key & 0b1111111
            key >>= 7
            if self._count_ones(seven_bits) % 2:
                seven_bits <<= 1
            else:
                seven_bits <<= 1
                seven_bits |= 1
            res = seven_bits << i*8 | res
        return res
    
    def _permutation(self, table, value, size):
        res = 0
        for pos in table:
            res |= (value >> (size - pos)) & 1
            res <<= 1
        res >>= 1
        return res

    def gen(self, init_key=None):
        if init_key is None:
            init_key = self.gen_init_key()
        init_key = self._expand_to_64(init_key)
        C = 0
        D = 0
        K = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        C = self._permutation(self.TABLE_FOR_KEY_PERM_C0, init_key, 64)
        D = self._permutation(self.TABLE_FOR_KEY_PERM_D0, init_key, 64)
        for i, v in enumerate(self.TABLE_FOR_BYTE_SHIFT):
            C <<= v
            D <<= v
            K[i] = (C << 28) | D
            K[i] = self._permutation(self.TABLE_FOR_FINAL_PERM, K[i], 56)

        return K
    

class RSAKey(Key):

    def __init__(self):
        super().__init__()
    
    def NOD(self, a, b):
        if a > b:
            b, a = a, b
        while b % a != 0:
            r = b % a
            b = a
            a = r
        return a
    
    def NODextended(self, a, b):
        if b == 0:
            return a, 1, 0  
        else:  
            gcd, x1, y1 = self.NODextended(b, a % b)  
            x = y1
            y = x1 - (a // b) * y1
            return gcd, x, y

    def is_simple(self, num, rounds=10):
        num -= 1
        s = 0
        d = num
        while d % 2 != 0:
            d //= 2
            s += 1
        
        for i in range(rounds):
            a = random.randint(2, num-1)
            if pow(a, d, num+1) == 1:
                continue
            for j in range(0, s):
                if pow(a, d*(2**j), num+1) == -1:
                    break
            else:
                return False
        return True

    def gen_init(self):
        p = 0
        while p == 0 or not self.is_simple(p):
            p = random.randint(10**32, 10**33)
            print(p)
        q = 0
        while q == 0 or not self.is_simple(q):
            q = random.randint(10**32, 10**33)
        n = (q-1)*(p-1)
        e = 0
        while e == 0 or self.NOD(n, e) != 1:
            e = random.randint(10**32, 10**33)
        return p, q, e
    
    def _key_is_valid(self, keys):
        p, q, e = keys
        return self.is_simple(p) and self.is_simple(q) and self.NOD(e, (p-1)*(q-1)) == 1

    def gen(self, keys):
        p, q, e = keys
        assert self._key_is_valid(keys), "Невалидные ключи"
        n = p*q
        n_euler = (p-1)*(q-1)
        _, d, _ = self.NODextended(e, n_euler)
        if d < 0:
            d = n_euler + d
        return n, e, d


class DHKey(Key):

    def __init__(self):
        super().__init__()

    def is_simple(self, num, rounds=10):
        num -= 1
        s = 0
        d = num
        while d % 2 != 0:
            d //= 2
            s += 1
        
        for i in range(rounds):
            a = random.randint(2, num-1)
            if pow(a, d, num+1) == 1:
                continue
            for j in range(0, s):
                if pow(a, d*(2**j), num+1) == -1:
                    break
            else:
                return False
        return True

    def gen_init(self):
        p = 0
        while p == 0 or not self.is_simple(p):
            p = random.randint(10**32, 10**33)
            print(p)
        g = 0
        while g == 0 or not self.is_simple(g) or not pow(g, p-1, p) == 1:
            g = random.randint(10**32, 10**33)
        a = random.randint(10**32, 10**33)
        b = random.randint(10**32, 10**33)
        return p, g, a, b
    
    def _key_is_valid(self, keys):
        p, g, a, b = keys
        return self.is_simple(p) and self.is_simple(g) and pow(g, p-1, p) == 1

    def gen(self, keys):
        p, g, a, b = keys
        assert self._key_is_valid(keys), "Невалидные ключи"
        A = pow(g, a, p)
        B = pow(g, b, p)
        if pow(A, b, p) != pow(B, a, p):
            print(pow(A, b, p), pow(B, a, p))
            return -1, -1
        return A, B

if __name__ == '__main__':
    print(bin(1))
    k = DESKey()
    print(k.gen(1))
