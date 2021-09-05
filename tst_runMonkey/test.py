# -*- coding:utf-8 -*-
# Description: Brief introduction of this file.
# Version: V 0.0
# Author: Yuntian Li
# Date: 2021-09-01 23:38:11
# LastEditTime: 2021-09-04 20:55:17
# LastEditors: Yuntian Li
# Copyright(C): NRIET, Nanjing, China 

import names
from monkey import Monkey
import qtToolkits

def main():
    myMonkey = Monkey("addressbook", qtToolkits.QtWidgetToolkit(), totalTime=1000)
    
    myMonkey.run_()