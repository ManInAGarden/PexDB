from datetime import datetime
from typing import Any

from wx.core import wxdate2pydate
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
            unitstr = None):
        
        self._fieldname = fieldname
        self._fieldcls = fieldcls
        self._idfieldname = idfieldname
        self._fetchexpr = fetchexpr
        self._choicedta = None
        self._unitstr = unitstr
        
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
        elif self.pgitemtype is pg.StringProperty:
            pitem = pg.StringProperty(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.DateProperty:
            pitem = pg.DateProperty(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.PropertyCategory:
            pitem = pg.PropertyCategory(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.BoolProperty:
            pitem = pg.BoolProperty(self.pgitemlabel, self.pgitemname)
            pitem.SetAttribute("UseCheckbox", 1)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.EnumProperty:
            pitem = pg.EnumProperty(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        elif self.pgitemtype is pg.PropertyCategory:
            pitem = pg.PropertyCategory(self.pgitemlabel, self.pgitemname)
            pitem.SetAutoUnspecified()
        else:
            raise Exception("unknow property item type <{0}>".format(str(self.pgitemtype)))

        return pitem

    def setvalue(self, propgrid,  val):
        pitm = propgrid.GetProperty(self.pgitemname)
        if self.pgitemtype is pg.EnumProperty and val is not None:
            sval = str(val)
        else:
            sval = val

        pitm.SetValue(sval)

    def getasbool(self, obj):
        if obj is None:
            return None

        return obj==1

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
            val = self.getasbool(pitm.GetValue())
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

    


class WxGuiMapper(object):
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

    def createprops(self, propgrid):
        for key, guiinf in self._mapping.items():
            pgi = guiinf.create_prop_item()

            if guiinf.pgitemtype is pg.EnumProperty and guiinf.fetchexpr is not None and guiinf.fieldcls is not None:
                q = sqp.SQQuery(self._fact, guiinf.fieldcls).where(guiinf.fetchexpr)
                guiinf._choicedta = []
                dispchoices = []
                for obj in q:
                    guiinf._choicedta.append(obj)
                    dispchoices.append(str(obj))

                pgi.SetChoices(pg.PGChoices(dispchoices))
            try: #try to delete existing property
                self.propgrid.DeleteProperty(guiinf.pgitemname)
            except Exception:
                pass
                    
            propgrid.Append(pgi)

class WxGuiMapperExperiment(WxGuiMapper):
    """definition for the GUI of the experiment data editor"""
    def __init__(self, fact : sqp.SQFactory, parentpropgrid):
        super().__init__(fact)
        self.add(WxGuiMapperInfo(fieldname="carriedoutdt", pgitemlabel="Ausführungsdatum", pgitemtype=pg.DateProperty))
        self.add(WxGuiMapperInfo(fieldname="description", pgitemlabel="Beschreibung"))
        self.add(WxGuiMapperInfo(fieldname="printerused", pgitemtype=pg.EnumProperty, fieldcls=Printer, idfieldname="printerusedid", pgitemlabel="Drucker", fetchexpr=Printer.IsActive==True))
        self.add(WxGuiMapperInfo(fieldname="extruderused", pgitemtype=pg.EnumProperty, fieldcls=Extruder, idfieldname="extruderusedid",pgitemlabel="Extruder", fetchexpr=Extruder.IsActive==True))
        self.add(WxGuiMapperInfo(fieldname="factors_category", pgitemtype=pg.PropertyCategory, pgitemlabel="Faktoren"))

        fdef_q = sqp.SQQuery(fact, FactorDefinition).where(FactorDefinition.IsActive==True).select(lambda para : (para.name, para.disptype, para.unit))

        for para in fdef_q:
            if para[2] is not None:
                un = para[2].abbreviation
            else:
                un = None
            if para[1] == "FLOAT":
                self.add(WxGuiMapperInfo(fieldname=para[0], pgitemtype=pg.FloatProperty, unitstr=un))
            elif para[1] == "BOOLEAN":
                self.add(WxGuiMapperInfo(fieldname=para[0], pgitemtype=pg.BoolProperty, unitstr=un))

        self.add(WxGuiMapperInfo(fieldname="results_category", pgitemtype=pg.PropertyCategory, pgitemlabel="Ergebnisse"))

        self.createprops(parentpropgrid)

    def object2gui(self, obj, propgrid):
        """expect obj to be key,value dict and set the values of the property grid items accordingly"""
        for key, value in obj.items():
            guidecl = self[key] #we are a dict too knwoing all the definitions for the propgriditems
            guidecl.setvalue(propgrid, value)

    def gui2object(self, propgrid) -> dict:
        """return the data from the property grid as key, value pairs where the key is the
        known fieldname and the values have been changed to their original types"""
        answ = {}

        for key, itemdecl in self._mapping.items():
            answ[key] = itemdecl.getvalue(propgrid)
            if itemdecl.fieldcls is not None and issubclass(itemdecl.fieldcls, PBase):
                if answ[key] is not None:
                    answ[itemdecl.idfieldname] = answ[key]._id
                else:
                    answ[itemdecl.idfieldname] = None

        return answ

