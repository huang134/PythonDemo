#!/usr/bin/python3

"""
把markdown文件里的本地图片转成Base64嵌入md文件
"""

import base64
import os

# 将md文件里的图片相对路径改成图片数据
def convertImg():
    # 读取原文件内容
    lstPath = os.path.split(os.path.abspath(__file__))
    toConvertMDFile = lstPath[0] + "./Readme.md"
    originalFile = open(toConvertMDFile, 'r', encoding='UTF-8')
    originalContent = originalFile.readlines()
    originalFile.close()

    withImgFile = []

    for lineContent in originalContent:
        if -1 != lineContent.find("![avatar]"):
            beginIndex = lineContent.find("(")
            endIndex = lineContent.find(")")
            toConvertImg = lineContent[beginIndex + 1:endIndex]
            imgFile = open(lstPath[0] + toConvertImg, 'rb')
            imgContent = base64.b64encode(imgFile.read())
            imgFile.close()
            contentTmp = "data:image/png;base64," + str(imgContent, 'UTF-8')
            lineContent = lineContent.replace(toConvertImg, contentTmp)
        withImgFile.append(lineContent)

    # 将内容写入新文件
    newMDFile = lstPath[0] + "./ReadmeWithImg.md"
    newFile = open(newMDFile, 'w', encoding='UTF-8')
    newFile.writelines(withImgFile)
    newFile.close()

if __name__ == "__main__":
    convertImg()