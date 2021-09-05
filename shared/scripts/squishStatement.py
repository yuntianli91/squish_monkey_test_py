# -*- coding:utf-8 -*-
# Description: Brief introduction of this file.
# Version: V 0.0
# Author: Yuntian Li
# Date: 2021-08-29 20:02:33
# LastEditTime: 2021-09-04 20:33:54
# LastEditors: Yuntian Li
# Copyright(C): NRIET, Nanjing, China 

# squish modules
import squish
import objectMap

class ScriptStatement:  
    #################### Functions ##################
    def __init__(self, name):
        self.name_ = name
        self.args_ = []
        
    def addArg_(self, value):
        self.args_.append(str(value))
    
    def addStringArg_(self, valueStr : str):
        escapedValue = ""   
        for tmp in valueStr:
            if (tmp == "\\"):
                escapedValue += "\\\\"
            elif (tmp == "\""):
                escapedValue += "\\\""
            else:
                escapedValue += tmp
            
        self.addArg_("\"" + escapedValue + "\"")
    
    def toString_(self):
        # make sure all args are Python str
#         args = [str(i) for i in self.args_]
        
        seperator = ','
        tmpStr = self.name_ + '(' + seperator.join(self.args_) + ')'
         
        return tmpStr
    
class RawStatement:
    #################### Functions ##################
    def __init__(self, code):
        self.code_ = code
        
    def toString_(self):
        return self.code_
    
def makeWaitStatement(obj):
    tmp = ScriptStatement("squish.waitForObject")
    objRealName = objectMap.realName(obj)
    
    if(objRealName == ""):
        if(squish.isNull(obj)):
            raise RuntimeError("Object vanished suddenly.")
        else:
            raise RuntimeError("Can not retrieve real name for a non-null object.")
        
    tmp.addStringArg_(objRealName)
    
    return tmp