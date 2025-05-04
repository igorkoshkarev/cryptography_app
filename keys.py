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

if __name__ == '__main__':
    print(bin(1))
    k = DESKey()
    print(k.gen(1))
