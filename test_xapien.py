import unittest
import json
from Xapien_task import clean_name, load_and_clean_data, calculate_fuzzy_similarity, calculate_jaccard_similarity, find_index_pairs, extract_related_pairs

class TestCustomClean_name(unittest.TestCase):
    def test_clean_name(self):
        self.assertEqual(clean_name("  The XYZ Holdings"), "xyz")
        self.assertEqual(clean_name("t-he Caprice, holdings. ltd "), "caprice")
        self.assertEqual(clean_name("999999, "), "999999")
        self.assertEqual(clean_name(" Holdings  "), "")

class TestLoadAndCleanData(unittest.TestCase):
    def test_load_and_clean_data(self):
        cleaned_names, unique_original_names = load_and_clean_data('test_sample.json')
        self.assertEqual(cleaned_names[0], "caprice")
        self.assertEqual(cleaned_names[1], "nashville")
        self.assertEqual(unique_original_names[1], "THE NASHVILLE CORPORATION LIMITED")
        self.assertEqual(unique_original_names[-2], "")

    def test_empty_json_file(self):
        with open('empty_file.json', 'w') as json_file:
            json.dump([], json_file)
        cleaned_names, unique_original_names = load_and_clean_data('empty_file.json')
        self.assertEqual(cleaned_names, [])
        self.assertEqual(unique_original_names, [])

class TestCalculateFuzzySimilarity(unittest.TestCase):
    def test_calculate_fuzzy_similarity(self):
        self.assertLess(calculate_fuzzy_similarity("caprice", "olswang"), 70)
        self.assertGreater(calculate_fuzzy_similarity("olswang cosec", "olswang directors 2"), 70)

class TestCalculateJaccardSimilarity(unittest.TestCase):
    def test_calculate_jaccard_similarity(self):
        self.assertEqual(calculate_jaccard_similarity("caprice", "caprice"), 1)
        self.assertEqual(calculate_jaccard_similarity("caprice", "olswang"), 0)
        self.assertGreater(calculate_jaccard_similarity("olswang cosec", "olswang directors 2"), 0.2)
        self.assertEqual(calculate_jaccard_similarity("", ""), 0)

class TestFindIndexPairs(unittest.TestCase):
    def test_find_index_pairs(self):
        company_names = ["caprice", "nashville", "olswang", "caprice", "nashville", ""]
        jaccard_threshold = 0.2 
        fuzzy_threshold = 70  
        index_pairs = find_index_pairs(company_names, jaccard_threshold, fuzzy_threshold)
        self.assertEqual(index_pairs, [(0, 3), (1, 4)])
        
class TestExtractRelatedPairs(unittest.TestCase):
    def test_extract_related_pairs(self):
        company_names = ["Caprice Holdings LTD", "THE NASHVILLE CORPORATION LIMITED", "OLSWANG COSEC LIMITED", "Caprice Holdings Limited", "NASSVILLE CORPORATION LTD"]
        index_pairs = [(0, 3), (1, 4)]
        related_pairs = extract_related_pairs(index_pairs, company_names)
        self.assertEqual(related_pairs, [("Caprice Holdings LTD", "Caprice Holdings Limited"), ("THE NASHVILLE CORPORATION LIMITED", "NASSVILLE CORPORATION LTD")])

if __name__ == '__main__':
    unittest.main()
