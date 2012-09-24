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


class Plotter(wx.Panel):
  " Simple plotter class"
  def __init__(self,parent):
    self.parent = parent
    wx.Panel.__init__(self,parent,-1,size=(50,50))
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.figure = matplotlib.figure.Figure()
    self.axPhase = self.figure.add_subplot(211)
    self.axPhase.hold(False)
    self.axU = self.figure.add_subplot(212)
    self.axU.hold(False)
    self.figure.subplots_adjust(hspace=0.5)
    self.canvas = FigureCanvas(self,-1,self.figure)
    self.sizer.Add(self.canvas)
    self.navtoolbar = NavigationToolbar2Wx(self.canvas)
    self.sizer.Add(self.navtoolbar)
    self.SetSizer(self.sizer)
    self.Fit()

  def plotPhaseFunction(self,phasefunction):
    " Plot the phase function, requires a pure function "
    # create x-axis
    wavelength = np.linspace(600,900,1000)
    vFun = np.vectorize(phasefunction)
    phases = vFun(wavelength)
    #print np.array([wavelength,phases]).transpose()
    self.axPhase.plot(wavelength,phases)
    self.axPhase.set_xlabel("Wavelength [nm]")
    self.axPhase.set_ylabel("Phase [rad]")
    self.canvas.draw()

  def plotVoltages(self,phasefunction):
    " Plot the voltages as a function of pixel index "
    # create x-axis
    x = np.arange(640)
    # get the data: do apply_phase with simulateOnly=True
    print "   PATTERN"
    pattern = self.parent.slmCal.apply_phase_on_freq(phasefunction,simulateOnly=True)
    self.axU.plot(x,pattern,'-x')
    self.axU.set_xlabel("Pixel index #")
    self.axU.set_ylabel("Voltage")
    self.canvas.draw()



class slmGui(wx.Frame):
  def __init__(self,parent,id=-1,title='SLM control'):
    self.figureRoot = wx.Frame.__init__(self,parent,id,title)
    self.parent = parent
    self.slmCal = slmCalibrated.slmCalibrated(port='/dev/ttyS0')
    self.initialize()

  def initialize(self):


    # add sizer
    self.sizer = wx.GridBagSizer()

#    # add a log window
#    self.logwindow = wx.LogTextCtrl(self)
#    self.sizer.Add(self.logwindow,(5,5),(2,2))
#
    # add buttons:
    self.applyButton = wx.Button(self,-1,label="Apply")
    self.sizer.Add(self.applyButton,(4,5))
    self.Bind(wx.EVT_BUTTON,self.ProcessInputAndWritePhase,self.applyButton)
    # preview button
    self.previewButton = wx.Button(self,-1,label="Preview!")
    self.sizer.Add(self.previewButton,(4,6))
    self.Bind(wx.EVT_BUTTON,self.CreatePreview,self.previewButton)

    # clear button
    self.clearButton = wx.Button(self,-1,label="Clear shaper")
    self.sizer.Add(self.clearButton,(4,7))
    self.Bind(wx.EVT_BUTTON,self.ClearShaper,self.clearButton)

    # add notebook
    self.nb = wx.Notebook(self,-1)
    self.nb.sizer = wx.GridBagSizer()
    
    self.cosine = FunctionObjectWrapper(self.nb,CosFunction)
    self.vshape = FunctionObjectWrapper(self.nb,Vshape)

    self.nb.AddPage(self.cosine,"Cosine")
    self.nb.AddPage(self.vshape,"V-shape")
    
    
    self.activeObject = self.cosine.phasefun
    
    self.sizer.Add(self.nb,(1,5),(2,4),wx.EXPAND)

    # add plot
    self.graphs = Plotter(self)
    self.sizer.Add(self.graphs,(1,1),(4,4),wx.EXPAND)

    self.sizer.AddGrowableCol(0)
    
    self.SetSizerAndFit(self.sizer)
    self.Show(True)
#
  def ClearShaper(self,event):
    """ Clear the shaper """
    print "Clearing shaper"
    self.slmCal.slm.clear()

  def CreatePreview(self,event):
    "create a preview in the graphs"
     # get page
    print self.nb.GetCurrentPage() # returns the current tab number
    self.activeObject = self.nb.GetCurrentPage().phasefun
    self.activeObject.processInput()
    # update graph
    self.updateGraph()   

  def ProcessInputAndWritePhase(self,event):
    """Process the input and write the phase. While the phase is being written,
    the button will be red"""

    # get page
    print self.nb.GetCurrentPage() # returns the current tab number
    self.activeObject = self.nb.GetCurrentPage().phasefun
    self.activeObject.processInput()
    # update graph
    self.updateGraph()
    self.writePhase()
#  
  def updateGraph(self):
    self.graphs.plotPhaseFunction(self.activeObject.returnFunction())
    # now get the graph, so that you can first check and then apply

    self.graphs.plotVoltages(self.activeObject.returnFunction())

#
  def writePhase(self):
    self.slmCal.apply_phase(self.activeObject.returnFunction())
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
    text = wx.StaticText(self.parent,-1,label=self.__str__())
    self.parent.sizer.Add(text,(0,0),(2,2))

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
    w0 = self.w0
    steepness = self.steepness
    offset = self.offset

    return lambda w: abs(w - w0)*steepness+offset

  def initialize(self):
    print "Initializing VShape"
    self.w0 = 780
    self.steepness = 0.1
    self.offset = 0

    self.entryOffset = self.createGuiInputBox('Offset [2 \pi rad]',1,1)
    self.entryW0     = self.createGuiInputBox('center wl [nm]',1,2,780)
    self.entrySteepness = self.createGuiInputBox('t [fs]',1,3,0.1)

  def processInput(self):
    try : 
      self.w0 = float(self.entryW0.GetValue())
      self.steepness = 2*np.pi*float(self.entrySteepness.GetValue())
      self.offset = float(self.entryOffset.GetValue())
    except ValueError:
      self.ShowError("One of the entries is incorrect")



class CosFunction(PhaseFunction):
  def __str__(self):
    return "Cosine: offset+amp*cos((w-w0)*t+phi)"

  def returnFunction(self):
    offset = self.offset
    amp = self.amp
    w0 = self.w0
    phi = self.phi
    t = self.t
    return lambda w: offset + amp*cos((w-w0)*t+phi)

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
    self.entryOffset = self.createGuiInputBox('offset',1,1)
    self.entryAmp = self.createGuiInputBox('Amp [rad]',1,2,0)
    self.entryW0   = self.createGuiInputBox('w0 ',1,3,0)
    self.entryPhi = self.createGuiInputBox('phi',1,4,0)
    self.entryT   = self.createGuiInputBox('t [fs]',1,5,0)

  def processInput(self):
    " update amp, w and phi, and display"
    print "Will shape with the cosine function. You entered: "
    try : 
      self.amp = float(self.entryAmp.GetValue())
      self.w0   = float(self.entryW0.GetValue())
      self.phi = float(self.entryPhi.GetValue())
      self.offset = float(self.entryOffset.GetValue())
      self.t   = 2*np.pi*float(self.entryT.GetValue())
    except ValueError :
      self.ShowError("One of the entries is incorrect")
      print "One of the entries is not a number!"
    
    print "parameters will be: "
    print "  A : %f" % self.amp
    print "  w : %f" % self.w0
    print "  phi:%f" % self.phi



if __name__ == '__main__':
  app = wx.App()
  frame = slmGui(None,-1,'testing title')
  app.MainLoop()

