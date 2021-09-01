#! /usr/bin/env python
#-*- coding:utf-8 -*-
'''
Description: Brief introduction of this file.
Version: V 0.0
Author: Yuntian Li
Date: 2021-08-29 20:02:33
LastEditTime: 2021-08-29 20:11:01
LastEditors: Yuntian Li
Copyright(C): NRIET, Nanjing, China 
'''
import squish
import objectMap

class ScriptStatement:
    #################### Variables ##################
    name_ = ""
    args_ = []
    
    #################### Functions ##################
    def __init__(self, name):
        self.name_ = name
        self.args_ = []
        
    def addArg_(self, value):
        self.args_.push(value)
    
    def addStringArg_(self, valueStr : str):
        escapedValue = ""
        
        for tmp in valueStr:
            if (tmp == "\\"):
                escapedValue += "\\\\"
            elif (tmp == "\""):
                escapedValue += "\\\""
            else:
                escapedValue += value
            
        self.addArg_("\"" + escapedValue + "\"")
    
    def toString_(self):
        seperator = ','
        tmpStr = name + '(' + seperator.join(self.args_) + ')'
         
        return tmpStr
    
class RawStatement:
    #################### Variables ##################
    code_ = ""
    #################### Functions ##################
    def __init__(self, code):
        self.code_ = code
        
    def toString_(self):
        return self.code_
    
def MakeWaitStatement(obj):
    tmp = ScriptStatement("waitForObject")
    objRealName = objectMap.realName(obj)
    
    if(objRealName == ""):
        if(squish.isNull(obj)):
            raise RuntimeError("Object vanished suddenly.")
        else:
            raise RuntimeError("Can not retrieve real name for a non-null object.")
        
    tmp.addStringArg_(objRealName)
    
    return tmp