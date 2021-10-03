# put the rtf files that you want to convert into './rtf-files' folder and run the script.
# pdf files will be created into the main folder'

from striprtf.striprtf import rtf_to_text
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
from os import walk

filePath='./rtf-files/'

def rtfToPdf(filePath, fileName):
    f = open(filePath+fileName, 'r')
    fileName=fileName.strip('.rtf')

    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    canvas = Canvas(f'{fileName}.pdf', pagesize=A4)
    canvas.setFont('Verdana', 10)
    # A4 (210 x 297 mm)

    # print(f.read())
    convertedText = rtf_to_text(f.read())
    # print(convertedText)
    heightReduction = 0
    lineDistance=0.5
    startHeight=29.7-2
    maxWidth=(21-1-1)*cm
    emptyLineCount=4

    for section in convertedText.split('\n\n'):
        sectionList=[]
        for line in section.split('\n'):
            targetLineCount=0
            if canvas.stringWidth(line)>maxWidth:
                # calculate how many lines needed for the long string
                targetLineCount = math.ceil(canvas.stringWidth(line)/maxWidth)
            # print(targetLineCount)

            if targetLineCount>0:
                line = line.split(' ')
                stringBuilder = ''
                newLine=[]
                for word in line:
                    previousStringBuilder = stringBuilder
                    stringBuilder += word + ' '
                    if canvas.stringWidth(stringBuilder) > maxWidth:
                        # if string is bigger than maximum width add previous string to array
                        newLine.append(previousStringBuilder)
                        stringBuilder=word + ' '
                # add last string to array
                newLine.append(stringBuilder)
                # print(newLine)
                # line = newLine
                for x in newLine:
                    sectionList.append(x)
            else:
                # line=[line]
                sectionList.append(line)

        # print(line)
        #add space after each paragraph
        sectionList.append('\n')
        for eachPart in sectionList:
            # keep paragraph within same page and if page finished start to new page
            if startHeight-heightReduction+(-emptyLineCount-len(sectionList))*lineDistance<0:
                heightReduction = 0
                canvas.showPage()
                # remind font settings in new page
                canvas.setFont('Verdana', 10)
            # check if decoding is done properly / remove not printable characters
            # print(eachPart.isprintable())
            if eachPart.isprintable():
                # print(f'{eachPart}'.startswith(r'\x'))
                canvas.drawString(1 * cm, (startHeight-heightReduction) * cm, eachPart)
            heightReduction = heightReduction+lineDistance
            # print(startHeight-heightReduction)

    canvas.save()
    f.close()
    print(f'{fileName}.pdf created in main folder')
    # canvas = Canvas('result.pdf', pageSize=(612.0, 792.0))
    # canvas = Canvas('result.pdf', pageSize=(10 * cm, 12 * cm))
    # canvas = Canvas('result.pdf', pageSize=LETTER)

rtfFiles=[]
for (dirPath, dirNames, fileNames) in walk(filePath):
    rtfFiles.extend(fileNames)

for eachFile in rtfFiles:
    if eachFile.endswith('.rtf'): rtfToPdf(filePath,eachFile)
