# -*- coding:utf-8 -*-
# Description: Brief introduction of this file.
# Version: V 0.0
# Author: Yuntian Li
# Date: 2021-08-29 20:02:33
# LastEditTime: 2021-09-04 23:12:04
# LastEditors: Yuntian Li
# Copyright(C): NRIET, Nanjing, China 

# squish modules
import warnings
import squish
import test
import object
import objectMap
# python modules
import time
import random

class Monkey:
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
        chosenObj = self.gui_.chooseRandomObject_()
        
        if (not chosenObj):
            self.warningMsg_("Couldn't find appropriate object for interaction (the choosen GUI object probably vanished suddenly)")
            if (self.failCount_ == 3):
                self.errorMsg_("Failed to find an object appropriate for interaction in three consecutive tries; giving up.")
                return False
        elif (objectMap.realName(chosenObj) == ""):
            self.warningMsg_("Ignoring empty real name for an object (probably a GUI object that vanished while trying to access it)")
            return False
        else:
            self.failCount_ = 0

            statement = self.gui_.statementForObject_(chosenObj)
                
            if (not statement):
                self.warningMsg_("Don't know what script statement to run for objects of type " + str(squish.className(chosenObj)))
            else:
                cmd = statement.toString_()
                try:
                    self.logMsg_(cmd)
                    exec(cmd)
                except Exception as ex:
                    self.warningMsg_(str(ex))
                    self.failCount_ += 1
                    if (self.failCount_ == 3):
                        self.errorMsg_("Failed to find an object appropriate for interaction in three consecutive tries; giving up.")
                        return False
            return True
