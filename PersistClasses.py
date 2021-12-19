from enum import unique
import sqlitepersist as sqp

class AbbreviatedThing(sqp.PBase):
    Abbreviation = sqp.String()
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
    do not instatiate directly but use the derived classes
    """
    UnitId = sqp.UUid()
    Unit = sqp.JoinedEmbeddedObject(targettype=Unit, localid=UnitId, autfill=True)
    IsActive = sqp.Boolean(default=True)
    DispType = sqp.String(default="FLOAT")

class FactorDefinition(_NamedValue):
    """definition for a factor - i.e. a parameter in the sclicing process"""
    CuraName = sqp.Catalog(catalogtype=CuraNameCat)
    

class ResultDefinition(_NamedValue):
    """definition for a result - a measrurement/rating"""
    pass

class FactorValue(sqp.PBase):
    """a paramater setting in an experiment - a factor"""
    FactorDefinitionId = sqp.UUid()
    ExperimentId = sqp.UUid()
    FactorDefinition = sqp.JoinedEmbeddedObject(targettype=FactorDefinition, localid=FactorDefinitionId, autofill=True)
    Value = sqp.String()

class ResultValue(sqp.PBase):
    """The result of an experiment - a rating or a measure"""
    ResultDefId = sqp.UUid()
    ExperimentId = sqp.UUid()
    ResultDefinition = sqp.JoinedEmbeddedObject(targettype=ResultDefinition, localid=ResultDefId, autofill=True)
    Value = sqp.Float()

class Project(sqp.PBase):
    Name = sqp.String()
    Status = sqp.Catalog(catalogtype=ProjectStatusCat)
    IsArchived = sqp.Boolean(default=False)

class Experiment(sqp.PBase):
    ProjectId = sqp.UUid()
    ExtruderUsedId = sqp.UUid()
    PrinterUsedId = sqp.UUid()
    Project = sqp.JoinedEmbeddedObject(targettype=Project, localid=ProjectId, autofill=True)
    ExtruderUsed = sqp.JoinedEmbeddedObject(targettype=Extruder, localid=ExtruderUsedId, autofill=True)
    PrinterUsed = sqp.JoinedEmbeddedObject(targettype=Printer, localid=PrinterUsedId, autofill=True)
    CarriedOutDt = sqp.DateTime()
    IsArchived = sqp.Boolean(default=False)
    Description = sqp.String()
    Factors = sqp.JoinedEmbeddedList(targettype=FactorValue, foreignid=FactorValue.ExperimentId, cascadedelete=True)
    