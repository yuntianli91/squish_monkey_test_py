#! /usr/bin/env python
#-*- coding:utf-8 -*-
'''
Description: Brief introduction of this file.
Version: V 0.0
Author: Yuntian Li
Date: 2021-08-29 19:57:56
LastEditTime: 2021-08-29 20:10:45
LastEditors: Yuntian Li
Copyright(C): NRIET, Nanjing, China 
'''
import object

import random
import math

def makeRandomString(strLen : int):
    charLists = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    charLen = len(charLists)
    result = "";
    for i in tange(0, strLen):
        result += chars[math.floor(random.random() * charLen)]
    
    return result;

def enumObject(enumCallback, parentObj):
    allObjects = ()
    
    if (not parentObj):
        allObjects = object.topLevelObjects()
    else:
        allObjects = object.children(parentObj)
        
    for obj in allObjects:
        if(enumCallback(obj)):
            enumObject(enumCallback, parentObj)
