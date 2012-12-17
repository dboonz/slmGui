import numpy
import numpy as np
from numpy import sin,cos,linspace
try :
  import wx
  from wx import Button
except ImportError :
  raise ImportError, "The wxPython module is required to run this program"

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas

from matplotlib.backends.backend_wx import NavigationToolbar2Wx
import slmCalibrated
from utils import w2f

# all functions should have the same properties:
class PhaseFunction():
  def __init__(self,parent,startRow=1, startCol=1):
    self.parent = parent
    self.initialize()
    text = wx.StaticText(self.parent,-1,label=self.__str__())
    self.parent.sizer.Add(text,(0,0),(2,2))

  def initialize(self):
    """ This function should set all relevant variables and create any graphical
    interface objects """
    print "Not implemented!"

  def returnFunction(self):
    "Return a pure function, dependent on the frequency"
    return lambda f: None
  def processInput(self):
    """"This function should process all the input that was given to graphical
    interface objects. """
    pass

  def createGuiInputBox(self,label,posX,posY,initialvalue=0):
    """ create a gui input box with text left to the box, and return the text
    input widget"""

    boxText = wx.StaticText(self.parent,-1,label=label)
    boxEntry = wx.TextCtrl(self.parent,-1,value=str(initialvalue))
    self.parent.sizer.Add(boxText,(posY,posX))
    self.parent.sizer.Add(boxEntry,(posY,posX+1))
    return boxEntry


  def ShowError(self,message):
    " Displays a popup error message"
    dialog = wx.MessageDialog(self.parent,message,'Error!',wx.OK|wx.ICON_ERROR)
    dialog.ShowModal()

class Vshape(PhaseFunction):
  # create a v-shape
  def __str__(self):
    return "VShape: abs(w-w0)*steepness+offset "

  def returnFunction(self):
    t = self.t
    offset = self.offset

    f0 = w2f(self.w0)
    print "f0 : " , f0 
    return lambda f: abs(f - f0)*t+offset

  def initialize(self):
    print "Initializing VShape"
    self.w0 = 780
    self.t = 0.1
    self.offset = 0

    self.entryOffset = self.createGuiInputBox('Offset [2 \pi rad]',1,1)
    self.entryW0     = self.createGuiInputBox('center wl [nm]',1,2,780)
    self.entryt = self.createGuiInputBox('t [fs]',1,3,0.1)

  def processInput(self):
    try : 
      self.w0 = float(self.entryW0.GetValue())
      self.t = float(self.entryt.GetValue())*1e-15*2*np.pi
      self.offset = float(self.entryOffset.GetValue())
    except ValueError:
      self.ShowError("One of the entries is incorrect")

class CalibrationFunction(PhaseFunction):
  " Function that gives you a spike at a certain wavelength"

  def __str__(self):
    return "Spike function"

  def returnFunction(self):
    # get boundaries for frequency:
    minFreq = w2f(self.centerwl+self.width)
    maxFreq = w2f(self.centerwl-self.width)
    height = self.height
    # create a function to make a spike of width width
    def spike(f):
      if f < minFreq:
        return self.offset
      elif f > maxFreq:
        return self.offset
      else :
        return self.offset+height
    return spike

  def initialize(self):
    self.centerwlEntry = self.createGuiInputBox("center wl [nm]",1,1,780)
    self.offsetEntry = self.createGuiInputBox("Offset [rad]",1,2,0)
    self.widthEntry = self.createGuiInputBox("width [nm]",1,3,1)
    self.heightEntry = self.createGuiInputBox("height [ pi rad]",1,4,1)

  def processInput(self):
    " update values"
    self.centerwl = float(self.centerwlEntry.GetValue())
    self.offset = float(self.offsetEntry.GetValue())
    self.width  = float(self.widthEntry.GetValue())
    self.height = float(self.heightEntry.GetValue())


class CosFunction(PhaseFunction):
  def __str__(self):
    return "Cosine: offset+amp*cos((w-w0)*t+phi)"

  def returnFunction(self):
    offset = self.offset
    amp = self.amp
    f0 = w2f(self.w0)
    phi = self.phi
    t = self.t
    return lambda f: offset + amp*cos((f-f0)*t+phi)

#    return lambda w: self.offset+ self.amp*cos((w-w0)*+self.phi)

  def initialize(self):
    print "Initializing sinFunction"
    # relevant variables:
    self.amp = 1.
    self.w0   = 1.
    self.phi = 1.
    self.offset = 1.
    self.t = 0

    # create entry boxes for the different props:
    self.entryOffset = self.createGuiInputBox('offset [pi rad]',1,1,0)
    self.entryAmp = self.createGuiInputBox('Amp [pi rad]',1,2,2)
    self.entryW0   = self.createGuiInputBox('lambda0 [nm] ',1,3,780)
    self.entryPhi = self.createGuiInputBox('phi [rad]',1,4,0)
    self.entryT   = self.createGuiInputBox('t [fs]',1,5,150)

  def processInput(self):
    " update amp, w and phi, and display"
    print "Will shape with the cosine function. You entered: "
    try : 
      self.amp = float(self.entryAmp.GetValue())
      self.w0   = float(self.entryW0.GetValue())
      self.phi = float(self.entryPhi.GetValue())
      self.offset = float(self.entryOffset.GetValue())
      self.t   = 2*np.pi*float(self.entryT.GetValue())*1e-15
    except ValueError :
      self.ShowError("One of the entries is incorrect")
      print "One of the entries is not a number!"
    
    print "parameters will be: "
    print "  A : %f" % self.amp
    print "  w : %f" % self.w0
    print "  phi:%f" % self.phi



