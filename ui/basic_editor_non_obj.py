#save 006
import maya.cmds as cmds
import os
import re
import threading
from functools import partial
#script editor script to be used to both be used as my pop up on the fly button function editor, as well as replacing the maya default script editor for the intellisense


#NEEDED Additions--------------------------------

#DONT FORGET! remember when I get to the point of adding this (or even just fixing some of the UI elements scaling and updating) to anything go back and put it in an object oriented format and start working from there out in object orientation
       #------------- I intend to do that so the tools I use or make in mark 2 can be basically directly appended to the next autorigger's API package


#Lets try to kill two birds with one stone and finish out this window to be my new script editor to replace the maya one

#basically ill make this one for being called in editor mode in my ui to edit button scripts to streamlined workflow (without the big history part and instead the small bar, no tabbed editors,)

#------------------------------------------------
#Buttons for saving scripts
#a function, that opens this with the script file associated with UI buttons
#a history bar on the bottom to catch errors

#A button to try to execute the script in the window, and one to run selections to catch errors 

# compile/update/reload function so I can stop opening and reopening maya to update scripts that I change
#include tabbed script editor opener (for stand alone use)

#oh and make ui update! like when you click the color changes or some shit 

#-------------------------------

newScriptEditorName = "ScriptEditor2"

"""
put a class here to define buttons and give a stored script location from the..
maya scripts folder

"""

#so the best way it looks like to do this is to just store the variables in their object attrs..
#.. and also call the button command with the connected attrs in the INIT and just leave..
#.. a callback method to return the location of the script.
class newButton (object):
    def __init__(self, _label, _commandMeth, _width, _scriptLoc, *args):
        self.scriptLoc = _scriptLoc
        cmds.button(label = _label, command = _commandMeth, width = _width )
    
    def scriptLocCallback(self):
        return self.scriptLoc



"""
This is where I'm keeping my functions all together before running the rest of the script editor window
v v v

"""
#basically like my editor function down below although it creates the part of the window where it reports the history of the editor
#as well as displays and returns from the code or error messages -- I'll make it adjustable in the layout but its base will be enough for 1
# or two lines
#            I made the show var report instead since its a reporter and so it seems to fit thematically

def echoAllCommandsSwitch():
    
    return


def clearHistory():
    return
    

def executeAllInWindow(_scriptEditorId, *args):
	cmds.cmdScrollFieldExecuter(_scriptEditorId, edit = True, executeAll = True)
	return
    
#takes one arguement, the Id or number or object or whatever for the script edtior in the window, or tab, to execute the selected text   
def executeSelectionInWindow(_scriptEditorId, *args):
    cmds.cmdScrollFieldExecuter(_scriptEditorId, edit = True, execute = True)
    return

    #this function ? ? ? will be refered to change the UI in the event of needing the change a button or append a tab or whatever
def updateWindowUI():  
    return
    #this function ? ? ? will be referred to and run in the save button script to make it so I do no have to keep relaunching maya
    #and It might need to compile the script and do a reload command (idk check this again later future me)    
def updateScripts():
    return
def getButtonScript():
    return
def saveButtonScript():
    return

#these are for the general editor, not the on the fly editor, as that'll keep just one editor window and saveing to the script to the button
def addNewEditorTab():
    return
    
def saveToShelfOptionsWindow():
    return

def saveScriptToShelf(x, *args):
    return
def saveScriptAsFile(_scriptEditorId, *args):
    scriptSaveName = str(cmds.fileDialog2(fileMode = 0))
    scriptSaveName = scriptSaveName[3:-2]
    print(scriptSaveName)
    
    scriptFile = open(scriptSaveName, 'w')
    
    cmds.cmdScrollFieldExecuter(_scriptEditorId, e = True, sla = True)
    scriptText = str(cmds.cmdScrollFieldExecuter(_scriptEditorId, q = True, slt = True))
    #print(scriptText)
    
    #trying to break down the lines in these commented out lines of code
    #because when i open the file that gets written out to in regular notepad all the text is on one line with no breaks
    #although when I open it in notepad++ its got seperate lines.
    
    newData = scriptText.split('\n')
    print(newData)
    
    
    #-----------OLD ISSUE THAT IS NOW RESOLVED---------------------
    #okay new issue is that as is this loop will write with formatting except for one space per space between written text will be
    # ommited from the formating, which is wierd because all empty lines should be the same, and not inconsistent like that
    
    
    #probably not efficient but here Im storing the length of the new data from the for loop to be called later with
    # also storing it so that I can just take 1 off and use it as a var for the index of the final line in the code to be saved 
    #commenting out the print statements until i need them again
    scriptLineCount = len(newData)
    scriptLastLine = int(scriptLineCount - 1)
    #print('the length of the new Data list is:' + str(scriptLineCount))
    #print('the correct last line number is:' + str(scriptLastLine))


    
    for i in range(len(newData)):
        if i == 0:
            writeLine = (newData[i] + '\r')
        elif i == (scriptLastLine):
            #checking if this elif is actually working
            #print('IT USED THE ELIF STATEMENT!!!!')
            writeLine = ('\n' + newData[i])
        else:
            writeLine = ('\n' + (newData)[i] + '\r')
        print('line-' + str(i) + ' :' + writeLine)
        scriptFile.write(writeLine)
        #scriptFile.write('\n\r')
        
    #scriptFile.write(scriptText)
    scriptFile.close()
    
    return

"""
^ ^ ^
This is where I'm keeping my functions all together before running the rest of the script editor window

"""

"""
This is where the editor window itself will be made V V V
"""

def showNewEditorWindow(_show, *args):
    
    windowWidth = 400
    windowHeight = 300

    #window command to define the window
    cmds.window(newScriptEditorName, title = 'Script Editor', width = windowWidth, height = windowHeight, minimizeButton = True, maximizeButton = True)

    #define a form layout and store it in a variable
    form = cmds.formLayout()

    #define and save a cmdScrollFieldExecutor (basically maya equivelent to the pyqt editor command) as a variable
    scriptEditor = cmds.cmdScrollFieldExecuter( width=200, height=330, sourceType="python", showLineNumbers = True)
    #important to note that saving it as a variable returns  the window number (correspoinding to the resulting object I assume),
    #        a form layout number, and cmds scroll field executor all divided by an "|" character
    #print(scriptEditor)

    #calling the split command isolates the return from scriptEditor var into a list   
    lst = scriptEditor.split('|')
    
    #use a simple list length -1 call on the list to store the last item (the cmdScrollFieldExecutorNumber) as a variable
    scriptEditorId = lst[len(lst) -1]
    
    
    
    #real quickly going to try to store the reporter as a variable to be called and attached to the form layout
    scriptReporter = cmds.cmdScrollFieldReporter(width = 900, height = 70)
    rLst = scriptReporter.split('|')
    scriptReporterId = rLst[len(rLst) -1]
    
    #making some row column layouts to call in, both 
    fileRow = cmds.rowLayout()
    #for whatever reason maya cannot find this object when later referenced
    cmds.setParent('..')
    runRow = cmds.rowLayout()
    
    
    #form layout when used to attach forms needs to call a layout object?
    #and I'm using the form layout thats stored as for
    if _show ==True:
        cmds.cmdScrollFieldExecuter(scriptEditor, edit=True)    
        cmds.formLayout(form, edit=True, attachForm=[(scriptEditorId, "top", 35), (scriptEditorId, "bottom", 125), (scriptEditorId, "left", 5), (scriptEditorId, "right", 5), (scriptReporterId, "bottom", 40), (scriptReporterId, "left", 42), (scriptReporterId, "right", 5), (fileRow, "top", 5), (runRow, "bottom", 5), (runRow, "right", 20), (runRow, "left", 20)])
        
        
        #start adding buttons for the functions
        
        #the row for the execute buttons
        cmds.rowLayout(runRow, numberOfColumns = 2)
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(label = "Execute All", command = partial(executeAllInWindow, scriptEditorId), width = 450)
        cmds.setParent('..')
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(label = "Execute Selection", command = partial(executeSelectionInWindow, scriptEditorId), width = 450) 
        
        #these set parents move the next ui element up the layout hierarchy
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..') 
        #the row for the save and reporter buttons
        cmds.rowLayout(fileRow, numberOfColumns = 4) 
        saveScriptFileButton = cmds.button(label = "Save To Shelf", command = partial(saveScriptAsFile, scriptEditorId), width = 225)
        saveScriptFileButton = cmds.button(label = "Save As File", command = partial(saveScriptAsFile, scriptEditorId), width = 225)
        saveScriptFileButton = cmds.button(label = "Toggle Echo All", command = partial(saveScriptAsFile, scriptEditorId), width = 225)
        saveScriptFileButton = cmds.button(label = "Clear Reporter", command = partial(saveScriptAsFile, scriptEditorId), width = 225)
        

           
        #run window  
        cmds.showWindow()
        return

#quick if loop to close the window if it already exits before launching the window
if cmds.window("ScriptEditor2", exists=True):
    cmds.deleteUI("ScriptEditor2")

#launch the window    
showNewEditorWindow(True)