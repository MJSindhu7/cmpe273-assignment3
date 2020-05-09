import pickle
import math

from pickle_hash import hash_code_hex
from bitarray import bitarray


class BloomFilter(object):
    def __init__(self, items_count, fp_prob):

        self.fp_prob = fp_prob

        self.size = self.get_size(items_count, fp_prob)

        self.hash_count = self.get_hash_count(self.size, items_count)

        self.bit_array = bitarray(self.size)

        self.bit_array.setall(0)

    def add(self, item):
        digests = []
        for i in range(self.hash_count):
            dump = pickle.dumps(item)
            hash = hash_code_hex(dump)
            index = int(hash, 16) % self.size
            digests.append(index)
            self.bit_array[index] = True

    def is_member(self, item):
        for i in range(self.hash_count):
            dump = pickle.dumps(item)
            hash = hash_code_hex(dump)
            index = int(hash, 16) % self.size
            if self.bit_array[index] == False:
                return False
        return True

    @classmethod
    def get_size(self, n, p):
        m = -(n * math.log(p)) / (math.log(2)**2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        k = (m / n) * math.log(2)
        return int(k)
