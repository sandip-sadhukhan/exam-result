# Requirement pdfminer.six
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os
import json

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def findStudentInfo(fileName):
    data = convert_pdf_to_txt(fileName)
    # find sgpa
    sep = data.split('ODD. (3rd) SEMESTER :')
    sep2 = sep[1].split('\n')
    cgpa = float(sep2[0])
    # find name
    sep = data.split('NAME : ')
    sep2 = sep[1].split('\n')
    name = sep2[0]
    # find rollNo
    sep = data.split('ROLL NO. : ')
    sep2 = sep[1].split('\n')
    rollNum = sep2[0]

    studentData = {
        'name':name,
        'rollNo':rollNum,
        'cgpa':cgpa,
    }
    with open(f'{studentData["rollNo"]}_info.json','w', encoding='utf-8') as fin:
        fin.write(json.dumps(studentData))

#main fun
# delete previous info file
for file in os.listdir():
    if "_info.json" in file:
        os.remove(file)
# call all for pdf
for file in os.listdir():
    if "_marksheet.pdf" in file:
        findStudentInfo(file)