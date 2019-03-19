import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets


# creating a basic window class that I can use in future scripts to create a quick..
#.. PyQt window that I can then build upon and add other features or create other..
#.. window types or boiler plate code


class basicWindow(object):
    # This object takes two arguements: height and widgth, to set the window size to
    def __init__(self, _height, _width):
        self.winHeight = _height
        self.winWidth = _width

    # the main function to run the window and set the size and layout (an empty form layout)..
    #.. 
    def main(self):
        #creating the application (in the event this isnt used in maya - commented out by default -)
        #app = QtWidgets.QApplication(sys.argv)

        #setting the .win attribute to the object to the QtWidget (basic window object)
        self.win = QtWidgets.QWidget()
        #call the QWidget method to resize the window, I set to the object attributes..
        #.. for height and width
        self.win.resize(self.winWidth, self.winHeight)
        
        #stick a basic form layout into the QWidget (window)
        mainLayout = QtWidgets.QFormLayout()

        #call the show method in the widget (window) 
        self.win.show()
        #then raise the window
        self.win.raise_()

        #basic close func (in the event this isnt used in maya - commented out by default -)
        sys.exit(app.exec_())

#creates basic window object
window = basicWindow( 300, 600)
#runs the main method to create the window
window.main()
