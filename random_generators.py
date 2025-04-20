class MersenneTwister:
    def __init__(self, seed):
        (self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
        self.a = 0x9908B0DF
        (self.u, self.d) = (11, 0xFFFFFFFF)
        (self.s, self.b) = (7, 0x9D2C5680)
        (self.t, self.c) = (15, 0xEFC60000)
        self.l = 18
        self.f = 1812433253
        
        self.MT = [0] * self.n
        self.index = self.n
        self.MT[0] = seed
        
        for i in range(1, self.n):
            self.MT[i] = (self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i) & self.d
    
    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & 0x80000000) + (self.MT[(i+1) % self.n] & 0x7FFFFFFF)
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ (x >> 1)
            if x % 2 != 0:
                self.MT[i] ^= self.a
        self.index = 0
    
    def get_random_number(self):
        if self.index >= self.n:
            self.twist()
        
        y = self.MT[self.index]
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= (y >> self.l)
        
        self.index += 1

        return y & self.d
    
    def get_random_number_on_range(self, start, end):
        n = self.get_random_number()
        normalized = n / (2**32)
        return start + int(normalized * (end - start + 1))


class LinearCongruentialGenerator:
    def __init__(self, seed, a, b, m):
        self.X = seed
        self.a = a
        self.b = b
        self.m = m

    def generate(self):
        self.X = (self.X*self.a + self.b) % self.m
    
    def get_random_number(self):
        self.generate()
        return self.X
    
    def get_random_number_on_range(self, start, end):
        n = self.get_random_number()
        return start + int(n % (end-start+1))

