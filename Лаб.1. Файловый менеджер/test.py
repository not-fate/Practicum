import unittest


def foo(t):
    num = int(t, base=16)
    num = num >> 10
    u2 = num & 0b1111111
    num = num >> 7
    u3 = num & 0b111
    num = num >> 3
    u4 = num & 0b1

    return (u2 << 4) | (u3 << 1) | u4


class TestFoo(unittest.TestCase):

    def test_1(self):
        self.assertEqual(foo('0x14361f'), 213)
        self.assertEqual(foo('0xc7d81'), 508)
        self.assertEqual(foo('0x151b3b'), 1125)
        self.assertEqual(foo('0xad622'), 858)


if __name__ == '__main__':
    unittest.main()
