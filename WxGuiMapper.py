from datetime import datetime

import wx

import sqlitepersist as sqp
from PersistClasses import *
import wx.propgrid as pg

from sqlitepersist.SQLitePersistBasicClasses import PBase

class WxGuiMapperInfo(object):
    def __init__(self, 
            fieldname : str, 
            fieldcls = None, 
            idfieldname = None, 
            pgitemlabel = None, 
            pgitemname = None, 
            pgitemtype = None,
            fetchexpr = None,
            unitstr = None,
            staticchoices = None,
            enabled=True):
        
        self._fieldname = fieldname
        self._fieldcls = fieldcls
        self._idfieldname = idfieldname
        self._fetchexpr = fetchexpr
        self._choicedta = None
        self._unitstr = unitstr
        self._staticchoices = staticchoices
        self._enabled = enabled
        
        if pgitemname is None:
            self._pgitemname = fieldname
        else:
            self._pgitemname = pgitemname

        if pgitemtype is None:
            self._pgitemtype = pg.StringProperty
        else:
            self._pgitemtype = pgitemtype

        if pgitemlabel is None:
            self._pgitemlabel = self._pgitemname
        else:
            self._pgitemlabel = pgitemlabel

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
            #pitem.SetAttribute(pg.PG_DATE_FORMAT, "%d.%m.%Y %H:%M:%S")
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
        else:
            raise Exception("unknow property item type <{0}>".format(str(self.pgitemtype)))

        pitem.Enable(self._enabled)

        return pitem

    def setvalue(self, propgrid,  val):
        pitm = propgrid.GetProperty(self.pgitemname)
        if self.pgitemtype is pg.EnumProperty and val is not None:
            sval = str(val)
        else:
            sval = val

        pitm.SetValue(sval)

    # def getasbool(self, obj):
    #     if obj is None:
    #         return None

    #     return obj==1

    def getasdatetime(self, wxdt):
        if wxdt is None:
            return None
        
        return datetime(wxdt.year, wxdt.month, wxdt.day, wxdt.hour, wxdt.minute, wxdt.second, wxdt.millisecond)

    def getfromenum(self, idx : int):
        if idx is None or idx<0:
            return None
        
        if self._choicedta is None:
            return None

        return self._choicedta[idx]

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
        elif self.pgitemtype is pg.PropertyCategory:
            return None
        else:
            raise Exception("unhandled property item type <{0}>".format(self.pgitemtype))

        return val

    def set_emty(self, pgrd : pg.PropertyGrid):
        pgrd.SetPropertyValue(self.pgitemname, None)
    

    @property
    def fieldname(self):
        return self._fieldname

    @fieldname.setter
    def fieldname(self, value):
        assert(value is not None)
        self._fieldname = value

    @property
    def fieldcls(self):
        return self._fieldcls

    @fieldcls.setter
    def fieldcls(self, value):
        self._fieldcls = value

    @property
    def idfieldname(self):
        return self._idfieldname

    @idfieldname.setter
    def idfieldname(self, value):
        self._idfieldname = value

    @property
    def pgitemtype(self):
        return self._pgitemtype

    @pgitemtype.setter
    def pgitemtype(self, value):
        assert(value is not None)
        self._pgitemtype = value

    @property
    def pgitemname(self):
        return self._pgitemname

    @pgitemname.setter
    def pgitemname(self, value):
        self._pgitemname = value

    @property
    def pgitemlabel(self):
        return self._pgitemlabel

    @pgitemlabel.setter
    def pgitemname(self, value):
        self._pgitemlabel = value

    @property
    def fetchexpr(self):
        return self._fetchexpr

    @fetchexpr.setter
    def fetchexpr(self, value):
        self._fetchexpr = value

    @property
    def unitstr(self):
        return self._unitstr

    @unitstr.setter
    def unitstr(self, value):
        self._unitstr = value

    @property
    def staticchoices(self):
        return self._staticchoices

    @staticchoices.setter
    def staticchoices(self, value):
        self._staticchoices = value

    
class WxGuiMapper(object):
    """inherit from this with your own class to create your GUI based on property grids"""
    def __init__(self, fact):
        self._mapping = {}
        self._fact = fact

    def __iter__(self):
        return self._mapping.__iter__()

    def __next__(self):
        return self._mapping.__next()

    def __getitem__(self, name):
         return self._mapping[name]

    def __setitem__(self, name, value):
        self._mapping[name] = value

    def add(self, mapping : WxGuiMapperInfo):
        self._mapping[mapping.fieldname] = mapping

    def gui2object(self, propgrid) -> dict:
        raise Exception("ovveride me!")

    def object2gui(self, obj : dict, propgrid) -> None:
        raise Exception("ovveride me!")

		
    def emptyallitems(self, pgrd):
        """emties all the properties to symbolise that no data are in the propgrid"""
        for key, guuinf in self._mapping.items():
            guuinf.set_emty(pgrd)

    def createprops(self, propgrid : pg.PropertyGrid):

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
            
            try: #try to delete existing property
                propgrid.DeleteProperty(guiinf.pgitemname)
            except Exception:
                pass
                    
            propgrid.Append(pgi)



