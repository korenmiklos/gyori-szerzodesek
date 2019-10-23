from zipfile import ZipFile
from lxml import etree
import sys
import csv

namespaces = {'o': 'urn:schemas-microsoft-com:office:office',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'v': "urn:schemas-microsoft-com:vml",
    'w': "http://schemas.openxmlformats.org/wordprocessingml/2006/main", 
    'w10': "urn:schemas-microsoft-com:office:word",
    'wp': "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing", 
    'wps': "http://schemas.microsoft.com/office/word/2010/wordprocessingShape", 
    'wpg': "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup", 
    'mc': "http://schemas.openxmlformats.org/markup-compatibility/2006", 
    'wp14': "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
    'w14': "http://schemas.microsoft.com/office/word/2010/wordml"}

# Load the first table from your document. In your example file,
# there is only one table, so I just grab the first one.
document = etree.XML(ZipFile(sys.argv[1]).open('word/document.xml').read())
output = csv.writer(sys.stdout)

for row in document.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr'):
    line = []
    for cell in row.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc'):
        line.append(' '.join([item.text for item in cell.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')]))
    output.writerow(line)
