#shoulder pauldron rigger tool
import maya.cmds as cmds
import maya.mel as mel
import 

#---------------------------- functions to be used ---------------------------

# base pop-up window function to be used down the line to call windows for..
# .. various reasons
def basicPopUp(*args):

# function to make a pop up to que selecting the pauldron mesh then run..
# .. a skin bind to the the pauldron joint 
def selectPauldronPopUp( *args):


# a basic function to create a locator between two joints or objects
# asically its going to make a 2 value ep curve and so there will be a uniform..
# .. middle cv point and ill stick a locator there.
# takes two arguements start object and end object | returns locator object name
def locToMidpoint( _start, _end, *args):
        #storing variables here
        tempCurveName = 'TempLineCurve'

        #store two translate locations for the start and end of the curve
        startPos = cmds.xform( _start, q = True, ws = True, t = True)
        endPos = cmds.xform( _end, q = True, ws = True, t = True)

        #create a curve using the translate locations from the xform..
        #.. of the start and end items
        cmds.curve(tempCurveName, )

        #snap the location of the 
        cmds.xform( blendCtlName, ws=True, t= xPos )



# a basic function to create 2 locators at the 1st and 2nd thirds..
# ..of a line segment between two objects
# basically its going to make a 3 value ep curve and so there will be a uniform..
# .. cv point on the thirds points and I'll stick a locators there.
# takes two arguements start object and end object | returns locator object names
def locToThirds( _start, _end, *args): 






#--------------------------- actual tool starts here -------------------------

#start of with a selection of the clav and shoulder (or possibly hips and thigh?? check on this later)..
#.. ps the last item should be the elbow.
sel = cmds.ls(sl=True)

for index, x in enumerate(sel):
    if index == 0:
        jName = cmds.joint()
        cmds.joint

#--------------------------- UI and Window Elements --------------------------
