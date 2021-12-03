import sqlitepersist as sqp

class AbbreviatedThing(sqp.PBase):
    Abbreviation = sqp.String()
    Name = sqp.String()

class Printer(AbbreviatedThing):
    Release = sqp.String()
    YearOfBuild = sqp.Int()
    MonthOfBuild = sqp.Int()
    Firmware = sqp.String()
    FirmwareVersion = sqp.String()

class Extruder(AbbreviatedThing):
    MaxTemperature = sqp.Int()
    HasCooler = sqp.Boolean()

class Unit(sqp.PBase):
    Name = sqp.String()
    ConvFactToBase = sqp.Float()

class Parameter(AbbreviatedThing):
    Unit = sqp.String()

class ParameterSetting(sqp.PBase):
    ParameterId = sqp.String()
    ParameterName = sqp.JoinedEmbeddedObject(targettype=Parameter, localid=ParameterId, autofill=True)
    Value = sqp.String()

class Experiment(sqp.PBase):
    CarriedOutDt = sqp.DateTime()
    ParameterSettings = sqp.JoinedEmbeddedList(targettype=ParameterSetting, foreignid="_id")
    