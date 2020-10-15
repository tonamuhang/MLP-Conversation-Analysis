import unittest
import sys
import os.path as osp
from hw3.generate_analysis import *

data_dir = osp.dirname(__file__)
data_file = osp.join(data_dir, "..", "..", "..", "data", "clean_dialog.csv")
dictionary_dir = osp.dirname(__file__)
dictionary_file = osp.join(dictionary_dir, "..", "..", "..", "data", "words_alpha.txt")
with open(dictionary_file) as f:
    non_dict_words = set(f.read().split())

class ScriptTestCase(unittest.TestCase):
    # Test if the sum of verbosity equal to 1
    def test_generate_verbosity(self):
        sum = 0
        for value in generate_verbosity(data_file).values():
            sum += value

        self.assertEqual(round(sum), 1.0)


    def test_generate_mention(self):
        for ponys in generate_mentions(data_file).values():
            sum = 0
            for value in ponys.values():
                sum += value
            if sum > 0:
                self.assertEqual(round(sum), 1.0)
            else:
                self.assertEqual(sum, 0.0)

    def test_generate_follow(self):
        for ponys in generate_followon(data_file).values():
            sum = 0
            for value in ponys.values():
                sum += value
            if sum > 0:
                self.assertEqual(round(sum), 1.0)
            else:
                self.assertEqual(sum, 0.0)

    def test_replace_unicode(self):
        self.assertEqual(replace_unicode("<U+0097>"), " ")
        self.assertEqual(replace_unicode("No<U+0097> whoa!"), "No  whoa!")
        self.assertNotEqual(replace_unicode("<U+>"), " ")

    def test_str_to_wordset(self):
        self.assertEqual(str_to_wordset("I love human"), {"I", "love", "human"})
        self.assertEqual(str_to_wordset("Two  spaces"), {"Two", "spaces"})
        self.assertEqual(str_to_wordset("Two Two words"), {"Two", "words"})
        
    def test_check_nonword(self):
        self.assertTrue(check_nonword("%f34", non_dict_words))
        self.assertFalse(check_nonword("hello", non_dict_words))


    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation("oh,"), "oh")
        self.assertEqual(remove_punctuation("i'm"), "i'm")

    
    def test_generate_nondict(self):
        self.assertFalse(generate_nondict(data_file)['Fluttershy'][0] in non_dict_words)

    
    def test_get_pony_masked(self):
        pony_names = {'Twilight Sparkle', 'Applejack', 'Rarity', 'Pinkie Pie', 'Rainbow Dash', 'Fluttershy'}
        self.assertTrue(get_pony_masked(data_file).pony.iloc[2] in pony_names)

    def test_check_ponynum(self):
        self.assertEqual(len(generate_mentions(data_file)), 6)
