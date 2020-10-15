import json
import pandas as pd
import numpy
import sys
import argparse
import re
from hw3.generate_analysis import *

pony_names = {'Twilight Sparkle': 'twilight', 'Applejack': 'applejack', 'Rarity': 'rarity', 'Pinkie Pie': 'pinkie', 'Rainbow Dash': 'rainbow', 'Fluttershy': 'fluttershy'}
pony_count = dict()

data_file = ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help='The dialog file in csv format')  
    parser.add_argument('-o', help='The output file path', default='')
    args = parser.parse_args()
    data_file = args.data_file
    output_path = args.o
    result = dict()


    result['verbosity'] = generate_verbosity(data_file) 
    result['mentions'] = generate_mentions(data_file)
    result['follow_on_comments'] = generate_followon(data_file)
    result['non_dictionary_words'] = generate_nondict(data_file)

    if output_path == "":
        print(result)
    else:
        if osp.exists(output_path):
            json_file = json.dumps(output_path)
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4)



if __name__ == "__main__":
    main()
