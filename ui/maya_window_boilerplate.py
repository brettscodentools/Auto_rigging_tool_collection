import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sip 

import maya.cmds as cmds
import maya.OpenMayaUI as mui
import maya.OpenMaya as om

# creating a basic window class that I can use in future scripts to create a quick..
#.. PyQt window that I can then build upon and add other features or create other..
#.. window types or boiler plate code

#this class will inherit from the QWidget class
class BasicWindow(QtGui.QDialog):
    # This object takes two arguements: height and widgth, to set the window size to
    def __init__(self, _height, _width, *args, **kwargs):
        super(basicWindow, self).__init__()
        self.resize(_height, _width)
        

#boiler plate function for maya ui to get the main window
def getMainWindow():
    #get a pointer to the maya main window using the main window mqt util
    pointer = mui.MQtUtil.mainWindow()

    #convert the return swig object to its memory location
    convPointer = long(pointer)

    #now store the main window by wrapping it with sip
    mainWindow = sip.wrapInstance(conPointer, QtCore.QObject)
    # now return the main window qobject 
    return mainWindow


def show():
    #store the main window with the funct 
    mainWin = getMainWindow()
    #now make the window
    win = BasicWindow(800, 600, parent = mainWin)
    
    #now do the show and raise
    win.show()
    win.raise_()

    #return the window
    return win 