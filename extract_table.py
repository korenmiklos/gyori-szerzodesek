from zipfile import ZipFile
from lxml import etree
import sys
import csv
import re
import os
import glob

KEYS = {
    'description': re.compile(r'(szerződés\W+megnevezése)|(támogatás\W+célja)', re.UNICODE),
    'winner': re.compile(r'(fél\W+megnevezése)|(támogatott\W+neve)', re.UNICODE),
    'amount': re.compile(r'(értéke)|(összege)', re.UNICODE),
    'period': re.compile(r'időtartam', re.UNICODE)
}

def read_urls(fname):
    output = {}
    for line in open(fname, 'r').readlines():
        key = os.path.basename(line).strip()
        if os.path.splitext(key)[1][0:4] == '.doc':
            if key in output:
                raise Exception('Duplicate key', key)
            else:
                output[key] = line.strip()
    return output

URLS = read_urls('documents.txt')

def row_to_dictionary(header, row, url):
    output = dict(url=url)
    for i, key in enumerate(header):
        for field in KEYS:
            if KEYS[field].search(key) is not None:
                try:
                    output[field] = row[i]
                except:
                    pass
    return output

def get_row(row):
    line = []   
    for cell in row.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc'):
        line.append(' '.join([item.text for item in cell.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')]))
    return line

def find_header(iterator, min_length=3):
    # Find first row with at least min_length elements
    header = []
    while len(header) < min_length:
        try:
            header = get_row(next(iterator))
        except:
            break
    return header
    

def dumpfile(fname, output):
    try:
        url = URLS[os.path.basename(fname)]
    except:
        return
    path = 'temp/docx/' + os.path.basename(fname)
    if not path[-1] == 'x':
        path += 'x'

    document = etree.XML(ZipFile(path).open('word/document.xml').read())
    rows = document.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr')
    header = find_header(rows)
    if header:
        for row in rows:
            output.writerow(row_to_dictionary(header, get_row(row), url))

if __name__ == '__main__':
    output = csv.DictWriter(sys.stdout, fieldnames=['url']+list(KEYS))
    output.writeheader()

    files = glob.glob('raw/doc/*.doc*')
    for file in files:
        dumpfile(file, output)
