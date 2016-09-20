#!/usr/bin/env python
"""
Tests a set of url for return cods and new addresses
"""
import requests
import csv


KEY_REPORTED_STATUS_CODE_1 = 200
KEY_REPORTED_STATUS_CODE_2 = 404
KEY_CONNECT_ERROR = 0

MESSAGE_ERROR_GET_URL = "Failed to get results for url: {}\n\tError message: {}."
MESSAGE_REPORT_PROBLEM = "\tProblem with: {}"
MESSAGE_ALL_URLS_CHECKED = "All {} URLs checked: Status 200: {}, Status 404: {}, Connect errors: {}."
MESSAGE_CHECKED_URLS = "{} URLs checked: Status 200: {}, Status 404: {}, Connect errors: {}."

FLUSH_INTERVAL = 100
COLUMN_QUERY_URL = 0

INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'
IN_FILE = 'input_urls_shop.tab'
OUT_FILE = 'checked_urls.tab'
TEST_SET = [['http://pestimenergia.bg/pellet_comfort_mini.htm', ],
            ['http://pestimenergia.bg/news23_en.htm']
            ]


def main():
    parse_requests(INPUT_DIR + IN_FILE, OUTPUT_DIR + OUT_FILE)


def parse_requests(in_path, out_path):
    """
    opens the files as csv objects and sends them to get_dstination_urls()
    :param in_path: path to input csv
    :param out_path: path to output csv
    :return :
    """
    with open(in_path, 'r', encoding='utf8') as f:
        with open(out_path, 'w', encoding='utf8') as j:
            get_destination_urls(f, j)


def get_destination_urls(in_file, out_file):
    """

    :param in_file: input csv file with two columns - url that need to be tested.
    :param out_file: output csv with columns [query_url, expected_final, final_url, status_code] with one column - url that need to be tested.
    :return out_csv:
    """
    in_csv = csv.reader(in_file, delimiter='\t')
    out_csv = csv.writer(out_file, delimiter='\t', lineterminator='\n')
    flush_status = 0
    code_count = {}
    for i, row in enumerate(in_csv, start=1):
        url_string = row[COLUMN_QUERY_URL]
        try:
            r = requests.get(url_string)
        except requests.exceptions.RequestException as e:
            code_count.setdefault(KEY_CONNECT_ERROR, 0)
            code_count[KEY_CONNECT_ERROR] += 1
            print(MESSAGE_ERROR_GET_URL.format(url_string, e))
            continue
        code_count.setdefault(r.status_code, 0)
        code_count[r.status_code] += 1

        if r.status_code == KEY_REPORTED_STATUS_CODE_2:
            print(MESSAGE_REPORT_PROBLEM.format(url_string))

        out_csv.writerow([url_string, r.url, r.status_code])
        if i - flush_status == FLUSH_INTERVAL:
            out_file.flush()
            flush_status = i
            print(MESSAGE_CHECKED_URLS.format(i,
                                              code_count.get(KEY_REPORTED_STATUS_CODE_1, 0),
                                              code_count.get(KEY_REPORTED_STATUS_CODE_2, 0),
                                              code_count.get(KEY_CONNECT_ERROR, 0)
                                              ))
    print(MESSAGE_ALL_URLS_CHECKED.format(i,
                                          code_count.get(KEY_REPORTED_STATUS_CODE_1, 0),
                                          code_count.get(KEY_REPORTED_STATUS_CODE_2, 0),
                                          code_count.get(KEY_CONNECT_ERROR, 0)
                                          )
          )

if __name__ == '__main__':
    main()
