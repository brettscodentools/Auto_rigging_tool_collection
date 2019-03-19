#quick broken FK/IK SwitchBlend Creator

import maya.cmds as cmds
import maya.mel as mel
import re



#------------------ Functions to be used ------------------------------


#Create Visibilty Driven Keys
#it'll be a quick kitbash func without much commenting
def visibilityDrivenKeys( _blendA, _blendB, _blendACtls, _blendBCtls, _attrCurve, _attrSize, *args):
    attrName = _blendA + '_' + _blendB + '_blend'
    blendAttr = _attrCurve + '.' + attrName
    
    blendRangeStart = 0
    blendRangeEnd = int(_attrSize)

    
    cmds.setAttr( blendAttr, blendRangeStart)

    for x in _blendBCtls:
        visibilityAttr = x + '.visibility'
        cmds.setAttr( visibilityAttr, 0)
        cmds.setDrivenKeyframe(visibilityAttr, cd=blendAttr, value=0, driverValue=blendRangeStart)

    for x in _blendACtls:
        visibilityAttr = x + '.visibility'
        cmds.setAttr( visibilityAttr, 1)
        cmds.setDrivenKeyframe(visibilityAttr, cd=blendAttr, value=1, driverValue=blendRangeStart)

    cmds.setAttr( blendAttr, blendRangeEnd)

    for x in _blendACtls:
        visibilityAttr = x + '.visibility'
        cmds.setAttr( visibilityAttr, 0)
        cmds.setDrivenKeyframe(visibilityAttr, cd=blendAttr, value=0, driverValue=blendRangeEnd)

    for x in _blendBCtls:
        visibilityAttr = x + '.visibility'
        cmds.setAttr( visibilityAttr, 1)
        cmds.setDrivenKeyframe(visibilityAttr, cd=blendAttr, value=1, driverValue=blendRangeEnd)

#going to make a function to set up the set driven key functionality..
#..
#
#arguements: bind chain list, the blend a and b, like before and the attribute holding curve (usually the text)..
#.. and the type of constraint (ie: 'orient'), also now the attribute int size (ie: being out of 0-10 range then you would put 10)
def createDrivenKeys( _bindChain, _blendA, _blendB, _conType, _attrCurve, _attrSize, *args):
    #build a string for the blend attr and the attrName from the args
    attrName = _blendA + '_' + _blendB + '_blend'
    blendAttr = _attrCurve + '.' + attrName

    blendRangeStart = 0
    blendRangeEnd = int(_attrSize)

    #step 1: set the bend attr to 0
    cmds.setAttr( blendAttr, blendRangeStart)

    #step 2: loop through the bind joints and set the constraint value for the blendB..
    #.. constraints to 0, and then set the constraint values for the blendA..
    #.. constraints to 1

    for x in _bindChain:
        #construct the driver joint names
        blendADriver = x + '_' + _blendA + '_driver'
        blendBDriver = x + '_' + _blendB + '_driver'

        #save the constraint atter for both a and B
        constraintAttrA = x + '_'+ _conType + 'Constraint1' + '.' + blendADriver + 'W' + '0'
        constraintAttrB = x + '_'+ _conType + 'Constraint1' + '.' + blendBDriver + 'W' + '1'
        cmds.setAttr( constraintAttrB, 0)
        cmds.setAttr( constraintAttrA, 1)

        
    #step 3: set the driven key with both of the constraints weights for the bind joint
    for x in _bindChain:
        #construct the driver joint names
        blendADriver = x + '_' + _blendA + '_driver'
        blendBDriver = x + '_' + _blendB + '_driver'
        
        constraintAttrA = x + '_'+ _conType + 'Constraint1' + '.' + blendADriver + 'W' + '0'
        constraintAttrB = x + '_'+ _conType + 'Constraint1' + '.' + blendBDriver + 'W' + '1'
        
        cmds.setDrivenKeyframe(constraintAttrA, cd=blendAttr, value=1, driverValue=blendRangeStart)
        cmds.setDrivenKeyframe(constraintAttrB, cd=blendAttr, value=0, driverValue=blendRangeStart)
        

    #step 4: set the blend attr to 10
    cmds.setAttr( blendAttr, blendRangeEnd)


    #step 5: flip the constraint settings to weight towards the blend B chain
    #now to swap the constraint values to begin setting up the rest of the settings
    for x in _bindChain:
        #construct the driver joint names
        blendADriver = x + '_' + _blendA + '_driver'
        blendBDriver = x + '_' + _blendB + '_driver'

        #save the constraint atter for both a and B
        constraintAttrA = x + '_'+ _conType + 'Constraint1' + '.' + blendADriver + 'W' + '0'
        constraintAttrB = x + '_'+ _conType + 'Constraint1' + '.' + blendBDriver + 'W' + '1'
        cmds.setAttr( constraintAttrA, 0)
        cmds.setAttr( constraintAttrB, 1)

    #step 6: set the driven key with both of the constraints weights for the bind joint
    for x in _bindChain:
        blendADriver = x + '_' + _blendA + '_driver'
        blendBDriver = x + '_' + _blendB + '_driver'


        constraintAttrA = x + '_'+ _conType + 'Constraint1' + '.' + blendADriver + 'W' + '0'
        constraintAttrB = x + '_'+ _conType + 'Constraint1' + '.' + blendBDriver + 'W' + '1'
        
        cmds.setDrivenKeyframe(constraintAttrA, cd=blendAttr, value=0, driverValue=blendRangeEnd)
        cmds.setDrivenKeyframe(constraintAttrB, cd=blendAttr, value=1, driverValue=blendRangeEnd)

    #that should wrap up this function


#----------------------------------------------------------------------


#make a quick function that will take a list, loop through it and make constraints..
# takes a list, a constraint type string (must match a contraint type), and a child suffix
def constrainToSelection(_sel, _conType, _parent, _offset, *args):
    if _conType == 'parent':
        for x in _sel:
            conParent = x + str(_parent)
            cmds.parentConstraint( conParent, x, mo=(_offset))
    elif _conType == 'point':
        for x in _sel:
            conParent = x + str(_parent)
            cmds.pointConstraint( conParent, x, mo=(_offset))
    elif _conType == 'orient':
        for x in _sel:
            conParent = x + str(_parent)
            cmds.orientConstraint( conParent, x, mo=(_offset))
    elif _conType == 'scale':
        for x in _sel:
            conParent = x + str(_parent)
            cmds.scaleConstraint( conParent, x, mo=(_offset))
    elif _conType == 'aim':
        for x in _sel:
            conParent = x + str(_parent)
            cmds.aimConstraint( conParent, x, mo=(_offset))
    elif _conType == 'pole vector':
        for x in _sel:
            conParent = x + str(_parent)
            cmds.poleVectorConstraint( conParent, x)
    else:
       return 'ERROR NOT A RECOGNIZED CONSTRAINT TYPE'
        



#----------------------------------------------------------------------




#clean curve fuction
#takes a selection list, text string for a name for the curve to be renames too..
#.. if theres no name input the default is to take the first in the selections name
def combineCurves(_sel, _text, *args):
    cShapes = []

    #use a loop to get the children under the curves and put the in the..
    #curve shape list
    for x in _sel:
        temp = cmds.listRelatives(x)
        for c in temp:
            cShapes.append(c)
        #also perform the world parenting and freeze transforms in the loop too 
        cmds.parent(x, w=True)
        cmds.makeIdentity( x, apply=True, t=1, r=1, s=1)


    #real quick lets add a safety selection clear
    cmds.select(cl=True)
    #store the length of the cshapes list to set the loop length
    cshapeLen = len(cShapes)
    # now lets select and combine like in the function below
    for x in cShapes[1:cshapeLen]:
        cmds.select(x, add=True)
    cmds.select(_sel[0], add=True)


    #now mel eval the parent line for whatever dogmatic reason I've decided to keep doing that
    mel.eval('parent -r -s;')

    #store a clean nam for the curve to be renamed to
    cleanName = re.sub('[a-zA-z0-9 \n\.]', '_', _text)
    newName = (cleanName + '_curve')
    cmds.rename(_sel[0], newName)

    #center pivot and freeze transforms
    cmds.select(cl=True)
    cmds.select(newName)
    cmds.xform(cp=True)
    cmds.makeIdentity(mesh, apply=True, t=1, r=1, s=1)
    cmds.select(cl=True)

    #delete the extra curve transforms
    selRange = len(_sel)
    for x in _sel[1:selRange]:
        cmds.delete(x)

    #return the curves new name
    return newName


    
#-----------------------------------------------------------------------

    

#create text curve function 
def simpleTextCurve(_text, _scale, _font = 'Times-Roman', *args):
    #quick and easy command to generate the curves
    outputList = cmds.textCurves( f = _font, t = _text )
    outputName = outputList[0]

    #scale the whole thing real quickly, also center piv and snap to world origin
    cmds.select(cl=True)
    cmds.select(outputName)
    cmds.xform(cp=True)
    cmds.select(cl=True)
    cmds.xform(outputName, ws=True, r=True, s=(_scale,_scale,_scale))
    cmds.move(0,0,0, outputName, rpr=True)
    cmds.makeIdentity( outputName, apply=True, t=1, r=1, s=1)

    #list the objects under the text object output
    groups = cmds.listRelatives(outputName)
    curves = []
    cShapes = []
    #do some quick looping to get the curves under the objects
    for x in groups:
        temp = cmds.listRelatives(x)
        for c in temp:
            curves.append(c)
    #do some quick looping to get the curve shapes under the curves
    for y in curves:
        temp = cmds.listRelatives(y)
        for c in temp:
            cShapes.append(c)
 

    # parent all ctls to the world and ..
    # .. freeze the transforms on all the curves so that they merge nicely
    for x in curves:
        cmds.parent(x, w=True)
        cmds.makeIdentity( x, apply=True, t=1, r=1, s=1)


    #now to clean up the text curves into one simple and clean curve
    shapeRange = len(cShapes)
    #before I got selecting things all willie nilly lets clear any potential selections
    cmds.select(cl=True)
    #select all but the first curve shape (since will be slecting its actual curve)
    for x in cShapes[1:shapeRange]:
        cmds.select(x, add=True)
    #now select the top curve to parent the shapes under
    cmds.select(curves[0], add=True)


    #now mel eval the parent line for whatever dogmatic reason I've decided to keep doing that
    mel.eval('parent -r -s;')
     
    #make a replace regular expressions line to nix any special characters and make..
    #.. a rename str to rename the curve with
    cleanName = re.sub('[^a-zA-z0-9]', '_', _text)
    newName = (cleanName + '_curve')
    cmds.rename(curves[0], newName)

    #center pivot and freeze new ctl
    cmds.select(cl=True)
    cmds.select(newName)
    cmds.xform(cp=True)
    cmds.move(0,0,0, newName, rpr=True)
    cmds.makeIdentity(newName, apply=True, t=1, r=1, s=1)
    cmds.select(cl=True)

    #then delete the extra containers
    curveRange = len(curves)
    for x in curves[1:curveRange]:
        cmds.delete(x)

    #delete extra groups 
    for x in groups:
        cmds.delete(x)
    #now delete the original text curve output to wrap it all up
    cmds.delete(outputName)

    #return the curve name so you can take that later for doing shit
    return newName


#-----------------------------------------------------------------------




#A function for putting fk ctls onto a bind chain, and arranges them in hierarchy
# takes a selection array 
def attachFKCtls( _sel, _blendChain, *args):
    numOfSelections = len(_sel)
    for index, x in enumerate(_sel):
        blendJointName = x + '_' + _blendChain + '_driver'
        blendCtlName = blendJointName + '_ctl'
        blendCtlGrp = blendJointName + '_group' 

        #call the make sphere curve function to pit out a 
        makeSphereCurve()

        #rename the sphere ctl curve to the new name for the fk chain
        cmds.rename('temp_sphere1', blendCtlName)

        #move the ctl to the joint location
        #store location first
        xPos = cmds.xform( x, q = True, ws = True, t = True)
        
        #then move the clt
        cmds.xform( blendCtlName, ws=True, t= xPos )
        cmds.select(cl=True)
        cmds.select(blendCtlName)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1)
        cmds.select(cl=True)

        #now group the ctl and move the group piv to the same position
        cmds.group(n=blendCtlGrp, em=True)
        cmds.xform(blendCtlGrp, ws = True, sp = xPos, rp = xPos)

        #now parent the ctl(child) to the group(parent)
        cmds.parent(blendCtlName, blendCtlGrp)
        
        #a just in case selection clearing for good house keeping
        cmds.select(cl=True)
        
        #now match the group rotation with the joint orient
        bindJointOrientToAttr( x, blendCtlGrp, 'rotate' )


    #now finally parent the ctls in a hierarchy that makes sense to
    for index, y in enumerate(_sel[1:numOfSelections], 1):
        parentIndex = index - 1
        blendCtlGrp = y + '_' + _blendChain + '_driver_group'
        parentCtl = str(_sel[parentIndex] + '_' + _blendChain + '_driver_ctl')
        
        print(str(blendCtlGrp))
        print(str(parentCtl))

        try:
            cmds.parent(blendCtlGrp, parentCtl)
        except:
            print('Index is ' + str(index) +  ', but the parenting did not work for whatever reason (for the fk ctls)')
            pass



#-----------------------------------------------------------------------


#lets turn the process of making two aditional joints chains a function
#takes a 3 joint select array, and then what its blending between
#lets turn the process of making two aditional joints chains a function
#takes a 3 joint select array, and then what its blending between
def makeBlendJointChains( _sel, _blendA, _blendB, *args):

    #lists to return the joint chains
    blendAChain = []
    blendBChain = []

    for index, x in enumerate(_sel):
        #save the name modified names of the joint in the loop to name the duplicates with
        blendAJointName = x + '_' + _blendA + '_driver'
        blendBJointName = x + '_' + _blendB + '_driver'
        
        blendAChain.append(blendAJointName)
        blendBChain.append(blendBJointName)

        #store the postiion and orient values for the joint in the loop
        bindJointPos = cmds.xform( x, q = True, ws = True, t = True)

        #the joint creation lines
        cmds.joint( n = blendAJointName, p = bindJointPos)
        #seperate with a healthy house keeping selection clear
        cmds.select(cl=True)
        
        cmds.joint( n = blendBJointName, p = bindJointPos)
        #seperate with a healthy house keeping selection clear
        cmds.select(cl=True)

        #set the orient values for the FK joint
        bindJointOrientToAttr( x, blendAJointName, 'jointOrient' )

        #set the orient values for the IK joint
        bindJointOrientToAttr( x, blendBJointName, 'jointOrient' )

        #check the enumeration index, if it's 0 then nothing needs to be done..
        #.. if its 1 then parent the object to index 0.. if it's 2 then parent to index 1
        #.. use try and excepts to catch errors
        if index == 0:
            print('index is 0, do nothing to see here')
            continue
        if index == 1:
            try:
                cmds.parent(blendAJointName, (str(_sel[0] + '_fk_driver')))
                cmds.parent(blendBJointName, (str(_sel[0] + '_ik_driver')))
            except:
                print('Index is 1, but the parenting did not work for whatever reason')
                pass
        if index == 2:
            try:
                cmds.parent(blendAJointName, (str(_sel[1] + '_fk_driver')))
                cmds.parent(blendBJointName, (str(_sel[1] + '_ik_driver')))
            except:
                print('Index is 2, but the parenting did not work for whatever reason')
                pass


    #store the would be names of groups for the duplicate joint chains
    blendAGrp = (str(_sel[0] + '_' + _blendA + '_chain_group'))
    blendBGrp = (str(_sel[0] + '_' + _blendB + '_chain_group'))

    #now to create a group to store each of the duplicate joint chains..
    #.. also freeze the transforms and
    cmds.group((str(_sel[0] + '_' + _blendA +'_driver')), n = blendAGrp)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1)
    cmds.select(cl=True)
    cmds.group((str(_sel[0] + '_' + _blendB + '_driver')), n = blendBGrp)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1)
    cmds.select(cl=True)

    #store the position of the base joint of the the bind chain
    basePos = cmds.xform((str(_sel[0])), q = 1, ws = 1, rp = 1)

    #change the rotate and scale pivots for both chain groups to the..
    #.. location of the base joint in the bind chain 
    cmds.xform(blendAGrp, ws = True, sp = basePos, rp = basePos)
    cmds.xform(blendBGrp, ws = True, sp = basePos, rp = basePos)

    #a healthy selection clearing for good house keeping
    cmds.select(cl=True)

    #select the base of the skin bind joint chain and pickwalk up to the parent joint
    cmds.select((str(_sel[0])))
    cmds.pickWalk(direction='up')

    #save that selection in a string to call in a parent constrain command
    pConst = cmds.ls(sl=True)

    #parent constrain the joint chain groups (contrainee/child) to the parent of the..
    #.. bind skin joint chain base joint (constrainor/parent).
    cmds.parentConstraint( pConst, blendAGrp, mo=True)
    cmds.parentConstraint( pConst, blendBGrp, mo=True)

    #return a two lists, one with the blendA joint chain, and the blendB joints chain
    blendChainLists = [blendAChain, blendBChain]
    return  blendChainLists





#----------------------------------------------------------------------



#update-------
#a function for transfering joint orient to attr
#update------

#note to self this wont work 100 percent on the joint heierachy. itll screw up ..
#around the hips or anything with more than one joint under it

#changing how this function works, this will instead aim constraint the target..
#.. to the next joint down the chain without maintaining offset.. then delete the constraint..
#.. and then takes the rotation on the target, stores it, sets it back to 0 and..
#.. then finally putting it on the target attr..

def bindJointOrientToAttr( _joint, _target, _attr, *args):
    
    #going to sort out what the "L_" or "R_" prefix is or if there is none at all..
    #.. then do a loop where i reference the locator's rotation and either..
    #.. put it right to the target or mirror the rotation to 

    #pickwalk down from the joint heirachy to get the next joint
    cmds.select(cl=True)
    cmds.select(_joint)
    cmds.pickWalk(direction='down')
    y = cmds.ls(sl=True)
    cmds.select(cl=True)
    #use it to make an aim constraint down the driection the joint would be..
    #.. oriented
    cmds.aimConstraint( y, _target, mo=False)
    
    #store the rotations made by the aim constraint
    bindJointOrientX = cmds.getAttr(_target + '.rotateX')
    bindJointOrientY = cmds.getAttr(_target + '.rotateY')
    bindJointOrientZ = cmds.getAttr(_target + '.rotateZ')

    #now delete the aim constraint and zero out the rotate values
    aConstName = _target + '_aimConstraint1'
    cmds.delete(aConstName)

    #zeroing out rotates
    cmds.setAttr(str(_target + '.rotateX'), 0)
    cmds.setAttr(str(_target + '.rotateY'), 0)
    cmds.setAttr(str(_target + '.rotateZ'), 0)

    #now put the stored aim constraint rotations down the line onto the target attr
    cmds.setAttr(_target + '.' + _attr +'X', bindJointOrientX)
    cmds.setAttr(_target + '.' + _attr +'Y', bindJointOrientY)
    cmds.setAttr(_target + '.' + _attr +'Z', bindJointOrientZ)


#----------------------------------------------------------------------


#a function for the plane pv locating method
#also input the selection array because when this runs the script(s) is on..
#.. will probably have cleared selection by the time this needs to be run
def planeToPVLocation( _sel, _zDistance, *args):
    #quick broken FK/IK SwitchBlend Creator

    zMV = -(_zDistance)
    jL = _sel

    #set up the pole vector by creating a triangle greo and snapping the verts to the joints in the ik chain and then grabbing the one for the elbow or knee and moveing it in Z axis
    #then moving the traingle Ctl to the space in component and I think grabbing the rotation off the middle vertex rotate pivot or something and putting that on to the Ctl
    #then make it the pole vector constrainor of the ik handle

    #lets make a plane and merge two of the verts the 3rd and 4th and then make a short loop to snap them to the joints
    pN = 'pv_plane'
    cmds.polyPlane(n = pN, sx=1,sy=1, w=1, h=1)

    cmds.polyMergeVertex('pv_plane.vtx[2]', 'pv_plane.vtx[3]', d = 1.5)

 
    #I wanted to come up with a more clever way of reading the names for the Vertex and matching them up with the number in the array they should correspond to
    #but for time Im making it less dynamic and more just getting this done because this is a specific part of the tool I can hard code out a lil

    #get the locations for the joints
    jL1  = cmds.xform( jL[0], q = 1, ws = 1, t = 1)
    jL2 = cmds.xform( jL[1], q = 1, ws = 1, t = 1)
    jL3 = cmds.xform( jL[2], q = 1, ws = 1, t = 1)

    #move the vertex to the locations
    cmds.xform('pv_plane.vtx[0]', ws = True, t = jL1)
    cmds.xform('pv_plane.vtx[1]', ws = True, t = jL3)
    #this is for the merged vertex or the point and it should go on the jL2 because thats the knee number
    cmds.xform('pv_plane.vtx[2]', ws = True, t = jL2) 

    cmds.select(cl=True)

    #now move the pv vertex it in the v axis in its normals
    cmds.moveVertexAlongDirection( "pv_plane.vtx[2]",  v= zMV)

    #return the target vertex and the plane name to allow to delete the plane later
    returns = ['pv_plane.vtx[2]','pv_plane']
    return returns


#-------------------------------------------------------------------


# A function for making the sphere ctl curve
def makeSphereCurve( _name = 'temp_sphere1', *args ):
    #create a circle on each axis
    cmds.circle( n = ('temp_circle1'), nr=(0, 0, 1), c=(0, 0, 0), r = 17 )
    cmds.circle( n = ('temp_circle2'), nr=(0, 1, 0), c=(0, 0, 0), r = 17 )
    cmds.circle( n = ('temp_circle3'), nr=(1, 0, 0), c=(0, 0, 0), r = 17 )

    #use a list real quick to hole the temp names
    cParts = ['temp_circle1', 'temp_circle2', 'temp_circle3']
    #make an empty list for the shapes to go in for the selection precombine
    combineList =[]

    # a little enumerate loop to grab the curve shapes and store em
    for index, x in enumerate(cParts):
        #if its the cirst curve which will be the parent object to the shapes
        if index == 0:
            #select it
            cmds.select(x)
            #store the name 
            y = cmds.ls(sl=True)
            #clear the selection
            cmds.select(cl=True)

            #add the selection to the list
            combineList.append(y)

        #for these two in the index I grab the underlying shape then..
        # .. store it all the same
        if index == 1:
            cmds.select(x)
            cmds.pickWalk(direction='down')
            y = cmds.ls(sl=True)
            print(y)
            cmds.select(cl=True)
            combineList.append(y)

        if index == 2:
            cmds.select(x)
            cmds.pickWalk(direction='down')
            y = cmds.ls(sl=True)
            print(y)
            cmds.select(cl=True)
            combineList.append(y)
    
    #selection clear for good house keeping
    cmds.select(cl=True)

    #select the shapes and then then lastly chose the "containing" curve
    cmds.select(combineList[1])
    cmds.select(combineList[2], add = True)
    cmds.select(combineList[0], add = True)
    mel.eval('parent -r -s;')
    cmds.select(cl=True)

    #delete the extra empty transforms
    cmds.delete(cParts[1])
    cmds.delete(cParts[2])

    #now just delete the construction history on the new curve and blamo its done
    cmds.select(cl=True)
    cmds.select('temp_circle1')
    cmds.delete(ch=True)
    cmds.select(cl=True)
    cmds.rename('temp_circle1', _name)
    cmds.select(cl=True)
        
    




#----------------------- end of Functions ---------------------------






#------------------- tool code starts here -------------------------
def fkIKSwitchMaker(*args): 
    #Had an arg where I took the offset field in but its easier to reference it..
    pvZoffField = cmds.intField( pvZOffsetField, q=1, v=1)

    #make a selection array to store the joint chain selected
    sel = cmds.ls(sl=True)
    pvZoffset = pvZoffField

    #a healthy good house keeping selection clearing
    cmds.select(cl=True)


    #update!!
    #first loop: loops the joints for thier positions and orient values and creates..
    #.. the joints for both of the extra blend joint chains
    #   use an enumerate to get index to make parenting them a little easier.'''
    #update!!
    # made this process into a function to be ran to make the chains for both fk and ik
    blndA = 'fk'
    blndB = 'ik'
    blendChains = makeBlendJointChains(sel, blndA, blndB)

    #a safety selection clear
    cmds.select(cl=True)


    #store a quick string names for the handle 
    ikN = (str(sel[2] + '_IK_handle'))
    ikS = (str(sel[0] + '_ik_driver'))
    ikE = (str(sel[2] + '_ik_driver'))

    #create the IK handle for the IK joint chain
    cmds.ikHandle(n= ikN, sj = ikS, ee = ikE, sol = 'ikRPsolver')

    #update!!
    #run the function to attach sphere fk controlls to the 'fk' chain
    #update!! made this a function
    attachFKCtls( sel, 'fk')

    #store some names really quickly for the ik ctl and the pv ctl and thier groups
    ikJointName = (sel[2] + '_ik_driver')
    ikCtlName = (ikJointName + '_ctl')
    ikCtlGrp = (ikJointName + '_group')
    pvCtlName = (ikJointName + '_pv_ctl')

    #make the curves for the IK handle and PV ctl curves and rename them
    makeSphereCurve()
    cmds.rename('temp_sphere1', ikCtlName)
    cmds.select(cl=True)

    makeSphereCurve()
    cmds.rename('temp_sphere1', pvCtlName)
    cmds.select(cl=True)


    #snap the IK handle ctl to the ik handle position, first storeing the Pos, and then snapping
    ikPos = cmds.xform( ikN, q = True, ws = True, t = True)
    cmds.xform( ikCtlName, ws=True, t= ikPos )

    #Freeze transforms on the pv ctl
    cmds.select(cl=True)
    cmds.select(ikCtlName)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1)
    cmds.select(cl=True)


    #now group and snap group piv to ik ctl
    cmds.group(n=ikCtlGrp, em=True)
    cmds.xform(ikCtlGrp, ws = True, sp = ikPos, rp = ikPos)

    #now parent the ctl (child) to the group (parent)
    cmds.parent(ikCtlName, ikCtlGrp)

    #A healthy just incase selection clear
    cmds.select(cl=True)

    #set the rotation for the IK handle Ctl
    bindJointOrientToAttr( sel[2], ikCtlGrp, 'rotate' )

    #snap the PV ctl to its needed pos (use the polyplane method) more specifically the function
    pvReturns = planeToPVLocation( sel, pvZoffset)
    pvTar = pvReturns[0]
    pvPos = cmds.xform( pvTar, q = True, ws = True, t = True)
    cmds.xform( pvCtlName, ws=True, t= pvPos )

    #Freeze transforms on the pv ctl
    cmds.select(cl=True)
    cmds.select(pvCtlName)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1)
    cmds.select(cl=True)

    #also delete the plane when were doing moveing things around
    cmds.delete(pvReturns[1])

    #make the switch text ctl curve
    #real quick add a part that makes it for the prefix for the name
    buildCurveName = simpleTextCurve('fk/ik', 20, 'Times-Roman')
    blendCurve = sel[0] + '_' + buildCurveName

    cmds.rename(buildCurveName, blendCurve)

    # snap it behind the wrist
    wPos = cmds.xform( sel[2], q = True, ws = True, t = True)
    cmds.xform(blendCurve, ws=True, t = wPos)
    cmds.xform(blendCurve, ws=True, r=True, t=(0,0,-35))

    #group the blend curve and then make the group parented (child) to..
    #.. the bind shoulder (parent)

    #make the curve group
    bCGrp = blendCurve + '_group'
    cmds.group(n=bCGrp, em=True)

    #snap its pivot to where the fk/ik switch is positioned 
    txtPos = cmds.xform( blendCurve, q = True, ws = True, t = True)
    cmds.xform(bCGrp, ws = True, sp = txtPos, rp = txtPos)

    #parent the text curve to the group 
    cmds.parent(blendCurve, bCGrp)

    #now start the constraining off with the parent constrain from..
    #..the bind shoulder (parent) to the txt group (child)

    #clear selection and group the position for the bind shoulder
    cmds.select(cl=True)
    cmds.select((str(sel[0])))
    cmds.pickWalk(direction='up')

    #save that selection in a string to call in a parent constrain command
    txtConstP = cmds.ls(sl=True)
    cmds.parentConstraint( txtConstP, bCGrp, mo=True)

    #constrain the fk ctls to the fk joints
    constrainToSelection(blendChains[0], 'orient', '_ctl', True)

    #constain the IK handle ctls to the IK handle, and the PV constrain the PV ctl..
    cmds.pointConstraint( ikCtlName, ikN)

    #before we pole vector lets actually do the orient on the wrist joint for the ik handle chain
    ikChain = blendChains[1]
    ikWrist = ikChain[2]
    cmds.orientConstraint( ikCtlName, ikWrist, mo=True)

    #now finally pole vector constrain the ik handle
    cmds.poleVectorConstraint(pvCtlName, ikN)

    #Loop through the bind joint chain and then orient constain the bind joints(constrainee/child)..
    #.. to the fk and ik joint chaints(constrainor/parents) so that it's doubled up like..
    #.. in my previous fk/ik switches
    constrainToSelection(sel, 'orient', '_fk_driver', True)
    constrainToSelection(sel, 'orient', '_ik_driver', True)

    #Create the fk/ik blend attr in the txt ctl curve
    attrName = blndA + '_' + blndB + '_blend'
    cmds.select(cl=True)
    cmds.select(blendCurve)
    cmds.addAttr(ln=attrName, at=  'long' , defaultValue=0, minValue=0, maxValue=10, k=True )
    cmds.select(cl=True)

    #now group all the groups into few more convienient groups
    ikCtlsGrpName = sel[2] + blndB + '_ctl_group'
    cmds.group(n=ikCtlsGrpName,em=True)
    cmds.parent(ikCtlGrp, ikCtlsGrpName)
    cmds.parent(pvCtlName, ikCtlsGrpName)

    #then set up the set driven key connection
    createDrivenKeys( sel, blndA, blndB, 'orient', blendCurve, 10)

    #really quickly going to just hook up this to arrays to make the visibility.
    #just going to change out the joint names
    blendACtl = [(sel[0] +'_fk_driver_ctl'), (sel[1]+'_fk_driver_ctl'), (sel[1] + '_fk_driver_ctl')]
    blendBCtl = [(sel[2] + '_ik_driver_ctl'), (sel[2] + '_ik_driver_pv_ctl')]

    #make the visibility set driven keys
    visibilityDrivenKeys( blndA, blndB, blendACtl, blendBCtl, blendCurve, 10)




#------------------------END OF ACTUAL TOOL------------------------------







 #--------------------UI Elements and Variables-------------------------
popUp = cmds.window(title = "Fk/IK switch maker", sizeable=False, resizeToFitChildren=True)
cmds.rowColumnLayout(numberOfColumns = 3, columnWidth = [(5, 150), (5, 1500), (5, 150)])
cmds.text(label='')
cmds.text(label="Set PV Z Offset:")
cmds.text(label='')

cmds.text(label='')
pvZOffsetField = cmds.intField( minValue=-900, maxValue=900, value=40 )
cmds.text(label='')

cmds.text(label='')
cmds.text(label='it works in negative values')
cmds.text(label='')

cmds.text(label='')
cmds.text(label='ie: setting back for an elbow : 40')
cmds.text(label='')

cmds.text(label='')
cmds.text(label='ie: setting front for a knee : -40')
cmds.text(label='')

cmds.text(label='')
cmds.text(label='')
cmds.text(label='')

cmds.text(label='')
cmds.text(label='Instructions:')
cmds.text(label='')

cmds.text(label='')
cmds.text(label='just have the three joint chain bind chain selected from start to end')
cmds.text(label='')

cmds.text(label='')
cmds.text(label='')
cmds.text(label='')

cmds.text(label='')
cmds.button(label = "Build Fk/IK Switch", command = fkIKSwitchMaker)
cmds.showWindow(popUp)