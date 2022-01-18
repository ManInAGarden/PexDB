from email.message import Message
import locale
import wx

class FloatValidator(wx.Validator):
    ''' validates that  '''

    #----------------------------------------------------------------------
    def __init__(self, minmax : tuple):
        wx.Validator.__init__(self)
        self.minmax = minmax
        #self.Bind(wx.EVT_CHAR, self.OnChar)

    #----------------------------------------------------------------------
    def Clone(self):
        '''Required Validator method'''
        return FloatValidator(self.minmax)

    #----------------------------------------------------------------------
    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if len(text) == 0:
            return True 
        else:
            try:
                flo = locale.atof(text)
                if self.minmax is None:
                    textCtrl.SetBackgroundColour(
                        wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
                    textCtrl.Refresh()
                    return True

                if flo >= self.minmax[0] and flo <= self.minmax[1]:
                    textCtrl.SetBackgroundColour(
                        wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
                    textCtrl.Refresh()
                    return True
                else:
                    wx.MessageBox("Input value is out of bounds")
                    textCtrl.SetBackgroundColour("pink")
                    textCtrl.SetFocus()
                    textCtrl.Refresh()
                    return False
            except ValueError as exc:
                textCtrl.SetBackgroundColour("pink")
                textCtrl.SetFocus()
                textCtrl.Refresh()
                wx.MessageBox("Cannot convert your inpupt to a valid float number")
                return False


            

            
            
        if self.minmax is None:
            return True
        else:
            return True

    #----------------------------------------------------------------------
    def TransferToWindow(self):
        return True

    #----------------------------------------------------------------------
    def TransferFromWindow(self):
        return True

    #----------------------------------------------------------------------
    def OnChar(self, event):
        keycode = int(event.GetKeyCode())
        if keycode < 256:
            #print keycode
            key = chr(keycode)
            if key in "0123456789":
                event.Skip()
            if key=="E" or keycode == "e":
                event.Skip()
            if key==",":
                event.Skip()

        return