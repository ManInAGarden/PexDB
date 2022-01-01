from datetime import date, datetime
from time import strftime

import wx
import wx.adv as wxadv
import sqlitepersist as sqp
from PersistClasses import *
import wx.propgrid as pg

from sqlitepersist.SQLitePersistBasicClasses import PBase

class TimeProperty(pg.PGProperty):
    def __init__(self, label=pg.PG_LABEL, name=pg.PG_LABEL):
        pg.PGProperty.__init__(self, label, name)
        self.my_value = None

    def DoGetEditorClass(self):
        """
        Determines what editor should be used for this property type. This
        is one way to specify one of the stock editors.
        """
        return pg.PropertyGridInterface.GetEditorByName("TextCtrl")

    def ValueToString(self, value, flags):
        """
        Convert the given property value to a string.
        """
        return str(value)

    def StringToValue(self, st, flags):
        """
        Convert a string to the correct type for the property.

        If failed, return False or (False, None). If success, return tuple
        (True, newValue).
        """
        try:
            val = datetime.strptime(st, "%H:%M:%S").time()
            return (True, val)
        except (ValueError, TypeError):
            pass
        except:
            raise
        return (False, None)


class WxGuiMapperInfo(object):
    """ Class to store the info for a single property field's data to property-grid information"""
    def __init__(self, 
            fname : str, 
            fcls : sqp.PBase = None, 
            idfldname : str  = None, 
            pgilabel : str = None, 
            pginame : str = None, 
            pgitype : pg.PGProperty = None,
            fexpr  = None,
            unit : str = None,
            schoices : list = None,
            vali : wx.Validator = None,
            isenabled : bool=True):
        """Create a new instance of a WXGuiMapperInfo
            fname : Name of the field in the data
            fcls  : for enum fields based in database data, the persistence class for the choices
            idfldname : name of the id-field (in the current object) to get the current choice
            pgilabel : Caption fir the property
            pginame : Name to be given to the property-item
            pgitype : Type of Property item.
            fexpr : fetching expression
            unit : Unit to be displayed with the caption (is appended to end of the caption text)
            schoices : for enum properties - the list of choices
            validator : a validator in case of user defined validation
            isenabled : Sets the enabled-state of the property item
        """
        assert fname is not None, "fname must not be None!"

        self._oldvalue = None #for change detection

        self._fieldname = fname
        self._fieldcls = fcls
        self._idfieldname = idfldname
        self._fetchexpr = fexpr
        self._choicedta = None
        self._unitstr = unit
        self._staticchoices = schoices
        self._enabled = isenabled
        self._validator = vali
        
        if pginame is None:
            self._pgitemname = fname
        else:
            self._pgitemname = pginame

        if pgitype is None:
            self._pgitemtype = pg.StringProperty
        else:
            self._pgitemtype = pgitype

        if pgilabel is None:
            #self._pgitemlabel = self._pgitemname does NOT work, confuses name, fieldname, and label mysteriously!!!!
            if pginame is not None:
                self._pgitemlabel = pginame
            else:
                self._pgitemlabel = fname
        else:
            self._pgitemlabel = pgilabel

    def create_prop_item(self):
        if self.pgitemtype is pg.FloatProperty:
            if not self.unitstr is None:
                label = "{0} [{1}]".format(self.pgitemlabel, self.unitstr)
            else:
                label = self.pgitemlabel

            pitem = pg.FloatProperty(label, self.pgitemname)
            pitem.SetAttribute("Precision", 3)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.IntProperty:
            if not self.unitstr is None:
                label = "{0} [{1}]".format(self.pgitemlabel, self.unitstr)
            else:
                label = self.pgitemlabel

            pitem = pg.IntProperty(label, self.pgitemname)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.StringProperty:
            pitem = pg.StringProperty(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.DateProperty:
            pitem = pg.DateProperty(self.pgitemlabel, self.pgitemname)
            #pitem.SetAttribute(pg.PG_DATE_PICKER_STYLE, wxadv.DP_ALLOWNONE)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.PropertyCategory:
            pitem = pg.PropertyCategory(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.BoolProperty:
            pitem = pg.BoolProperty(self.pgitemlabel, self.pgitemname)
            pitem.SetAttribute("UseCheckbox", 1)
            #pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.EnumProperty:
            pitem = pg.EnumProperty(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.PropertyCategory:
            pitem = pg.PropertyCategory(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is TimeProperty:
            pitem = TimeProperty(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        else:
            raise Exception("unknow property item type <{0}>".format(str(self.pgitemtype)))

        pitem.Enable(self._enabled)
        if self.validator is not None:
            pitem.SetValidator(self.validator)
            

        return pitem

    def setvalue(self, propgrid,  val):
        self._oldvalue = val
        pitm = propgrid.GetProperty(self.pgitemname)
        if self.pgitemtype is pg.EnumProperty and val is not None:
            sval = str(val)
        elif self.pgitemtype is pg.DateProperty and val is not None:
            #vals = str(val)
            #sval = pitm.StringToValue(vals)
            sval = val
        else:
            sval = val

        pitm.SetValue(sval)
        pitm.SetModifiedStatus(False)

    def getmonthnum(self, wxdt : wx.DateTime) -> int:
        monthes = {
            wx.DateTime.Jan : 1,
            wx.DateTime.Feb : 2,
            wx.DateTime.Mar : 3,
            wx.DateTime.Apr : 4,
            wx.DateTime.May : 5,
            wx.DateTime.Jun : 6,
            wx.DateTime.Jul : 7,
            wx.DateTime.Aug : 8,
            wx.DateTime.Sep : 9,
            wx.DateTime.Oct : 10,
            wx.DateTime.Nov : 11,
            wx.DateTime.Dec : 12
            }
        
        return monthes[wxdt.month]

    def getasdatetime(self, wxdt):
        if wxdt is None:
            return None
        
        return datetime(wxdt.year, self.getmonthnum(wxdt), wxdt.day, wxdt.hour, wxdt.minute, wxdt.second, wxdt.millisecond)

    def getfromenum(self, idx : int):
        if idx is None or idx<0:
            return None
        
        if self._choicedta is None:
            return None

        return self._choicedta[idx]

    def has_changed(self, propgrid : pg.PropertyGrid):
        pitm = propgrid.GetProperty(self.pgitemname)
        
        answ = self._oldvalue != pitm.GetValue()
        return answ


    def getvalue(self, propgrid):
        pitm = propgrid.GetProperty(self.pgitemname)
        if self.pgitemtype is pg.StringProperty:
            val = pitm.GetValueAsString()
        elif self.pgitemtype is pg.BoolProperty:
            val = pitm.GetValue()
        elif self.pgitemtype is pg.DateProperty:
            val = self.getasdatetime(pitm.GetValue())
        elif self.pgitemtype is pg.FloatProperty:
            val = pitm.GetValue()
        elif self.pgitemtype is pg.EnumProperty:
            val = self.getfromenum(pitm.GetChoiceSelection())
        elif self.pgitemtype is pg.IntProperty:
            val = pitm.GetValue()
        elif self.pgitemtype is TimeProperty:
            val = pitm.GetValue()
        elif self.pgitemtype is pg.PropertyCategory:
            return None
        else:
            raise Exception("unhandled property item type <{0}>".format(self.pgitemtype))

        return val

    def set_empty(self, pgrd : pg.PropertyGrid):
        pgrd.SetPropertyValue(self.pgitemname, None)
    

    @property
    def fieldname(self):
        return self._fieldname

    @property
    def fieldcls(self):
        return self._fieldcls

    @property
    def idfieldname(self):
        return self._idfieldname

    @property
    def pgitemtype(self):
        return self._pgitemtype

    @property
    def pgitemname(self):
        return self._pgitemname

    @property
    def pgitemlabel(self):
        return self._pgitemlabel

    @property
    def fetchexpr(self):
        return self._fetchexpr

    @property
    def unitstr(self):
        return self._unitstr

    @property
    def staticchoices(self):
        return self._staticchoices

    @property
    def validator(self):
        return self._validator
    
class WxGuiMapper(object):
    """inherit from this with your own class to create your GUI based on property grids"""
    def __init__(self, fact, propertygrid : pg.PropertyGrid):
        self._mapping = {}
        self._fact = fact
        self._parentpropgrid = propertygrid

    def __iter__(self):
        return self._mapping.__iter__()

    def __next__(self):
        return self._mapping.__next()

    def __getitem__(self, name):
         return self._mapping[name]

    def __setitem__(self, name, value):
        self._mapping[name] = value

    @property
    def parentpropgrid(self):
        return self._parentpropgrid

    def add(self, mapping : WxGuiMapperInfo):
        self._mapping[mapping.fieldname] = mapping

    def gui2object(self) -> dict:
        raise Exception("ovveride me!")

    def object2gui(self, obj : dict) -> None:
        raise Exception("ovveride me!")

		
    def emptyallitems(self):
        """emties all the properties to symbolise that no data are in the propgrid"""
        for key, guuinf in self._mapping.items():
            guuinf.set_empty(self._parentpropgrid)

    def deleteallprops(self):
        self._parentpropgrid.Clear()

    def createallprops(self):
        """creates all the property items as defined"""
        self.deleteallprops()

        for key, guiinf in self._mapping.items():
            pgi = guiinf.create_prop_item()

            if guiinf.pgitemtype is pg.EnumProperty and guiinf.fieldcls is not None:
                if guiinf.fetchexpr is not None:
                    q = sqp.SQQuery(self._fact, guiinf.fieldcls).where(guiinf.fetchexpr)
                else:
                    q = sqp.SQQuery(self._fact, guiinf.fieldcls).where()

                guiinf._choicedta = []
                dispchoices = []
                for obj in q:
                    guiinf._choicedta.append(obj)
                    dispchoices.append(str(obj))

                pgi.SetChoices(pg.PGChoices(dispchoices))
            elif guiinf.pgitemtype is pg.EnumProperty and guiinf.staticchoices is not None and len(guiinf.staticchoices)>0:
                pgi.SetChoices(pg.PGChoices(guiinf.staticchoices))
                guiinf._choicedta = guiinf.staticchoices
            
            self._parentpropgrid.Append(pgi)
            self._parentpropgrid.Refresh()

    def has_changed(self):
        for ky, value in self._mapping.items():
            if  value.has_changed(self._parentpropgrid):
                return True
        
        return False
            



