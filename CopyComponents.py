#!/usr/bin/python3

"""
 使用：
    copy_components.py "MFCore,AppUpdater"
 说明：
    1、支持从发布目录拷贝和从开发目录拷贝两种方式
"""

from git.repo import Repo
import os
import platform
import shutil
import sys
import threading
import time

fromRelease = True
fromDevelop = False

isWin64 = False

forceCopy = True

fromPathPrefix = "/../.."
toLibPathPrefix = "./lib/win"
toResPathPrefix = "./res/conf"

toMacLicPathPrefix = "./lib/mac"

# 拉取最新内容并切换到对应分支
def pullProcess(workPath, branch = "developer"):
    if not os.path.exists(workPath):
        print("%s is not exist" % workPath)
        return

    repository = Repo(workPath)
    repository.git.pull()

    repository.git.checkout(branch)

# 拉取组件最新内容
def pullComponents():
    pullProcess(os.getcwd() + fromPathPrefix + "/MFFoundation/MFFoundation_Release")
    pullProcess(os.getcwd() + fromPathPrefix + "/MFControl/MFControl_Release")
    pullProcess(os.getcwd() + fromPathPrefix + "/MFCore/MFCore_Release")
    pullProcess(os.getcwd() + fromPathPrefix + "/AppUpdater/AppUpdater_Release")
    pullProcess(os.getcwd() + fromPathPrefix + "/Feedback/Feedback_Release")
    pullProcess(os.getcwd() + fromPathPrefix + "/MFRegister/MFRegister_Release")

class pullThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sys.stdout.write("开始线程：" + " 拉取最新内容 " + time.ctime(time.time()) + "\n")
        pullComponents()
        sys.stdout.write("退出线程：" + " 拉取最新内容 " + time.ctime(time.time()) + "\n")

# 判断文件/文件夹是否存在再拷贝
def copyWrap(sourcePath, targetPath, filter = ""):
    if os.path.isdir(sourcePath):
        if os.path.exists(sourcePath):
            if os.path.exists(targetPath):
                shutil.rmtree(targetPath)
            shutil.copytree(sourcePath, targetPath)
            toRemoveFile = str(filter)
            if len(toRemoveFile) != 0:
                lstRemove = toRemoveFile.split(',')
                for removeTmp in lstRemove:
                    if os.path.exists(targetPath + "/" + removeTmp):
                        os.remove(targetPath + "/" + removeTmp)
    elif os.path.isfile(sourcePath):
        if os.path.exists(sourcePath):
            shutil.copy(sourcePath, targetPath)
    else:
        print(sourcePath, "special file, maybe file path is error")

# MFCore拷贝
def copyMFCore():
    print("copyMFCore %s" % os.getcwd())

    if platform.system() == "Darwin" or forceCopy:
        # MFFoundation
        copyWrap(os.getcwd() + "%s/MFFoundation/MFFoundation_Release/lib/mac/libMFFoundation.dylib.dSYM" % (fromPathPrefix), "%s/MFFoundation/libMFFoundation.dylib.dSYM" % (toMacLicPathPrefix))
        copyWrap(os.getcwd() + "%s/MFFoundation/MFFoundation_Release/lib/mac/libMFFoundation.dylib" % (fromPathPrefix), "%s/MFFoundation/" % (toMacLicPathPrefix))
    
        # MFFoundation
        copyWrap(os.getcwd() + "%s/MFControl/MFControl_Release/lib/mac/libMFControl.dylib.dSYM" % (fromPathPrefix), "%s/MFControl/libMFControl.dylib.dSYM" % (toMacLicPathPrefix))
        copyWrap(os.getcwd() + "%s/MFControl/MFControl_Release/lib/mac/libMFControl.dylib" % (fromPathPrefix), "%s/MFControl/" % (toMacLicPathPrefix))
    
        # MFCore
        copyWrap(os.getcwd() + "%s/MFCore/MFCore_Release/lib/mac/libMFCore.dylib.dSYM" % (fromPathPrefix), "%s/MFCore/libMFCore.dylib.dSYM" % (toMacLicPathPrefix))
        copyWrap(os.getcwd() + "%s/MFCore/MFCore_Release/lib/mac/libMFCore.dylib" % (fromPathPrefix), "%s/MFCore/" % (toMacLicPathPrefix))
    else:
        if isWin64:
            fromDir = "x64"
            architectureDir = "Release_x64"
            toDir = "x64"
        else:
            fromDir = "x32"
            architectureDir = "Release"
            toDir = "Win32"

        # MFFoundation
        copyWrap(os.getcwd() + "%s/MFFoundation/MFFoundation_Release/lib/win/%s/MFFoundation.lib" % (fromPathPrefix, fromDir), "%s/%s/MFFoundation/" % (toLibPathPrefix, toDir))
        copyWrap(os.getcwd() + "%s/MFFoundation/MFFoundation_Release/lib/win/%s/MFFoundation.dll" % (fromPathPrefix, fromDir), "%s/%s/MFFoundation/" % (toLibPathPrefix, toDir))
        copyWrap(os.getcwd() + "%s/MFFoundation/MFFoundation_Release/lib/win/%s/MFFoundation.lib" % (fromPathPrefix, fromDir), "%s/%s/MFFoundation/" % (toLibPathPrefix, toDir))

        # MFControl
        copyWrap(os.getcwd() + "%s/MFControl/MFControl_Release/lib/win/%s/MFControl.lib" % (fromPathPrefix, fromDir), "%s/%s/MFControl/" % (toLibPathPrefix, toDir))
        copyWrap(os.getcwd() + "%s/MFControl/MFControl_Release/lib/win/%s/MFControl.dll" % (fromPathPrefix, fromDir), "%s/%s/MFControl/" % (toLibPathPrefix, toDir))
        copyWrap(os.getcwd() + "%s/MFControl/MFControl_Release/lib/win/%s/MFControl.pdb" % (fromPathPrefix, fromDir), "%s/%s/MFControl/" % (toLibPathPrefix, toDir))

        # openssl
        copyWrap(os.getcwd() + "%s/MFFoundation/MFFoundation_Release/lib/win/%s/libeay32.dll" % (fromPathPrefix, fromDir), "%s/%s/openssl/" % (toLibPathPrefix, toDir))
        copyWrap(os.getcwd() + "%s/MFFoundation/MFFoundation_Release/lib/win/%s/ssleay32.dll" % (fromPathPrefix, fromDir), "%s/%s/openssl/" % (toLibPathPrefix, toDir))

        if fromRelease:
            # MFCore
            copyWrap(os.getcwd() + "%s/MFCore/MFCore_Release/lib/win/%s/MFCore.lib" % (fromPathPrefix, fromDir), "%s/%s/MFCore/" % (toLibPathPrefix, toDir))
            copyWrap(os.getcwd() + "%s/MFCore/MFCore_Release/lib/win/%s/libMFCore.dll" % (fromPathPrefix, fromDir), "%s/%s/MFCore/" % (toLibPathPrefix, toDir))
            copyWrap(os.getcwd() + "%s/MFCore/MFCore_Release/lib/win/%s/libMFCore.pdb" % (fromPathPrefix, fromDir), "%s/%s/MFCore/" % (toLibPathPrefix, toDir))
        elif fromDevelop:
            # MFCore
            copyWrap(os.getcwd() + "%s/MFCore/MFCore/output/%s/MFCore.lib" % (fromPathPrefix, architectureDir), "%s/%s/MFCore/" % (toLibPathPrefix, toDir))
            copyWrap(os.getcwd() + "%s/MFCore/MFCore/output/%s/libMFCore.dll" % (fromPathPrefix, architectureDir), "%s/%s/MFCore/" % (toLibPathPrefix, toDir))
            copyWrap(os.getcwd() + "%s/MFCore/MFCore/output/%s/libMFCore.pdb" % (fromPathPrefix, architectureDir), "%s/%s/MFCore/" % (toLibPathPrefix, toDir))

            # conf
            copyWrap(os.getcwd() + "/../../../MFCore/MFCore/output/{0}/language".format(architectureDir), "../res/conf/MFCore/language")
            copyWrap(os.getcwd() + "/../../../MFCore/MFCore/output/{0}/skin".format(architectureDir), "../res/conf/MFCore/skin")

# AppUpdater拷贝
def copyAppUpdater():
    print("copyAppUpdater %s" % os.getcwd())

    if platform.system() == "Darwin":
        print("TODO")
    else:
        if isWin64:
            architectureDir = "Release_x64"
            toDir = "x64"
        else:
            architectureDir = "Release"
            toDir = "Win32"

        if fromRelease:
            # AppUpdater
            if isWin64:
                copyWrap(os.getcwd() + "%s/AppUpdater/AppUpdater_Release/vs2013-x64/appAutoUpdate.exe" % (fromPathPrefix), "%s/%s/AppUpdater/" % (toLibPathPrefix, toDir))
            else:
                copyWrap(os.getcwd() + "%s/AppUpdater/AppUpdater_Release/appAutoUpdate.exe" % (fromPathPrefix), "%s/%s/AppUpdater/" % (toLibPathPrefix, toDir))

            # conf
            copyWrap(os.getcwd() + "%s/AppUpdater/AppUpdater_Release/language" % (fromPathPrefix), "%s/AppUpdater/language" % (toResPathPrefix), "main/language.ini")
            copyWrap(os.getcwd() + "%s/AppUpdater/AppUpdater_Release/skin" % (fromPathPrefix), "%s/AppUpdater/skin" % (toResPathPrefix))
            copyWrap(os.getcwd() + "%s/AppUpdater/AppUpdater_Release/LiveUpdateSetting" % (fromPathPrefix), "%s/AppUpdater/" % (toResPathPrefix))
        elif fromDevelop:
            # conf
            copyWrap(os.getcwd() + "%s/AppUpdater/AppUpdater/output/%s/language" % (fromPathPrefix, architectureDir), "%s/AppUpdater/language" % (toResPathPrefix), "main/language.ini")
            copyWrap(os.getcwd() + "%s/AppUpdater/AppUpdater/output/%s/skin" % (fromPathPrefix, architectureDir), "%s/AppUpdater/skin" % (toResPathPrefix))
            copyWrap(os.getcwd() + "%s/AppUpdater/AppUpdater/output/%s/LiveUpdateSetting" % (fromPathPrefix, architectureDir), "%s/AppUpdater/" % (toResPathPrefix))

# Feedback拷贝
def copyFeedback():
    print("copyFeedback %s" % os.getcwd())

    if platform.system() == "Darwin":
        print("TODO")
    else:
        if isWin64:
            fromDir = "x64"
            architectureDir = "Release_x64"
            toDir = "x64"
        else:
            fromDir = "x32"
            architectureDir = "Release"
            toDir = "Win32"

        if fromRelease:
            copyWrap(os.getcwd() + "%s/Feedback/Feedback_Release/win/%s/Feedback.exe" % (fromPathPrefix, fromDir), "%s/%s/Feedback/" % (toLibPathPrefix, toDir))

            # conf
            copyWrap(os.getcwd() + "%s/Feedback/Feedback_Release/win/FeedbackRes" % (fromPathPrefix), "%s/Feedback/FeedbackRes" % (toResPathPrefix))
        elif fromDevelop:
            copyWrap(os.getcwd() + "%s/Feedback/Feedback/output/%s/Feedback.exe" % (fromPathPrefix, architectureDir), "%s/%s/Feedback/" % (toLibPathPrefix, toDir))
            copyWrap(os.getcwd() + "%s/Feedback/Feedback/output/%s/zlib1.dll" % (fromPathPrefix, architectureDir), "%s/%s/Feedback/" % (toLibPathPrefix, toDir))

            # conf
            copyWrap(os.getcwd() + "%s/Feedback/Feedback/output/%s/FeedbackRes" % (fromPathPrefix, architectureDir), "%s/Feedback/FeedbackRes" % (toResPathPrefix))

# MFRegister拷贝
def copyMFRegister():
    print("copyMFRegister %s" % os.getcwd())

    if platform.system() == "Darwin":
        print("TODO")
    else:
        if isWin64:
            fromDir = "x64"
            architectureDir = "Release_x64"
            toDir = "x64"
        else:
            fromDir = "x32"
            architectureDir = "Release"
            toDir = "Win32"

        if fromRelease:
            print("TODO")
            # 版本不一致
        elif fromDevelop:
            copyWrap(os.getcwd() + "%s/MFRegister/MFRegister/output/%s/MFRegister.lib" % (fromPathPrefix, architectureDir), "%s/%s/MFRegister/" % (toLibPathPrefix, toDir))
            copyWrap(os.getcwd() + "%s/MFRegister/MFRegister/output/%s/SoftMgr.dll" % (fromPathPrefix, architectureDir), "%s/%s/MFRegister/" % (toLibPathPrefix, toDir))

            # conf
            copyWrap(os.getcwd() + "%s/MFRegister/MFRegister/output/%s/language" % (fromPathPrefix, architectureDir), "%s/MFRegister/language" % (toResPathPrefix), "main/language.ini")
            copyWrap(os.getcwd() + "%s/MFRegister/MFRegister/output/%s/RegisterRes" % (fromPathPrefix, architectureDir), "%s/MFRegister/language" % (toResPathPrefix))
            copyWrap(os.getcwd() + "%s/MFRegister/MFRegister/output/%s/skin" % (fromPathPrefix, architectureDir), "%s/MFRegister/language" % (toResPathPrefix))

# 根据不同组件拷贝文件
def copyComponentFile(componentType):
    if componentType == "MFCore":
        copyMFCore()
    elif componentType == "AppUpdater":
        copyAppUpdater()
    elif componentType == "Feedback":
        copyFeedback()
    elif componentType == "MFRegister":
        copyMFRegister()
    else:
        return

class processThread (threading.Thread):
    def __init__(self, component):
        threading.Thread.__init__(self)
        self.component = component
    def run(self):
        sys.stdout.write("开始线程：" + " " + self.component + " " + time.ctime(time.time()) + "\n")
        copyComponentFile(self.component)
        sys.stdout.write("退出线程：" + " " + self.component + " " + time.ctime(time.time()) + "\n")

# 拷贝对应的组件
def copyComponents():
    # 只添加了带翻译的组件，依赖组件主要从MFCore组件拷贝
    lstToCopyComponent = ["MFCore", "AppUpdater", "Feedback", "MFRegister"]

    if len(sys.argv) == 2:
        toCopyComponent = sys.argv[1]
        lstToCopyComponent = toCopyComponent.split(',')

    if fromRelease:
        pull = pullThread()
        pull.start()
        pull.join()

    threads = []
    for componentType in lstToCopyComponent:
        thread = processThread(componentType)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

if __name__ == "__main__":
    copyComponents()