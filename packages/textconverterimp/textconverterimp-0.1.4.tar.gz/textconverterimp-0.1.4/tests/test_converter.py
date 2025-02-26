import unittest
from textconverterim.converter import to_sentence_case, to_title_case, to_kebab_case

class TestTextConverter(unittest.TestCase):
    def test_to_sentence_case(self):
        self.assertEqual(to_sentence_case("ТекСт из слОв"), "Текст из слов")

    def test_to_title_case(self):
        self.assertEqual(to_title_case("ТекСт из слОв"), "Текст Из Слов")

    def test_to_kebab_case(self):
        self.assertEqual(to_kebab_case("ТекСт из слОв"), "текст-из-слов")

if __name__ == '__main__':
    unittest.main()