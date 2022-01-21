from email.message import Message
import locale
import wx

from Evaluator import Evaluator

class FloatValidator(wx.Validator):
    ''' validates that  '''

    #----------------------------------------------------------------------
    def __init__(self, minmax : tuple):
        wx.Validator.__init__(self)
        self.minmax = minmax
        self.Bind(wx.EVT_CHAR, self.OnChar)

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


class MergeFormulaValidator(wx.Validator):
    ''' validates that a merge formula even hast the chance to work properly  '''

    #----------------------------------------------------------------------
    def __init__(self, globals : dict):
        wx.Validator.__init__(self)
        self.globals = globals
        self.Bind(wx.EVT_CHAR, self.OnChar)


    #----------------------------------------------------------------------
    def Clone(self):
        '''Required Validator method'''
        return MergeFormulaValidator(self.globals)

    #----------------------------------------------------------------------
    def Validate(self, parentwin):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if text is None or len(text) == 0:
            return True

        return self.is_formulaok(text)

    def is_formulaok(self, formula):
        """check the formula with a lambda"""

        try:
            evalu = Evaluator()
            erg = evalu.eval_formula(formula, self.globals)
            terg = type(erg)
            if not terg is float:
                wx.MessageBox("Result will not be float but of type {}. Check usage of commas instead of decimal dots.".format(str(terg)))
                answ = False
            else:
                answ = True
        except Exception as sexc:
            wx.MessageBox("Syntax error in formula - {}".format(str(sexc)))
            answ = False

        return answ
    #----------------------------------------------------------------------
    def TransferToWindow(self):
        return True

    #----------------------------------------------------------------------
    def TransferFromWindow(self):
        return True

    #----------------------------------------------------------------------
    def OnChar(self, event):
        keycode = int(event.GetKeyCode())
        key = chr(keycode)

        if keycode>=314 and keycode<=317:
            event.Skip()

        if keycode >= 256:
            return

        if keycode == 127 or keycode==8: #del and backspace
            event.Skip()

        if key.isalnum():
            event.Skip()

        if key in ",.*+-()/ _":
            event.Skip()

        return