from PyPDF2 import PdfReader
from pyarabic import araby
import re

#
# with open('basicvocabulary.pdf', 'rb') as pdf_file:
#     reader = PdfReader(pdf_file)
#     num_pages = len(reader.pages)
#     for page_num in range(num_pages):
#         page = reader.pages[page_num]
#         text = '\n'.join([page.extract_text() for page in reader.pages])

with open('basicvocabulary.pdf', 'rb') as pdf_file:
    reader = PdfReader(pdf_file)
    text = ('\n'.join([page.extract_text() for page in reader.pages]))

print(text)
