# Requirement pdfminer.six
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os
import json

def sortFunc(file):
    return int(file.split("_marksheet.pdf")[0])

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


def findStudentInfo(fileName, sem):
    # Main Output
    cur_path = os.path.dirname(__file__)
    file_path = os.path.relpath(f'./{sem}/{fileName}', cur_path)
    data = convert_pdf_to_txt(file_path)
    if sem == 'SM03':
        # find sgpa
        sep = data.split('ODD. (3rd) SEMESTER :')
        sep2 = sep[1].split('\n')
        try:
            cgpa = float(sep2[0])
        except:
            cgpa = "Incomplete"
        # find name
        sep = data.split('NAME : ')
        sep2 = sep[1].split('\n')
        name = sep2[0]
        # find rollNo
        sep = data.split('ROLL NO. : ')
        sep2 = sep[1].split('\n')
        rollNum = sep2[0]
    elif sem == 'SM02':
        # find sgpa
        sep = data.split('EVEN (2nd) SEMESTER :')
        sep2 = sep[1].split('\n')
        try:
            cgpa = float(sep2[0])
        except:
            cgpa = "Incomplete"
        # find name
        sep = data.split('NAME : ')
        sep2 = sep[1].split('\n')
        name = sep2[0]
        # find rollNo
        sep = data.split('ROLL NO. : ')
        sep2 = sep[1].split('\n')
        rollNum = sep2[0] 
        
    elif sem == 'SM01':
        # find sgpa
        sep = data.split('ODD. (1st) SEMESTER :')
        sep2 = sep[1].split('\n')
        try:
            cgpa = float(sep2[0])
        except:
            cgpa = "Incomplete"

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
    # with open(f'{studentData["rollNo"]}_info.json','w', encoding='utf-8') as fin:
    #     fin.write(json.dumps(studentData))
    return studentData

def saveIntoFile(semFolders):
    mainOutput = {}
    for sem in semFolders:
        allFiles = []

        for file in os.listdir(f'./{sem}/'):
            allFiles.append(file)

        allFiles.sort(key=sortFunc)
        mainDict = {}
        for file in allFiles:
            rollNo = int(file.split("_marksheet.pdf")[0])
            content = findStudentInfo(file, sem)
            mainDict[rollNo] = content
            print(f"{rollNo} Done!")
        mainOutput[sem] = mainDict
    with open('studentInfo.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(mainOutput))


#main fun
# delete previous info file
# for file in os.listdir():
#     if "_info.json" in file:
#         os.remove(file)
if os.path.exists('studentInfo.json'):
    os.remove('studentInfo.json')
    
semFolders = ['SM01', 'SM02', 'SM03']
saveIntoFile(semFolders)
# findStudentInfo(file)