from email.policy import default
import os # needed for on_after_delete of ExperimentDocs
from datetime import datetime
from enum import unique
import sqlitepersist as sqp
from sqlitepersist.SQLitePersistBasicClasses import UUid

class AbbreviatedThing(sqp.PBase):
    Abbreviation = sqp.String(uniquegrp="ABBRUNIQ")
    Name = sqp.String()

    def __str__(self):
        return "{0}/{1}".format(self.abbreviation, self.name)

class Printer(AbbreviatedThing):
    """a 3d printer"""
    ProducedBy = sqp.String()
    Release = sqp.String()
    YearOfBuild = sqp.Int()
    MonthOfBuild = sqp.Int()
    Firmware = sqp.String()
    FirmwareVersion = sqp.String()
    IsActive = sqp.Boolean(default=True)

class ModificationTarget(sqp.PCatalog):
    _cattype = "MODTARG"

class CuraNameCat(sqp.PCatalog):
    _cattype = "SLICERNAME_CURA"
    Type = sqp.String(default="SLICERNAME_CURA") #override type default

    def __str__(self):
        return self.value

class ProjectStatusCat(sqp.PCatalog):
    _cattype = "STATUS_PROJECT"
    _langsensitive = True
    Type = sqp.String(default="STATUS_PROJECT") #override type default

    def __str__(self):
        return self.value


class ExpAttachmentTypeCat(sqp.PCatalog):
    _cattype = "EXP_ATTACH_TYPE"
    _langsensitive = False
    Type = sqp.String(default="EXP_ATTACH_TYPE") #override type default

    def __str__(self):
        return self.value

class Modification(sqp.PBase):
    """a modification applied to a printer or to an extruder"""
    ParentId = sqp.UUid()
    ModTarget = sqp.Catalog(catalogtype=ModificationTarget)
    Description = sqp.String()

class Extruder(AbbreviatedThing):
    """an extruder"""
    ProducedBy = sqp.String()
    MaxTemperature = sqp.Int(default=250)
    HasCooler = sqp.Boolean(default=True)
    IsActive = sqp.Boolean(default=True)

class Unit(AbbreviatedThing):
    FactorToBase = sqp.Float()
    BaseUnit = sqp.String()

    def __str__(self):
        return self.abbreviation

class _NamedValue(AbbreviatedThing):
    """a stored value of some kind with a unit, a GUI display type. Can be deactivated if
    not in use any more but data are stored which use it
    do not instantiate directly but use the derived classes
    """
    UnitId = sqp.UUid()
    Unit = sqp.JoinedEmbeddedObject(targettype=Unit, localid=UnitId, autfill=True)
    IsActive = sqp.Boolean(default=True)
    DispType = sqp.String(default="FLOAT")

class FactorDefinition(_NamedValue):
    """ definition for a factor - i.e. a parameter in the sclicing process
    """
    CuraName = sqp.Catalog(catalogtype=CuraNameCat)
    DefaultMin = sqp.Float()
    DefaultMax = sqp.Float()
    DefaultLevelNum = sqp.Int(default=2)
    

class ResponseDefinition(_NamedValue):
    """ definition for a result - a measrurement/rating
    """
    pass

class EnviroDefinition(_NamedValue):
    """ definition of an environmental value to be surveyed in experimnents
        in addition to the factors
    """
    pass

class FactorValue(sqp.PBase):
    """a paramater setting in an experiment - a factor"""
    FactorDefinitionId = sqp.UUid()
    ExperimentId = sqp.UUid()
    FactorDefinition = sqp.JoinedEmbeddedObject(targettype=FactorDefinition, localid=FactorDefinitionId, autofill=True)
    Value = sqp.Float()

    def __str__(self) -> str:
        unit = ""
        if self.facordefinition is not None and self.factordefinition.unit is not None:
            unit = self.factordefinition.unit.abbreviation

        return "factor val: {}{}".format(self._value, unit)


class ResponseValue(sqp.PBase):
    """The result of an experiment - a rating or a measure"""
    ResponseDefinitionId = sqp.UUid()
    ExperimentId = sqp.UUid()
    ResponseDefinition = sqp.JoinedEmbeddedObject(targettype=ResponseDefinition, localid=ResponseDefinitionId, autofill=True)
    Value = sqp.Float()

class EnviroValue(sqp.PBase):
    EnviroDefinitionId = sqp.UUid()
    ExperimentId = sqp.UUid()
    EnviroDefinition = sqp.JoinedEmbeddedObject(targettype=EnviroDefinition, localid=EnviroDefinitionId, autofill=True)
    Value = sqp.Float()

class Project(sqp.PBase):
    Name = sqp.String()
    Status = sqp.Catalog(catalogtype=ProjectStatusCat)
    IsArchived = sqp.Boolean(default=False)
    Description = sqp.String()
    #merge calculation calcalutes a merged response from the other responses by merging them with a given formula
    DoMergeCalculation = sqp.Boolean(default=False)
    MergeFormula = sqp.String()


class ProjectFactorPreparation(sqp.PBase):
    ProjectId = sqp.UUid()
    MinValue = sqp.Float()
    MaxValue = sqp.Float()
    LevelNum = sqp.Int(default=2)
    FactorDefinitionId = sqp.UUid()
    FactorDefinition = sqp.JoinedEmbeddedObject(targettype=FactorDefinition, localid=FactorDefinitionId, autofill=True)

class ProjectResponsePreparation(sqp.PBase):
    ProjectId = sqp.UUid()
    ResponseDefinitionId = sqp.UUid()
    CombinationWeight = sqp.Float()
    ResponseDefinition = sqp.JoinedEmbeddedObject(targettype=ResponseDefinition, localid=ResponseDefinitionId, autofill=True)

    @property
    def name(self):
        if self.responsedefinition is not None:
            return self.responsedefinition.name
        else:
            return None

    @property
    def unit(self):
        if self.responsedefinition is not None and self.responsedefinition.unit:
            return self.responsedefinition.unit.abbreviation
        else:
            return "-unitless-"

class ProjectEnviroPreparation(sqp.PBase):
    ProjectId = sqp.UUid()
    EnviroDefinitionId = sqp.UUid()
    EnviroDefinition =  sqp.JoinedEmbeddedObject(targettype=EnviroDefinition, localid=EnviroDefinitionId, autofill=True)

    @property
    def name(self):
        if self.envirodefinition is not None:
            return self.envirodefinition.name
        else:
            return None

    @property
    def unit(self):
        if self.envirodefinition is not None and self.envirodefinition.unit:
            return self.envirodefinition.unit.abbreviation
        else:
            return "-unitless-"

class ExperimentDoc(sqp.PBase):
    """Doc attachments to an experiment"""
    ExperimentId = sqp.UUid()
    Name = sqp.String()
    FilePath = sqp.String()
    AttachmentType = sqp.Catalog(catalogtype=ExpAttachmentTypeCat)

    def on_after_delete(self):
        #make sure that archive files are also deleted when refernce exists and is valid
        print("in method ExperimentDoc().on_after_delete()".format(self.filepath))
        if self.filepath is not None and len(self.filepath)>0:
            if os.path.exists(self.filepath) and os.path.isfile(self.filepath):
                os.remove(self.filepath)
                print("removed file <{}> by ExperimentDoc().on_after_delete()".format(self.filepath))


class FactorCombiDefInter(sqp.CommonInter):
    _intertype = "COMBIDEF_FACTDEF"
    FactorDefinition = sqp.JoinedEmbeddedObject(targettype=FactorDefinition, localid="downid", autofill=True)

class FactorCombiPreparation(sqp.PBase):
    ProjectId = sqp.UUid()
    Name = sqp.String()
    IsNegated = sqp.Boolean(default=False)
    FactorDefs = sqp.IntersectedList(targettype=FactorCombiDefInter)

class Experiment(sqp.PBase):
    ProjectId = sqp.UUid()
    ExtruderUsedId = sqp.UUid()
    PrinterUsedId = sqp.UUid()
    Project = sqp.JoinedEmbeddedObject(targettype=Project, localid=ProjectId, autofill=True)
    Sequence = sqp.Int()
    Repnum = sqp.Int()
    ExtruderUsed = sqp.JoinedEmbeddedObject(targettype=Extruder, localid=ExtruderUsedId, autofill=True)
    PrinterUsed = sqp.JoinedEmbeddedObject(targettype=Printer, localid=PrinterUsedId, autofill=True)
    CarriedOutDt = sqp.DateTime()
    IsArchived = sqp.Boolean(default=False)
    Description = sqp.String()
    Factors = sqp.JoinedEmbeddedList(targettype=FactorValue, foreignid=FactorValue.ExperimentId, cascadedelete=True)
    Responses = sqp.JoinedEmbeddedList(targettype=ResponseValue, foreignid=ResponseValue.ExperimentId, cascadedelete=True)
    Enviros = sqp.JoinedEmbeddedList(targettype=EnviroValue, foreignid=EnviroValue.ExperimentId, cascadedelete=True)
    Docs = sqp.JoinedEmbeddedList(targettype=ExperimentDoc, foreignid=ExperimentDoc.ExperimentId, cascadedelete=True)




    