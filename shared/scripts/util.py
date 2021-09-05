# -*- coding:utf-8 -*-
# Description: Brief introduction of this file.
# Version: V 0.0
# Author: Yuntian Li
# Date: 2021-08-29 19:57:56
# LastEditTime: 2021-09-04 20:26:48
# LastEditors: Yuntian Li
# Copyright(C): NRIET, Nanjing, China 

# python modules
import random
import math

def makeRandomString(strLen : int):
    charLists = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    
    charLen = len(charLists)
    for i in range(0, strLen):
        result += charLists[math.floor(random.random() * charLen)]
    
    return result;

def makeShuffleIndices(indicesLen : int):
    tmp = []
    for i in range(0, indicesLen):
        tmp.append(i)

    random.shuffle(tmp)
    return tmp
