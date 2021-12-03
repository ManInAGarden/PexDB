import json
from dataclasses import dataclass

class SubProperty():
    def __init__(self, subdict):
        self.__subdict = subdict
        self.SelfiefyMe()            

    def SelfiefyMe(self):
        for key,val in self.__subdict.items():
            if not val is dict:
                setattr(self, key, val)
            else:
                raise BaseException("Subattribut <" + key + "> in Klasse <" +  type(self).__name__)

@dataclass
class DbConnectionProperties(SubProperty):
    name : str
    user : str
    password : str
    url : str
    subname : str

    def __init__(self, subdict):
        super().__init__(subdict)
        url = self.url
        url = url.replace("${user}", self.user)
        url = url.replace("${password}", self.password)
        url = url.replace("${DbName}", self.name)
        self.url = url

@dataclass
class EMailSettingProperties(SubProperty):
    progname : str
    emailaddrsep : str

    def __init__(self, subdict):
        super().__init__(subdict)


"""Properties in JSON-Format in einer Datei verwalten"""
@dataclass
class Properties():
    dbconnection : DbConnectionProperties
    emailsettings : EMailSettingProperties

    def __init__(self, filename, readnow = True):
        self.filename = filename
        self.__rawconf = None
        if readnow:
            self.ReadConfig()

    def ReadConfig(self):
        with open(self.filename, 'r') as myfile:
            data=myfile.read()
            self.__rawconf = json.loads(data)
        self.SelfyfieMe()

    def SelfyfieMe(self):
        for key,val in self.__rawconf.items():
            if not type(val) is dict:
                setattr(self, key, val)
            else:
                if key=="dbconnection":
                    setattr(self, key, DbConnectionProperties(val))
                elif key=="emailsettings":
                    setattr(self, key, EMailSettingProperties(val))
                else:
                    raise BaseException("Unbekanntes ")
                



if __name__ == '__main__':
    properties = Properties("PexDb.conf")
    print(properties.dbconnection.name)
    print(properties.dbconnection.url)
