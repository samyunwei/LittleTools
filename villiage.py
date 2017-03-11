import json


class villiage(object):
    def __init__(self, name, town, county="", city="", geojson=""):
        self.name = name
        self.town = town
        self.county = county
        self.city = city
        self.geojson = geojson
        self.longitude = ""
        self.latitude = ""
        self._jsondict = None

    def __str__(self):
        return 'Villiage:%5s Town:%5s Count:%5s City:%s' % (self.name, self.town, self.county, self.city)

    def getSerachDict(self):
        res = {"address": self.county + self.town + self.name, "city": self.city}
        return res

    def getSaveStr(self):
        res = [self.name, self.town, self.county, self.city, self.geojson]
        res = "***".join(res) + "\n"
        return res

    def setDict(self, theJson=None):
        if theJson:
            self.geojson = theJson
        self._jsondict = json.loads(self.geojson)
        self._autoGet()

    def _autoGet(self):
        if self._jsondict == None:
            return
        if self._jsondict["status"] == "0":
            return
        location = self._jsondict["geocodes"][0]["location"].split(',')
        self.longitude = location[0]
        self.latitude = location[1]

    @classmethod
    def getVilFromString(cls, vilstr, sep="***"):
        """

        :param vilstr:
        :type vilstr:str
        :param sep:
        :type  sep:str
        :return:
        """
        temp = vilstr.split(sep)
        return villiage(temp[0], temp[1], temp[2], temp[3], temp[4])
