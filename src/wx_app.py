try :
  import wx
except ImportError :
  raise ImportError , "The wxPython module is required for this program"

class simpleapp_wx(wx.Frame):
  def __init__(self,parent,id,title):
    wx.Frame.__init__(self,parent,id,title)

    self.parent = parent
    self.initialize()

  def initialize(self):
    sizer = wx.GridBagSizer()

    # user code

    " Add a text entry field"
    self.entry = wx.TextCtrl(self,-1,value=u"Enter text")
    sizer.Add(self.entry,(0,0),(1,1),wx.EXPAND)
    # add callback
    self.Bind(wx.EVT_TEXT_ENTER,self.OnButtonClick,self.entry)


    " Add a button"
    button = wx.Button(self,-1,label="Click me !")
    sizer.Add(button,(0,1))
    self.Bind(wx.EVT_BUTTON, self.OnButtonClick,button)

    self.label = wx.StaticText(self,-1,label=u"Hello!")
    self.label.SetBackgroundColour(wx.BLUE)
    self.label.SetForegroundColour(wx.BLUE)
    sizer.Add(self.label,(1,0),(1,2),wx.EXPAND)



    sizer.AddGrowableCol(0)
    self.SetSizerAndFit(sizer)

    self.entry.SetFocus()
    self.entry.SetSelection(-1,-1)
    self.Show(True)

  def OnPressEnter(self,event):
    self.label.SetLabel("You pressed enter!")

  def OnButtonClick(self,event):
    self.label.SetLabel("You licked the button!")



if __name__ == '__main__':
  app = wx.App()
  frame = simpleapp_wx(None,-1,'my app')
  app.MainLoop()


