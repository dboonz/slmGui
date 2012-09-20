import numpy as np
try :
  import wx
  from wx import Button
except ImportError :
  raise ImportError, "The wxPython module is required to run this program"
#
#from Tkinter import Checkbutton, IntVar, BooleanVar, Button, Label, PhotoImage, StringVar, Radiobutton
#from Tkinter import Entry
#
class slmGui(wx.Frame):
  def __init__(self,parent,id=-1,title='SLM control'):
    self.figureRoot = wx.Frame.__init__(self,parent,id,title)
    self.parent = parent
    self.initialize()

  def initialize(self):
    # add sizer
    self.sizer = wx.GridBagSizer()

    # add buttons:
    self.applyButton = wx.Button(self,-1,label="Apply")
    self.sizer.Add(self.applyButton,(10,10))
    self.Bind(wx.EVT_BUTTON,self.ProcessInputAndWritePhase,self.applyButton)

    self.sineObject = SinFunction(self)
    self.activeObject = self.sineObject

    self.sizer.AddGrowableCol(0)
    self.SetSizerAndFit(self.sizer)
    self.Show(True)
#
  def ProcessInputAndWritePhase(self,event):
    self.activeObject.processInput()
    # update graph
    self.updateGraph()
    self.writePhase()
#  
  def updateGraph(self):
    print "UpdateGraph not implemented"
#
  def writePhase(self):
    print "writePhase: Not implemented"
#

# all functions should have the same properties:
class PhaseFunction():
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


class SinFunction(PhaseFunction):
  def returnFunction(self):
    return lambda w: self.amp*sin(self.w*w+self.phi)

  def initialize(self):
    print "Initializing sinFunction"
    # relevant variables:
    self.amp = 1.
    self.w   = 1.
    self.phi = 1

    # create entry boxes for the different props:
    self.entryAmp = wx.TextCtrl(self.parent,-1,value=u"Amp")
    self.parent.sizer.Add(self.entryAmp,(1,1),(1,1),wx.EXPAND)

    self.entryW = wx.TextCtrl(self.parent,-1,value=u"W")
    self.parent.sizer.Add(self.entryW,(2,1),(1,1),wx.EXPAND)

    self.entryPhi = wx.TextCtrl(self.parent,-1,value=u"Phi")
    self.parent.sizer.Add(self.entryPhi,(3,1),(1,1),wx.EXPAND)

  def processInput(self):
    " update amp, w and phi, and display"
    print "You entered: "
    try : 
      self.amp = float(self.entryAmp.GetValue())
      self.w   = float(self.entryW.GetValue())
      self.phi = float(self.entryPhi.GetValue())
    except ValueError :
      print "One of the entries is not a number!"
      #TODO : create an error dialog
    
    print "parameters will be: "
    print "  A : %f" % self.amp
    print "  w : %f" % self.w
    print "  phi:%f" % self.phi


if __name__ == '__main__':
  app = wx.App()
  frame = slmGui(None,-1,'testing title')
  app.MainLoop()
#  gui = slmGui(None)
#  gui.mainloop()

