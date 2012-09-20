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
    sizer = wx.GridBagSizer()

    # add buttons:
    self.applyButton = wx.Button(self,-1,label="Apply")
    sizer.Add(self.applyButton,(0,0))
#    self.Bind(wx.EVT_BUTTON,self.ProcessInputAndWritePhase,self.applyButton)

#    self.cosineObject = CosFunction(self.parent)
#    self.activeObject = self.cosineObject

    sizer.AddGrowableCol(0)
    self.SetSizerAndFit(sizer)
    print "Here!"
    self.Show(True)
#
#

if __name__ == '__main__':
  app = wx.App()
  frame = slmGui(None,-1,'testing title')
  app.MainLoop()
#  gui = slmGui(None)
#  gui.mainloop()

