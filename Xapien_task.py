import json
import regex
from cleanco import basename
from collections import OrderedDict
from fuzzywuzzy import fuzz

def clean_name(name):
    cleaned_name = regex.sub(r"[[:punct:]]+", "", name).lower()
    cleaned_name = basename(basename(cleaned_name)) # basename removes legal suffixes, call twice in case companies have 2 suffixes
    cleaned_name = cleaned_name.replace("holdings", "").replace("the", "").replace("club", "").replace("group", "") # remove common words not removed by basename
    cleaned_name = cleaned_name.strip()
    return cleaned_name

def load_and_clean_data(file_name):
    try:
        with open(file_name, 'r') as json_file:
            company_names_list = json.load(json_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_name}' does not exist")
    except json.JSONDecodeError:
        raise ValueError(f"The file '{file_name}' is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the file: {e}")
    
    unique_company_names_list = list(OrderedDict.fromkeys(company_names_list)) # remove duplicates forming list from which we will choose pairs
    cleaned_company_names = [clean_name(name) for name in unique_company_names_list]
    return cleaned_company_names, unique_company_names_list

def calculate_fuzzy_similarity(name1, name2):
    m1 = fuzz.token_sort_ratio(name1, name2) + 1e-9
    m2 = fuzz.partial_ratio(name1, name2) + 1e-9
    harmonic_mean = 2 * m1 * m2 / (m1 + m2)
    return harmonic_mean

def calculate_jaccard_similarity(name1, name2):
    set1 = set(name1.split())
    set2 = set(name2.split()) 
    intersection_size = len(set1.intersection(set2))
    union_size = len(set1.union(set2))
    if union_size == 0:
        jaccard_similarity = 0 # avoid divide by 0 errors caused by case of two empty strings
    else:
        jaccard_similarity = intersection_size / union_size
    return jaccard_similarity

def find_index_pairs(company_names, jaccard_threshold, fuzzy_threshold):
    if not (0 <= jaccard_threshold <= 1):
        raise ValueError("jaccard_threshold must be between 0 and 1")
    if not (0 <= fuzzy_threshold <= 100):
        raise ValueError("fuzzy_threshold must be between 0 and 100")
    related_indices = []
    for i in range(len(company_names)):
        for j in range(i+1, len(company_names)): # i+1 ensures calculations only performed once per pair
            name1 = company_names[i]
            name2 = company_names[j] 
            jaccard_similarity = calculate_jaccard_similarity(name1, name2)
            if jaccard_similarity >= jaccard_threshold:
                similarity = calculate_fuzzy_similarity(name1, name2)
                if similarity >= fuzzy_threshold:
                    related_indices.append((i, j))
    return related_indices

def extract_related_pairs(index_pairs, company_names):
    related_pairs = []
    for i1, i2, in index_pairs:
        name1 = company_names[i1]
        name2 = company_names[i2]
        related_pairs.append((name1,name2))
    return related_pairs

def main():

    # Load and clean the data
    try:
        cleaned_names, unique_original_names = load_and_clean_data('org_names[19229].json') 
    except Exception as e:
        print(f"Error: {e}")
        return 0

    # Calculate Jaccard similarity metric for all pairs, only calculate fuzzy ratio if pair exceeds a low jaccard threshold
    jaccard_threshold = 0.1  
    fuzzy_threshold = 70
    try:
        index_pairs = find_index_pairs(cleaned_names, jaccard_threshold, fuzzy_threshold)
    except Exception as e:
        print(f"Error: {e}")
        return 0

    # Produce final list of pairs
    related_pairs = extract_related_pairs(index_pairs, unique_original_names)
    print(len(related_pairs))
    print(related_pairs[:20])

if __name__ == "__main__":
    main()
