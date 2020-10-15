import pandas as pd
import numpy
import sys
import argparse
import re
import os.path as osp

pony_names = {'Twilight Sparkle': 'twilight', 'Applejack': 'applejack', 'Rarity': 'rarity', 'Pinkie Pie': 'pinkie', 'Rainbow Dash': 'rainbow', 'Fluttershy': 'fluttershy'}
pony_count = dict()

data_file = ""

def get_pony_masked(data_file):
    df = pd.read_csv(data_file)
    is_pony_mask = df['pony'].apply(lambda x: x in pony_names.keys())
    return df[is_pony_mask]


def generate_verbosity(data_file):
    df = pd.read_csv(data_file)
    
    is_pony_mask = df['pony'].apply(lambda x: x in pony_names.keys())
    
    # Test: check if percentage adds to 1(can be performed for all operations)
    # Get verbosity
    for pony in df[is_pony_mask].pony:
        pony_name = pony_names.get(pony)
        if not pony_name in pony_count.keys():
            pony_count[pony_name] = 0
        else:
            pony_count[pony_name] += 1
   
    
    total_count = 0
    for count in pony_count.values():
        total_count += count
    for k, v in pony_count.items():
        pony_count[k] = round(v / total_count, 2)

    return pony_count


def generate_mentions(data_file):
    df = pd.read_csv(data_file)
    is_pony_mask = df['pony'].apply(lambda x : x in pony_names.keys())
    
    mention_dict = dict()
    pony_df = df[is_pony_mask]

    # Build mention count
    for index, row in pony_df.iterrows():
        pony_key = pony_names[row.pony]
        if pony_key not in mention_dict:
            mention_dict[pony_key] = dict()
        for other_pony in pony_names.keys():
            other_pony_key = pony_names[other_pony]
            other_pony_re = other_pony.replace(" ", "|")
            if re.search(rf"\b{other_pony_re}\b", row.dialog):
                if other_pony != row.pony:
                    if not other_pony_key in mention_dict[pony_key].keys():
                        mention_dict[pony_key][other_pony_key] = 0
                    else:
                        mention_dict[pony_key][other_pony_key] += 1

    # Build mention percentage
    for pony, pony_mention in mention_dict.items():
        total = 0
        for count in pony_mention.values():
            total += count
        for other, count in pony_mention.items():
            mention_dict[pony][other] = round(count / total, 2)

    return(mention_dict)

def generate_followon(data_file):
    df = pd.read_csv(data_file)
    is_pony_mask = df['pony'].apply(lambda x : x in pony_names.keys())

    pony_df = df[is_pony_mask]
    follow_on = dict()

    # Generate follow count for every pony
    for index, row in pony_df.iterrows():
        prev_pony = df.iloc[index-1].pony
        this_pony = row.pony
        this_pony_key = pony_names[this_pony]
        if prev_pony in pony_names:
            prev_pony_key = pony_names[prev_pony]
        else:
            prev_pony_key = 'other'

        if not this_pony_key in follow_on.keys():
            follow_on[this_pony_key] = dict()

        if prev_pony in pony_names.keys():
            if prev_pony != row.pony:
                if not prev_pony_key in follow_on[this_pony_key].keys():
                    follow_on[this_pony_key][prev_pony_key] = 0
                if df.iloc[index-1].title == row.title:
                    follow_on[this_pony_key][prev_pony_key] += 1
        else:
            if not 'other' in follow_on[this_pony_key].keys():
                follow_on[this_pony_key]['other'] = 0
            follow_on[this_pony_key]['other'] += 1

    # Calculate follow % for every pony
    for pony, follow_list in follow_on.items():
        total = 0
        for value in follow_list.values():
            total += value
        for other, value in follow_list.items():
            follow_on[pony][other] = round(value / total, 2)
    return follow_on


def generate_nondict(data_file):
    df = pd.read_csv(data_file)
    is_pony_mask = df['pony'].apply(lambda x : x in pony_names.keys())
    pony_df = df[is_pony_mask]

    pony_non_dict = dict()
    non_dict_path = osp.join(osp.dirname(__file__), "..", "..", "data", "words_alpha.txt")
    with open(non_dict_path) as f:
        non_dict_words = set(f.read().split())

    # Build non-word count for each pony
    for index, row in pony_df.iterrows():
        this_pony = row.pony
        this_pony_key = pony_names[this_pony]
        if not this_pony_key in pony_non_dict.keys():
            pony_non_dict[this_pony_key] = dict()

        dialog = replace_unicode(row.dialog)
        dialog = dialog.lower()

        sentence_dict = str_to_wordset(dialog)
        for word in sentence_dict:
            # remove potential punctuation
            word = remove_punctuation(word)
            if check_nonword(word, non_dict_words):
                if not word in pony_non_dict[this_pony_key].keys():
                    pony_non_dict[this_pony_key][word] = 0
                pony_non_dict[this_pony_key][word] += 1
        
    # Find the top 5 words
    for pony, dictionary in pony_non_dict.items():
        sorted_dict = sort_dictionary(dictionary)
        topfive = sorted_dict[:5]

        pony_non_dict[pony] = []
        
        for word in topfive:
            pony_non_dict[pony].append(word[0])
    
    return pony_non_dict


def remove_punctuation(word):
    return re.sub('[^A-Za-z0-9\']+', '', word)

def replace_unicode(line):
    return re.sub(r"<U\+[0-9a-zA-Z]{4}>", " ", line)


def str_to_wordset(line):
    return set(line.split())

def check_nonword(word, dictionary):
    return (not word in dictionary)

def sort_dictionary(dictionary):
    return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help='The dialog file in csv format')  
    parser.add_argument('-o', help='The output file path', default='')
    args = parser.parse_args()
    data_file = args.data_file
    
    generate_nondict(data_file)


if __name__ == "__main__":
    main()
