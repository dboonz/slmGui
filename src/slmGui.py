import numpy as np
import Tkinter

from Tkinter import Checkbutton, IntVar, BooleanVar, Button, Label, PhotoImage, StringVar, Radiobutton
from Tkinter import Entry

class slmGui(Tkinter.Tk):
  def __init__(self,parent):
    self.figureRoot = Tkinter.Tk.__init__(self,parent)
    self.parent = parent
    self.initialize()

  def initialize(self):
    self.title('SLM control')
    # add buttons:
    self.applyButton = Button(self.parent,
        text = "Apply",
        command = self.ProcessInputAndWritePhase)
    self.applyButton.grid(column = 50, row = 70)
    self.cosineObject = CosFunction(self.parent)
    self.activeObject = self.cosineObject

  def ProcessInputAndWritePhase(self):
    self.activeObject.processInput()
    # update graph
    self.writePhase()

  def writePhase(self):
    print "writePhase: Not implemented"


# all functions should have the same properties:
class PhaseFunction:
  def __init__(self,parent,startRow=1, startCol=1):
    self.parent = parent
    self.initialize()
    # create a bounding box
    #
  def initialize(self):
    """ This function should set all relevant variables and create any graphical
    interface objects """
    print "Not implemented!"

  def returnFunction(self):
    "Return a pure function, dependent on the frequency"
    return lambda l: None
  def processInput(self):
    """"This function should process all the input that was given to graphical
    interface objects. """
    pass

class CosFunction(PhaseFunction):
  def returnFunction(self):
    return lambda w: self.amp*cos(self.w*w+self.phi)

  def initialize(self):
    self.amp = 1.
    self.w   = 1.
    self.phi = 0
    self.inputAmp = createInputField(self.parent,30,1,self.amp,text="A [rad]")
    self.inputW = createInputField(self.parent,30,2,self.w,text="w [/fs]")
    self.inputPhi = createInputField(self.parent,30,3,self.phi,text="phi [rad]")
#
#    self.inputAmp = Tkinter.Entry(self.parent)
#    self.inputAmp.insert(0,str(self.amp))
#    self.inputAmp.grid(row=10,column=10)
#    self.inputW = Tkinter.Entry(self.parent)
#    self.inputW.grid(row=11,column=10)
#    self.inputPhi = Tkinter.Entry(self.parent)
#    self.inputPhi.grid(row=12,column=10)
#    self.inputTest = createInputField(self.parent,3,13,10,text="bla")
#
  
  def processInput(self):
    try :
      self.amp = float(self.inputAmp.get())
      self.w = float(self.inputW.get())
      self.phi = float(self.inputPhi.get())
    except :
      print "Error, cannot convert " + self.inputAmp.get() + "to float"

    print "parameters will be: "
    print "  A : %f" % self.amp
    print "  w : %f" % self.w
    print "  phi:%f" % self.phi
    

def createInputField(parent,startCol,startRow, initialValue,text = None):
  entry = Tkinter.Entry(parent)
  entry.insert(0,str(initialValue))
  entry.grid(row = startRow,column=startCol)
  if(text is not None):
    Label(parent,text=text+'   ').grid(row = startRow, column =
        startCol-1,sticky='E')
  return entry
    

if __name__ == '__main__':
  gui = slmGui(None)
  gui.mainloop()

