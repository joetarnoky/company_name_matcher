# company_name_matcher
Produces a list of pairs of related companies given a list of company names

Dependencies:
pip install python-Levenshtein
pip install fuzzywuzzy

Limitations:
Due to the application of the jaccard metric before fuzzy calcualtions this cannot match misspelt names, this sacrifice was made in favour of a factor 8 increase in performance speed due to jaccard calculations being far more efficient than fuzzy calculations.
