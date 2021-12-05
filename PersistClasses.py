import sqlitepersist as sqp

class AbbreviatedThing(sqp.PBase):
    Abbreviation = sqp.String()
    Name = sqp.String()

class Printer(AbbreviatedThing):
    """a 3d printer"""
    ProducedBy = sqp.String()
    Release = sqp.String()
    YearOfBuild = sqp.Int()
    MonthOfBuild = sqp.Int()
    Firmware = sqp.String()
    FirmwareVersion = sqp.String()

class ModificationTarget(sqp.PCatalog):
    _cattype = "MODTARG"

class Modification(sqp.PBase):
    """a modification applied to a printer or to an extruder"""
    ParentId = sqp.UUid()
    ModTarget = sqp.Catalog(catalogtype=ModificationTarget)
    Description = sqp.String()

class Extruder(AbbreviatedThing):
    """an extruder"""
    ProducedBy = sqp.String()
    MaxTemperature = sqp.Int()
    HasCooler = sqp.Boolean()

class Unit(AbbreviatedThing):
    FactorToBase = sqp.Float()
    BaseUnit = sqp.UUid()

class Parameter(AbbreviatedThing):
    Unit = sqp.String()

class ParameterSetting(sqp.PBase):
    ParameterId = sqp.String()
    ParameterName = sqp.JoinedEmbeddedObject(targettype=Parameter, localid=ParameterId, autofill=True)
    Value = sqp.String()

class Experiment(sqp.PBase):
    CarriedOutDt = sqp.DateTime()
    ParameterSettings = sqp.JoinedEmbeddedList(targettype=ParameterSetting, foreignid="_id")
    