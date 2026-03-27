import unittest

class Test(unittest.TestCase):
    def test_hardcoded_low(self):
        self.assertEqual(sam(2, 10, 1000), 24)
        self.assertEqual(sam(3, 13, 50), 23)
        self.assertEqual(sam(5, 20, 100), 25)
        self.assertEqual(sam(7, 15, 200), 143)
        self.assertEqual(sam(10, 5, 100), 0)

    def test_random(self):
        import random
        for _ in range(100):
            base = random.randint(100, 10000)
            exponent = random.randint(100, 10000)
            modulo = random.randint(100, 100)
            expected = pow(base, exponent, modulo)
            self.assertEqual(sam(base, exponent, modulo), expected)

    def test_random_high(self):
        import secrets
        for _ in range(10):
            base = secrets.randbits(1024)
            exponent = secrets.randbits(1024)
            modulo = secrets.randbits(1024) + 1 
            expected = pow(base, exponent, modulo)
            self.assertEqual(sam(base, exponent, modulo), expected)


def sam(base: int, exponent: int, modulo: int):
    current = base % modulo
    for bit in bin(exponent)[3:]:
        current = (current * current) % modulo
        if bit == '1':
            current = (current * base) % modulo
    return current

if __name__ == '__main__':
    unittest.main()