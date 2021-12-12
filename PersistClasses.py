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

class Parameter(AbbreviatedThing):
    """definition for a parameter"""
    UnitId = sqp.UUid()
    Unit = sqp.JoinedEmbeddedObject(targettype=Unit, localid=UnitId, autfill=True)
    CuraName = sqp.Catalog(catalogtype=CuraNameCat)
    IsActive = sqp.Boolean(default=True)
    DispType = sqp.String(default="FLOAT")

class Setting(sqp.PBase):
    """a paramater setting in an experiment"""
    ParameterId = sqp.UUid()
    ExperimentId = sqp.UUid()
    ParameterDefinition = sqp.JoinedEmbeddedObject(targettype=Parameter, localid=ParameterId, autofill=True)
    Value = sqp.String()

class Experiment(sqp.PBase):
    ExtruderUsedId = sqp.UUid()
    PrinterUsedId = sqp.UUid()
    ExtruderUsed = sqp.JoinedEmbeddedObject(targettype=Extruder, localid=ExtruderUsedId, autofill=True)
    PrinterUsed = sqp.JoinedEmbeddedObject(targettype=Printer, localid=PrinterUsedId, autofill=True)
    CarriedOutDt = sqp.DateTime()
    IsArchived = sqp.Boolean(default=False)
    Description = sqp.String()
    Settings = sqp.JoinedEmbeddedList(targettype=Setting, foreignid=Setting.ExperimentId, cascadedelete=True)
    