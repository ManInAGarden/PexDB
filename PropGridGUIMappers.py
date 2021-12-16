import wx.propgrid as pg

from WxGuiMapper import *

class WxGuiMapperExperiment(WxGuiMapper):
    """definition for the GUI of the experiment data editor
    some proprty items are declared statically but all the factors and results
    are added dynamically by what is found in the currenty active factor definitions and 
    result definitions"""
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


class WxGuiMapperFactorDefintion(WxGuiMapper):
    """definition for the GUI of the factor defintions data editor
    """
    def __init__(self, fact : sqp.SQFactory, parentpropgrid):
        super().__init__(fact)
        self.add(WxGuiMapperInfo(fieldname="abbreviation", pgitemlabel="Abbreviation", pgitemtype=pg.StringProperty))
        self.add(WxGuiMapperInfo(fieldname="name", pgitemlabel="Name", pgitemtype=pg.StringProperty))
        self.add(WxGuiMapperInfo(fieldname="unit", pgitemtype=pg.EnumProperty, fieldcls=Unit, idfieldname="unitid", pgitemlabel="Unit"))
        self.add(WxGuiMapperInfo(fieldname="disptype", pgitemtype=pg.EnumProperty, pgitemlabel="Display type", staticchoices=["FLOAT", "BOOLEAN"]))
        self.add(WxGuiMapperInfo(fieldname="isactive", pgitemtype=pg.BoolProperty, pgitemlabel="Is active"))
        self.add(WxGuiMapperInfo(fieldname="curaname", pgitemtype=pg.EnumProperty, fieldcls=CuraNameCat, pgitemlabel="Cura name"))

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