#!/usr/bin/python
import os
import numpy
import numpy as np
from numpy import cos,linspace
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
from PhaseFunctions import *


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
        #phasefunction is dependent on frequency, not wavelength, so convert
        vFun = np.vectorize(phasefunction)
        phases = vFun(w2f(wavelength))
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
        print "     PATTERN"
        pattern = self.parent.slmCal.apply_phase_on_freq(phasefunction,simulateOnly=True)
        self.axU.plot(x,pattern,'-x')
        self.axU.set_xlabel("Pixel index #")
        self.axU.set_ylabel("Voltage")
        self.canvas.draw()



class slmGui(wx.Frame):
    def __init__(self,parent,id=-1,title='SLM control'):
        self.figureRoot = wx.Frame.__init__(self,parent,id,title)
        self.parent = parent

        if os.name == 'nt':
	        self.slmCal = slmCalibrated.slmCalibrated(port=0)
	        print "Assuming windows"
        else :
	        self.slmCal = slmCalibrated.slmCalibrated(port='/dev/ttyS0')
	        print "Assuming linux"
        self.initialize()

    def initialize(self):


        # add sizer
        self.sizer = wx.GridBagSizer()

#        # add a log window
#        self.logwindow = wx.LogTextCtrl(self)
#        self.sizer.Add(self.logwindow,(5,5),(2,2))
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
        self.sizer.Add(self.clearButton,(5,5))
        self.Bind(wx.EVT_BUTTON,self.ClearShaper,self.clearButton)

        # set to zero
        self.zeroButton = wx.Button(self,-1,label="Initialize to 0")
        self.sizer.Add(self.zeroButton,(5,6))
        self.Bind(wx.EVT_BUTTON,self.ZeroShaper,self.zeroButton)

        # add notebook
        self.nb = wx.Notebook(self,-1)
        self.nb.sizer = wx.GridBagSizer()
        
        self.cosine = FunctionObjectWrapper(self.nb,CosFunction)
        self.vshape = FunctionObjectWrapper(self.nb,Vshape)
        self.calibrationfunction = FunctionObjectWrapper(self.nb,CalibrationFunction)

        self.nb.AddPage(self.cosine,"Cosine")
        self.nb.AddPage(self.vshape,"V-shape")
        self.nb.AddPage(self.calibrationfunction,"Calibration")
        
        
        self.activeObject = self.cosine.phasefun
        
        self.sizer.Add(self.nb,(1,5),(2,4),wx.EXPAND)

        # add plot
        self.graphs = Plotter(self)
        self.sizer.Add(self.graphs,(1,1),(5,4),wx.EXPAND)

        self.sizer.AddGrowableCol(0)
        
        self.SetSizerAndFit(self.sizer)
        self.Show(True)
#
    def ClearShaper(self,event):
        """ Clear the shaper """
        print "Clearing shaper"
        self.slmCal.slm.clear()
        print "Shaper cleared"

    def ZeroShaper(self,event):
        print "Initializing to 0 "
        self.slmCal.apply_phase(lambda l:0)

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
        """Write the active phase to the shaper """
        self.slmCal.apply_phase_on_freq(self.activeObject.returnFunction())
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
        

if __name__ == '__main__':
    import traceback
    import sys
    # This try-catch statement is done to ensure that you can read the exceptions in windows, before the shell is killed
    try :
      app = wx.App()
      frame = slmGui(None,-1,'SLM gui')
      app.MainLoop()
    except Exception as e:
        print "Exception occurred. "
        print e.args
        traceback.print_exc(file=sys.stdout)

        discard = raw_input("Press any key to continue.")
        raise

