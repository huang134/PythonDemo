#!/usr/bin/python3

# param1 1.xlsx                 翻译文件
# param2 l1:t1,l2:t2            待翻译的参数 l1-语言标识（Chinese、English等）t1-ts文件名
# "args": ["./Thai/泰语文案.xlsx", "Thai:./Thai/MFCore_Thai.ts,Thai:./Thai/Feedback_Thai.ts,Thai:./Thai/LiveUpdate_Thai.ts,Thai:./Thai/Register_Thai.ts"]
# 根据ts文件名生成对应qm文件

import os
import sys
import pandas as pd
from xml.etree.cElementTree import parse, Element
import threading
import time

# 多语言字典 <sourceText, <languageType, translatedText>>
languageDict = dict()

# 生成多语言字典
def generateLanguageDict(translatedDocIn, languageDictIn):
    df = pd.ExcelFile(translatedDocIn)

    for sheet in df.sheet_names:
        sdf = pd.read_excel(translatedDocIn, sheet)

        # print(sdf.columns)
        for indexTmp in sdf.index:
            i = 0
            source = ""
            dictTmp = dict()
            for columnTmp in sdf.columns:
                # 需要先找到源文本
                if (-1 != columnTmp.lower().find('source') or -1 != columnTmp.lower().find('english') or -1 != columnTmp.lower().find('英语')) and (0 == len(str(source).strip())):
                    source = sdf.loc[indexTmp].values[i]
                    # print(i, "source = ", source)
                elif (len(str(source).strip()) != 0):
                    dictTmp[columnTmp] = sdf.loc[indexTmp].values[i]
                    # print(i, columnTmp, sdf.loc[indexTmp].values[i])
                i += 1
            # print(dictTmp)

            languageDictIn[source] = dictTmp
        break
    
    # print(languageDictIn)

releaseTool = 'D:/Qt/Qt5.6.3/5.6.3/msvc2013_64/bin/lrelease.exe'

class processThread (threading.Thread):
    def __init__(self, languageType, tsFile):
        threading.Thread.__init__(self)
        self.languageType = languageType
        self.tsFile = tsFile
    def run(self):
        sys.stdout.write("开始线程：" + " " + self.languageType + " " + self.tsFile + " " + time.ctime(time.time()) + "\n")
        modifyTS(self.languageType, self.tsFile)
        # 将ts转成qm
        exeLine = releaseTool + ' ' + self.tsFile + ' -qm' + ' ./' + os.path.splitext(self.tsFile)[0] + '.qm'
        os.popen(exeLine)
        sys.stdout.write("退出线程：" + " " + self.languageType + " " + self.tsFile + " " + time.ctime(time.time()) + "\n")

# 对ts文件进行源匹配替换
def modifyTS(languageType, tsFile):
    doc = parse(tsFile)
    root = doc.getroot()
    for context in root:
        for message in context:
            sourceMatch = ""
            for nodeTmp in message:
                if -1 != nodeTmp.tag.find('source'):
                    if nodeTmp.text in languageDict and languageType in languageDict[nodeTmp.text]:
                        sourceMatch = languageDict[nodeTmp.text][languageType]
                elif -1 != nodeTmp.tag.find('translation') and len(sourceMatch) != 0:
                    nodeTmp.text = sourceMatch
                    if 'type' in nodeTmp.attrib:
                        nodeTmp.attrib.pop('type')
    doc.write(tsFile, 'UTF-8')

# 生成qm文件
def generateQM():
    if len(sys.argv) < 3:
        print('parameter input error')
        return

    translatedDoc = sys.argv[1]
    toProcessList = sys.argv[2]

    generateLanguageDict(translatedDoc, languageDict)

    lstProcess = toProcessList.split(',')

    # 对列表参数进行校验
    lstUnique = []
    for process in lstProcess:
        if not process in lstUnique:
            lstUnique.append(process)

    threads = []
    for process in lstUnique:
        lstTmp = process.split(':')
        if len(lstTmp) < 2:
            print('parameter input error')
        
        thread = processThread(lstTmp[0], lstTmp[1])
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

if __name__ == "__main__":
    generateQM()
