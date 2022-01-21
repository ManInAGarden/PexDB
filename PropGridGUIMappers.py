import wx.propgrid as pg
from WxGuiMapper import *

class DateValidator(wx.Validator):
    """A validator for dates in strings"""
    def Validate(self, parent):
        print(parent)
    
    def TransferToWindow(self):
        return super().TransferToWindow()

    def TransferFromWindow(self):
        return super().TransferFromWindow()

    def Clone(self):
        return super().Clone()

class WxGuiMapperExperiment(WxGuiMapper):
    """definition for the GUI of the experiment data editor
    some proprty items are declared statically but all the factors and results
    are added dynamically by what is found in the currenty active factor definitions and 
    result definitions"""
    def __init__(self, fact : sqp.SQFactory, parentpropgrid : pg.PropertyGrid, proj : Project):
        super().__init__(fact, parentpropgrid)
        
        #dtv = DateValidator()

        self._project = proj
        self.add(WxGuiMapperInfo(fname="sequence", pgilabel="#", pgitype=pg.IntProperty))
        self.add(WxGuiMapperInfo(fname="repnum", pgilabel="Repetition#", pgitype=pg.IntProperty))
        self.add(WxGuiMapperInfo(fname="carriedout_dt", pgilabel="Date", pgitype=pg.DateProperty))
        self.add(WxGuiMapperInfo(fname="carriedout_ti", pgilabel="Time", pgitype=TimeProperty))
        self.add(WxGuiMapperInfo(fname="description", pgilabel="Description"))
        self.add(WxGuiMapperInfo(fname="printerused", pgitype=pg.EnumProperty,  fcls=Printer, idfldname="printerusedid", pgilabel="Printer", fexpr=Printer.IsActive==True))
        self.add(WxGuiMapperInfo(fname="extruderused", pgitype=pg.EnumProperty, fcls=Extruder, idfldname="extruderusedid",pgilabel="Extruder", fexpr=Extruder.IsActive==True))
        self.add(WxGuiMapperInfo(fname="factors_category", pgitype=pg.PropertyCategory, pgilabel="Factors"))

        fprep_q = sqp.SQQuery(fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==proj._id)
        for fprep in fprep_q:
            fdef = fprep.factordefinition
            if fdef.unit is not None:
                un = fdef.unit.abbreviation
            else:
                un = None
            if fdef.disptype == "FLOAT":
                self.add(WxGuiMapperInfo(fname=fdef.name, pgitype=pg.FloatProperty, unit=un, isenabled=fdef.isactive))
            elif fdef.disptype == "BOOLEAN":
                self.add(WxGuiMapperInfo(fname=fdef.name, pgitype=pg.BoolProperty, unit=un, isenabled=fdef.isactive))

        self.add(WxGuiMapperInfo(fname="responses_category", pgitype=pg.PropertyCategory, pgilabel="Responses"))
        
        rprep_q = sqp.SQQuery(fact, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==proj._id)
        for rprep in rprep_q:
            resd = rprep.responsedefinition
            if resd.unit is not None:
                un = resd.unit.abbreviation
            else:
                un = None
            if resd.disptype == "FLOAT":
                self.add(WxGuiMapperInfo(fname=resd.name, pgitype=pg.FloatProperty, unit=un, isenabled=resd.isactive))
            elif resd.disptype == "BOOLEAN":
                self.add(WxGuiMapperInfo(fname=resd.name, pgitype=pg.BoolProperty, unit=un, isenabled=resd.isactive))

        self.add(WxGuiMapperInfo(fname="enviros_category", pgitype=pg.PropertyCategory, pgilabel="Environment"))
        envprep_q = sqp.SQQuery(fact, ProjectEnviroPreparation).where(ProjectEnviroPreparation.ProjectId==proj._id)
        for envprep in envprep_q:
            envd = envprep.envirodefinition
            if resd.unit is not None:
                un = envd.unit.abbreviation
            else:
                un = None
            
            self.add(WxGuiMapperInfo(fname="#ENV#"+envd.name, 
                pgilabel=envd.name,
                pgitype=pg.FloatProperty, 
                unit=un, 
                isenabled=envd.isactive))

        self.createallprops()

    def object2gui(self, obj : dict):
        """expect obj to be key,value dict and set the values of the property grid items accordingly"""
        for key, value in obj.items():
            guidecl = self[key] #self[key] is a dict too knowing all the definitions for the propgriditems
            guidecl.setvalue(self.parentpropgrid, value)

        self._parentpropgrid.Refresh()

    def gui2object(self) -> dict:
        """return the data from the property grid as key, value pairs where the key is the
        known fieldname and the values have been changed to their original types"""
        answ = {}

        for key, itemdecl in self._mapping.items():
            answ[key] = itemdecl.getvalue(self.parentpropgrid)
            if itemdecl.fieldcls is not None and issubclass(itemdecl.fieldcls, PBase):
                if answ[key] is not None:
                    answ[itemdecl.idfieldname] = answ[key]._id
                else:
                    answ[itemdecl.idfieldname] = None

        return answ


class WxGuiMapperFactorDefintion(WxGuiMapper):
    """definition for the GUI of the factor defintions data editor
    """
    def __init__(self, fact : sqp.SQFactory, parentpropgrid : pg.PropertyGrid):
        super().__init__(fact, parentpropgrid)
        self.add(WxGuiMapperInfo(fname="abbreviation", pgilabel="Abbreviation", pgitype=pg.StringProperty))
        self.add(WxGuiMapperInfo(fname="name", pgilabel="Name", pgitype=pg.StringProperty))
        self.add(WxGuiMapperInfo(fname="unit", pgitype=pg.EnumProperty, fcls=Unit, idfldname="unitid", pgilabel="Unit"))
        self.add(WxGuiMapperInfo(fname="disptype", pgitype=pg.EnumProperty, pgilabel="Display type", schoices=["FLOAT", "BOOLEAN"]))
        self.add(WxGuiMapperInfo(fname="isactive", pgitype=pg.BoolProperty, pgilabel="Is active"))
        self.add(WxGuiMapperInfo(fname="curaname", pgitype=pg.EnumProperty, fcls=CuraNameCat, pgilabel="Cura name"))
        self.add(WxGuiMapperInfo(fname="defaultmin", pgitype=pg.FloatProperty, pgilabel="default min value"))
        self.add(WxGuiMapperInfo(fname="defaultmax", pgitype=pg.FloatProperty, pgilabel="default max value"))
        self.add(WxGuiMapperInfo(fname="defaultlevelnum", pgitype=pg.IntProperty, pgilabel="default number of levels"))

        self.createallprops()

    def object2gui(self, obj):
        """expect obj to be key,value dict and set the values of the property grid items accordingly"""
        for key, value in obj.items():
            guidecl = self[key] #we are a dict too knwoing all the definitions for the propgriditems
            guidecl.setvalue(self.parentpropgrid, value)

    def gui2object(self) -> dict:
        """return the data from the property grid as key, value pairs where the key is the
        known fieldname and the values have been changed to their original types"""
        answ = {}

        for key, itemdecl in self._mapping.items():
            answ[key] = itemdecl.getvalue(self.parentpropgrid)
            if itemdecl.fieldcls is not None and issubclass(itemdecl.fieldcls, PBase):
                if answ[key] is not None:
                    answ[itemdecl.idfieldname] = answ[key]._id
                else:
                    answ[itemdecl.idfieldname] = None

        return answ


class WxGuiMapperResultDefintion(WxGuiMapper):
    """definition for the GUI of the result defintions data editor
    """
    def __init__(self, fact : sqp.SQFactory, parentpropgrid : pg.PropertyGrid):
        super().__init__(fact, parentpropgrid)
        self.add(WxGuiMapperInfo(fname="abbreviation", pgilabel="Abbreviation", pgitype=pg.StringProperty))
        self.add(WxGuiMapperInfo(fname="name", pgilabel="Name", pgitype=pg.StringProperty))
        self.add(WxGuiMapperInfo(fname="unit", pgitype=pg.EnumProperty, fcls=Unit, idfldname="unitid", pgilabel="Unit"))
        self.add(WxGuiMapperInfo(fname="isactive", pgitype=pg.BoolProperty, pgilabel="Is active"))

        self.createallprops()

    def object2gui(self, obj):
        """expect obj to be key,value dict and set the values of the property grid items accordingly"""
        for key, value in obj.items():
            guidecl = self[key] #we are a dict too knwoing all the definitions for the propgriditems
            guidecl.setvalue(self.parentpropgrid, value)

    def gui2object(self) -> dict:
        """return the data from the property grid as key, value pairs where the key is the
        known fieldname and the values have been changed to their original types"""
        answ = {}

        for key, itemdecl in self._mapping.items():
            answ[key] = itemdecl.getvalue(self.parentpropgrid)
            if itemdecl.fieldcls is not None and issubclass(itemdecl.fieldcls, PBase):
                if answ[key] is not None:
                    answ[itemdecl.idfieldname] = answ[key]._id
                else:
                    answ[itemdecl.idfieldname] = None

        return answ