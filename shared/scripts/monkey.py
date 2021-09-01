#! /usr/bin/env python
#-*- coding:utf-8 -*-
'''
Description: Brief introduction of this file.
Version: V 0.0
Author: Yuntian Li
Date: 2021-08-29 20:02:33
LastEditTime: 2021-08-29 20:10:39
LastEditors: Yuntian Li
Copyright(C): NRIET, Nanjing, China 
'''
import squish
import test
import object
import objectMap

import time

class Monkey:
    ################ Variables ###################
    app_ = "" # Name of AUT
    gui_ = None # type of QtToolKit
    
    failCount_ = 0 # count of failed cmds
    logFp_ = None # file pointer of write log msg
    
    totalOpNum_ = 0 # total operations of test
    totalTime_ = 0 # total time of test

     
    ################ Functions ###################
    # -------------------------------- #
    # initialization 
    def __init__(self, app, gui, totalOpNum = -1, totalTime = -1):
        self.app_ = app
        self.gui_ = gui
        
        self.totalOpNum_ = totalOpNum
        self.totalTime_ = totalTime
    
        self.failCount_ = 0
        self.logFp_ = open("output.csv", "w+")
   
    # -------------------------------- #
    # print log msg to the test results window
    def logMsg_(self, msg : str):
        test.log(msg)
    
    # -------------------------------- #
    # print warning msg to the test results window
    def warningMsg_(self, msg : str):
        test.warning(msg)
    
    # -------------------------------- #
    # print error msg to the test results window
    def errorMsg_(self, msg : str):
        test.fatal(msg)
        
    # -------------------------------- #
    # exit Flag
    def exitControl_(self, opCount : int, elapsedTime : float):
        # exit when reach maximum operations num
        if (self.totalOpNum_ != -1 and opCount >= self.totalOpNum_):
            return True
        
        # exit when reach maximum operations time
        if (self.totalTime_ != -1 and elapsedTime >= self.totalTime_):
            return True
        # otherwise continue
        return False
        
    # --------------------------------- #
    # run the monkey test
    def run_(self):
        squish.startApplication(self.app_)
        
        self.failCount_ = 0
        
        opCount = 0
        initTime = time.time()
        while (True):
            # exit if reach the maximum operations or times
            opCount += 1
            elapsedTime = time.time() - initTime
            
            if(self.exitControl_(opCount, elapsedTime)):
                break
            # try run the Monkey test
            try:
                self.guardedRun_()
            except Exception as ex:
                self.warningMsg_("Error occurred : " + str(ex))
                squish.snooze(1)
        
        self.logMsg_("Monkey test Done, result summaries are given below:\n")
        self.logMsg_("Passes: " + str(test.resultCount("passes")))
    # -------------------------------- #
    # guarded run of monkey
    def guardedRun_(self):
        pass