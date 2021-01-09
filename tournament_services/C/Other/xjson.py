#!/usr/bin/env python3


import fileinput
import json
import sys


def parse_json_objects(json_string):
    """
    Purpose: Parse multiple well-formed JSON objects from STDIN
    Signature: String -> List
    :return: list of Python representations of JSON object
    """
    result_list = []
    json_decoder = json.JSONDecoder()
    input_str = json_string.strip()
    while input_str:
        input_str = input_str.strip()
        value, index = json_decoder.raw_decode(input_str)
        input_str = input_str[index:]
        result_list.append(value)

    return result_list

def read_from_stdin():
    """
    Purpose: Reads a given file from the stdin line-by-line
    Signature: Void -> String
    :return: String with parsed line-by-line input
    """
    stdin_str = ""
    for line in fileinput.input():
        stdin_str += line
    return stdin_str



def create_count_seq_object(ret_list):
    """
    Purpose: Create a count and sequence JSON object
    Signature: List -> Dictionary
    :param ret_list: result list of the JSON parsed into python
    :return: a dictionary object (representing JSON object) where first key
             is count for the amount of JSON values read and the sequence
             is just the list of JSON objects
    """

    return {
        'count': len(ret_list),
        'seq': ret_list
    }


def create_json_list(result_list):
    """
    Purpose: Create a JSON list representing values from parsing
    Signature: List -> List
    :param result_list: result list of JSON values parsed
    :return: List where first value is the count of JSON values and rest is reversed sequence from input
    """
    reversed_result_list = [ele for ele in reversed(result_list)]
    return [len(result_list)] + reversed_result_list


def main():
    """
    Purpose: Run the xjson program to parse JSON and display output about it
    Signature: Void -> Void
    :return: Prints data about parsed JSON to STDOUT
    """
    json_string = read_from_stdin()
    result_list = parse_json_objects(json_string)
    count_seq_object = create_count_seq_object(result_list)
    json_list = create_json_list(result_list)
    print(json.dumps(count_seq_object), file=sys.stdout)
    print(json.dumps(json_list), file=sys.stdout)


if __name__ == '__main__':
    main()
