# -*- coding:utf-8 -*-
# Description: Brief introduction of this file.
# Version: V 0.0
# Author: Yuntian Li
# Date: 2021-08-29 22:50:49
# LastEditTime: 2021-09-04 23:10:32
# LastEditors: Yuntian Li
# Copyright(C): NRIET, Nanjing, China 

# squish modules
import squish
import test
import object
import objectMap
# python modules
import random
# user modules
import squishStatement as ss
import util

class QtBased:
    ################## class methods ####################
    def __init__(self):
        self.cachedInheritDict_ = {}
        self.maxRandomValue__ = -1
        self.chosenObj_ = None

    def mouseClickXYConstructor_(self, obj):
        statement = ss.ScriptStatement("squish.mouseClick")
        # add mouseClick args : mouseClick(obj, x, y, modifier, button)
        statement.addArg_(ss.makeWaitStatement(obj).toString_()) # waitForObject(obj)
        statement.addArg_(random.randint(0, obj.width)) # x
        statement.addArg_(random.randint(0, obj.height)) # y
        statement.addArg_("squish.Qt.NoModifier") # modifier
        button = "squish.Qt.LeftButton" if (random.random() > 0.5) else "squish.Qt.RightButton"
        statement.addArg_(button)
        
        return statement

    def clickButtonConstructor_(self, obj):
        statement = ss.ScriptStatement("squish.clickButton")
        statement.addArg_(ss.makeWaitStatement(obj).toString_())
        return statement

    def typeConstructor_(self, obj):
        statement = ss.ScriptStatement("squish.type")
        statement.addArg_(ss.makeWaitStatement(obj).toString_())
        statement.addStringArg_(util.makeRandomString(100))
        return statement

    def closeWhatThisConstructor_(self, obj):
        statement = ss.ScriptStatement("squish.sendEvent")
        statement.addArg_("QCloseEvent")
        statement.addArg_("{type='QWhatThis}")
        return statement

    def isA_(self, obj, cn, typeNameFn, inheritsFn):
        if (not self.cachedInheritDict_):
            self.cachedInheritDict_ = {}

        concreteClassName = typeNameFn(obj)
        # check whether concreteClassName is already in the dictionary
        if (concreteClassName in self.cachedInheritDict_):
            if (cn in self.cachedInheritDict_[concreteClassName]):
                return self.cachedInheritDict_[concreteClassName][cn]
        else:
            self.cachedInheritDict_[concreteClassName] = {}

        # get inherits class and save in the dictionary
        result = inheritsFn(obj, cn)
        self.cachedInheritDict_[concreteClassName][cn] = result

        return result

    def isObjectReady_(self, obj):
        try:
            return (squish.waitForObject(obj, 0) != None and obj.visible)
        except:
            return False
    
    def recurseIntoObject(self, obj):
        return True

    def statementForObject_(self, obj, statementConstructors, typeNameFn, inheritsFn):
        # if find corresponding constructor, execute it
        for key in statementConstructors:
            if (self.isA_(obj, key, typeNameFn, inheritsFn)):
                objCallback = statementConstructors[key]
                return objCallback(self, obj)
        # otherwise return none
        return None
    
    def enumCallback_(self, obj, statementConstructors, typeNameFn, inheritsFn):
        if (not QtBased.statementForObject_(self, obj, statementConstructors, typeNameFn, inheritsFn)):
            return self.recurseIntoObject(obj)

        if (not self.isObjectReady_(obj)):
            return self.recurseIntoObject(obj)

        tmp = random.random()
        if (tmp > self.maxRandomValue__):
            self.chosenObj_ = obj
            self.maxRandomValue__ = tmp 

        return self.recurseIntoObject(obj)

    def enumObject_(self, callback, parentObj, statementConstructors, typeNameFn, inheritsFn):
        allObjects = []

        if (not parentObj):
            # if parentObj is None, get all top objects
            allObjects = object.topLevelObjects()
        else:
            # if parentObj is given, get its children objects
            allObjects = object.children(parentObj)

        # recurse into all objects
        for currObj in allObjects:
            if (callback(currObj, statementConstructors, typeNameFn, inheritsFn)):
                self.enumObject_(callback, currObj, statementConstructors, typeNameFn, inheritsFn)

    def chooseRandomObject_(self, statementConstructors, typeNameFn, inheritsFn):
        # if find active QPopupWidget, just return it
        activePopupWidgetM = squish.QApplication.activePopupWidget()
        if (not squish.isNull(activePopupWidgetM)):
            squish.cast(activePopupWidgetM, activePopupWidgetM.metaObject().className())
            return activePopupWidgetM
        
        # if find QModalWidget, make it parentObj
        parentObj = None
        activeModalWidgetM = squish.QApplication.activeModalWidget()
        if (not squish.isNull(activeModalWidgetM)):
            parentObj = activeModalWidgetM

        self.enumObject_(self.enumCallback_, parentObj, statementConstructors, typeNameFn, inheritsFn)
        
        return self.chosenObj_
       
class QtWidgetToolkit(QtBased):
    def inheritsFn_(self, obj, cn):
        ####### This does not work #######
        # return obj.inherits and obj.inherits(cn)
        ##################################
        try:
            return obj.inherits(cn)
            pass
        except Exception as ex:
            return False
            test.fatal("Inherits error: " + str(ex))

    def activateItemConstructor_(self, obj):
        allActions = obj.actions()
        numAction = allActions.count()

        # try each actions randomly until find the first enabled and visible one
        indices = util.makeShuffleIndices(numAction)
        for i in range(0, numAction):
            act = allActions.at(indices[i])
            if (act.enabled and act.visible):
                cleanedStr = str(act.text).replace('&', '')
                if (cleanedStr != "" and cleanedStr != "Close" and cleanedStr != "Quit" and cleanedStr != "Exit"):
                    statement = ss.ScriptStatement("squish.activateItem")
                    statement.addArg_(ss.makeWaitStatement(obj).toString_())
                    statement.addStringArg_(cleanedStr)
                    return statement

        # if no action is founded, exit QMenu
        exitStatement = ss.ScriptStatement("squish.sendEvent")
        exitStatement.addStringArg_("QCloseEvent")
        exitStatement.addStringArg_(objectMap.realName(obj))
        return exitStatement

    def selectComboBoxItemConstructor_(self, obj):
        cmd = "obj=" + ss.makeWaitStatement(obj).toString_() + "\n"
        cmd += "obj.currentIndex = random.randint(0, obj.count)\n"

        return ss.RawStatement(cmd)

    def selectRandomSpinBoxValueConstructor_(self, obj):
        cmd = "obj=" + ss.makeWaitStatement(obj).toString_() + "\n"
        cmd += "obj.value = obj.minimum + random.random() * (obj.maximum - obj.minimum)"

        return ss.RawStatement(cmd)

    def selectRandomTabConstructor_(self, obj):
        test.log("QTab need to be done !")
        
    def selectRandomTableItemConstructor_(self, obj):
        test.log("QTableItem need to be done !")
        
    def selectRandomListItemConstructor_(self, obj):
        test.log("QListItem need to be done !")
    
    def selectRandomTreeItemConstructor_(self, obj):
        test.log("QTreeItem need to be done !")
        
    def chooseRandomObject_(self):
        return QtBased.chooseRandomObject_(self ,self.statementConstructors_, squish.className, self.inheritsFn_);

    def statementForObject_(self, obj):
        return QtBased.statementForObject_(self, obj, self.statementConstructors_, squish.className, self.inheritsFn_);

    statementConstructors_ = {
        "QAbstractButton": QtBased.clickButtonConstructor_,
        "QWhatsThat": QtBased.closeWhatThisConstructor_,
        "QLineEdit": QtBased.typeConstructor_,
        "QScrollBar": QtBased.mouseClickXYConstructor_,
        "QAbstractScrollArea": QtBased.mouseClickXYConstructor_,
        "QMenuBar": activateItemConstructor_,
        "QMenu": activateItemConstructor_,
        "QComboBox": selectComboBoxItemConstructor_,
        "QSpinBox": selectRandomSpinBoxValueConstructor_,
        "QTabWidget" : selectRandomTabConstructor_,
        "QTableWidget" : selectRandomTableItemConstructor_,
        "QListWidget" : selectRandomListItemConstructor_,
        "QTreeWidget" : selectRandomTreeItemConstructor_
    }
    