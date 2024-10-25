import unittest

from Parser import mk_lexObj,mk_prsrObj

P_obj = mk_prsrObj()
L_obj = mk_lexObj()

class TestLexer(unittest.TestCase):
    def teststring(self):
        self.assertEqual(L_obj('{"foo"}'),['{', 'foo', '}'])

if __name__ == "__main__":
    unittest.main()