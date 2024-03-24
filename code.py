import pandas as pd
import csv
import sys
import re
import json
from typing import Tuple

lst_of_dict = []
RECORD_DICT = {}

"""
python pivoter

# convert custom file to json
# line based file processing

Run program:

    $ python3 code.py input_file output

[TODO]:
    * use pep8 recomendation
    * compare csv vs. pandas
"""

INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else 'input_file'
OUTPUT_FILE = sys.argv[2] if len(sys.argv) > 1 else 'output_file'

# constant values
START_RECORD = 'RECORD'

# [TODO]: put in class and remove global object

lst_of_dict = []
# global RECORD_DICT
RECORD_DICT = {}


# helper functions
def remove_endl(string: str) -> str:
    """remove ending \n from a string"""
    return string.replace("\n", "")


def parse_space(string: str) -> list:
    """split string with space"""
    return re.split('( )', string)


def make_pretty(string: str) -> list:
    """remove endl and seprate space"""
    return parse_space(remove_endl(string))


def key_prettifier(key_json: str) -> str:
    """
    remove ( [", "], # ) from key to make it pretty
    """
    return key_json.replace('["', '').replace('"]', '').replace('#', '')


def dump_json(list_of_dict: list, file_output: str) -> None:
    """dump list of dictionaries to output file"""
    with open(file_output, "w", encoding='utf-8') as outfile:
        json.dump(list_of_dict, outfile, indent=4)


def dump_csv_pandas(list_of_dict: list, file_output: str) -> None:
    """convert dictionary to csv"""
    pd.DataFrame(list_of_dict).to_csv(file_output, index=False)


def dump_csv_csv(list_of_dict: list, file_output: str) -> None:
    """convert dictionary to csv"""
    with open(file_output, 'w', newline='',
              encoding='utf-8') as file_descriptor:
        csv_writer = csv.writer(file_descriptor)

        count = 0
        for data in list_of_dict:
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())


def extract_line(get_line: str) -> Tuple[str, str]:
    """extract key, value from each line"""

    # some criteria on line extraction
    # key = next(s for s in get_line)
    key = get_line[0]
    val = ''.join(get_line[1:]).strip()
    return key, val


def main() -> None:
    """program main loop"""
    global RECORD_DICT

    with open(INPUT_FILE, 'r', encoding='utf-8') as file_descriptor:
        for line in file_descriptor:

            get_line = make_pretty(line)
            key_record = ''

            if (START_RECORD not in get_line):
                key_record, val = extract_line(get_line=get_line)
                key_json = json.dumps([key_record])
                key_json = key_prettifier(key_record)
                RECORD_DICT.update({key_json: val})

            else:  # START_RECORD REACHED
                if len(RECORD_DICT):  # better and faster approach? data in list not good
                    lst_of_dict.append(RECORD_DICT)
                    RECORD_DICT = {}
        lst_of_dict.append(RECORD_DICT)


if __name__ == '__main__':
    main()
    # print(len(lst_of_dict))
    dump_json(list_of_dict=lst_of_dict, file_output=OUTPUT_FILE+ '.json')
    # dump_csv_csv(list_of_dict=lst_of_dict, file_output=OUTPUT_FILE+'.csv')
    dump_csv_pandas(list_of_dict=lst_of_dict, file_output=OUTPUT_FILE+'pandas.csv')
