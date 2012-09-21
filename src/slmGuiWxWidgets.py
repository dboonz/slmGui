import numpy as np
try :
  import wx
  from wx import Button
except ImportError :
  raise ImportError, "The wxPython module is required to run this program"

import numpy
import numpy as np
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas

from matplotlib.backends.backend_wx import NavigationToolbar2Wx


class Plotter(wx.Panel):
  " Simple plotter class"
  def __init__(self,parent):
    self.parent = parent
    wx.Panel.__init__(self,parent,-1,size=(50,50))
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.figure = matplotlib.figure.Figure()
    self.ax1 = self.figure.add_subplot(211)
    self.ax2 = self.figure.add_subplot(212,sharex=self.ax1)
    self.figure.subplots_adjust(hspace=0.5)
    t = np.linspace(0,1,100)
    y1 = np.sin(t)
    y2 = np.cos(t)
    self.ax1.plot(t,y1)
    self.ax1.set_xlabel("Wavelength [nm]")
    self.ax1.set_ylabel("Phase [rad]")
    self.ax2.plot(t,y2)
    self.canvas = FigureCanvas(self,-1,self.figure)
    self.sizer.Add(self.canvas)
    self.navtoolbar = NavigationToolbar2Wx(self.canvas)
    self.sizer.Add(self.navtoolbar)
    self.SetSizer(self.sizer)
    self.Fit()


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
    self.sizer.Add(self.applyButton,(4,5))
    self.Bind(wx.EVT_BUTTON,self.ProcessInputAndWritePhase,self.applyButton)

    # add notebook
    self.nb = wx.Notebook(self,-1)
    self.nb.sizer = wx.GridBagSizer()
    
    self.sine = FunctionObjectWrapper(self.nb,SinFunction)
    self.cosine = FunctionObjectWrapper(self.nb,CosFunction)

    self.nb.AddPage(self.cosine,"Cosine")
    self.nb.AddPage(self.sine,"Sine")
    
    
    self.activeObject = self.cosine.phasefun
    
    self.sizer.Add(self.nb,(1,5),(2,4),wx.EXPAND)

    # add plot
    self.plot = Plotter(self)
    self.sizer.Add(self.plot,(1,1),(4,4),wx.EXPAND)

    self.sizer.AddGrowableCol(0)
    
    self.SetSizerAndFit(self.sizer)
    self.Show(True)
#
  def ProcessInputAndWritePhase(self,event):
    # get page
    print self.nb.GetCurrentPage() # returns the current tab number
    self.activeObject = self.nb.GetCurrentPage().phasefun
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

class FunctionObjectWrapper(wx.Panel):
  """ This is a function object wrapper. Because we want the instances of
  PhaseFunction to inherit from Phasefunction, they do not inherit from
  wx.Panel. So this is just to provide wx.Panel, and a grid manager """
  def __init__(self,parent,PhaseFunctionReference):
    """ Constructor. Argument: Reference to the function class you want to be put in """
    wx.Panel.__init__(self,parent)
    self.sizer = wx.GridBagSizer()
    self.phasefun = PhaseFunctionReference(self)
    self.SetSizerAndFit(self.sizer)

  def __str__(self):
    return "Current phase function: " + self.phasefun.__str__()
    

    #SinFunction(self)



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


class CosFunction(PhaseFunction):
  "SHOULD BE KEPT! REMOVE SINFUNCTION!"
  def __str__(self):
    return "Cosine!"
  def returnFunction(self):
    return lambda w: self.amp*cos(self.w*w+self.phi)

  def initialize(self):
    print "Initializing sinFunction"
    # relevant variables:
    self.amp = 1.
    self.w   = 1.
    self.phi = 1

    # create entry boxes for the different props:
    amptext = wx.StaticText(self.parent,-1,label="Amp [rad]")
    self.parent.sizer.Add(amptext,(1,1),(1,1))
    self.entryAmp = wx.TextCtrl(self.parent,-1,value=u"0")
    self.parent.sizer.Add(self.entryAmp,(1,2),(1,1),wx.EXPAND)
    
    wtext = wx.StaticText(self.parent,-1,label="w [rad]")
    self.parent.sizer.Add(wtext,(2,1),(1,1),wx.RIGHT)
    self.entryW = wx.TextCtrl(self.parent,-1,value=u"0")
    self.parent.sizer.Add(self.entryW,(2,2),(1,1),wx.EXPAND)

    phitext = wx.StaticText(self.parent,-1,label="phi [rad]")
    self.parent.sizer.Add(phitext,(3,1),(1,1),wx.RIGHT)
    self.entryPhi = wx.TextCtrl(self.parent,-1,value=u"0")
    self.parent.sizer.Add(self.entryPhi,(3,2),(1,1),wx.EXPAND)

  def processInput(self):
    " update amp, w and phi, and display"
    print "Will shape with the cosine function. You entered: "
    try : 
      self.amp = float(self.entryAmp.GetValue())
      self.w   = float(self.entryW.GetValue())
      self.phi = float(self.entryPhi.GetValue())
    except ValueError :
      dialog = wx.MessageDialog(self.parent,"One of the entries is incorrect.",'Error!',wx.OK|wx.ICON_ERROR)
      dialog.ShowModal()
      print "One of the entries is not a number!"

      print self.entryAmp.GetValue()
      print self.entryW.GetValue()
      print self.entryPhi.GetValue()
      #TODO : create an error dialog
    
    print "parameters will be: "
    print "  A : %f" % self.amp
    print "  w : %f" % self.w
    print "  phi:%f" % self.phi




class SinFunction(PhaseFunction):
  def __str__(self):
    return "Cosine!"

  
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
    print "Will shape with the sine function. You entered: "
    try : 
      self.amp = float(self.entryAmp.GetValue())
      self.w   = float(self.entryW.GetValue())
      self.phi = float(self.entryPhi.GetValue())
    except ValueError :
      print "One of the entries is not a number!"

      print self.entryAmp.GetValue()
      print self.entryW.GetValue()
      print self.entryPhi.GetValue()
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

