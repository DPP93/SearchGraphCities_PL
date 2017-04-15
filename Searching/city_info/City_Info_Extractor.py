import requests
import json

class City:
    def __init__(self, cityName, population):
        self.cityName = cityName
        self.population = population
        self.listOfDistancesToOtherCities = dict()
        self.distanceToWarsaw = 0
        self.latitude = 0
        self.longitude = 0

def readDistanceBetweenCities(distanceJson):
   pass

def readPositionOfCity(geocodingJson):
    pass

def readApiKey(apiKeyFile):
    apiFile = open(apiKeyFile)
    apiKey = apiFile.readline()
    apiFile.close()
    return apiKey

def setupCities():
    apiKey = readApiKey("apiKey")
    apiKeyGeo = readApiKey("apiKeyGeocoding")
    print (apiKey)
    print(apiKeyGeo)
    requestCity = requests.get(
        "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Poznań&destinations=Warszawa&key=" + apiKey)

    response = json.loads(requestCity.text)
    print(response)

    requestLatitude = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=Szczecin&key=" + apiKeyGeo)

    resp = json.loads(requestLatitude.text)
    print(resp)

    cities = []
    cities.append(City("Szczecin", 409211))
    cities.append(City("Gdynia", 248574))
    cities.append(City("Bydgoszcz", 362286))
    cities.append(City("Gdańsk", 460354))
    cities.append(City("Białystok", 294675))
    cities.append(City("Olsztyn", 175482))
    cities.append(City("Poznań", 552393))
    cities.append(City("Włocławek", 115982))
    cities.append(City("Częstochowa", 235156))
    cities.append(City("Katowice", 308269))
    cities.append(City("Kraków", 759131))
    cities.append(City("Rzeszów", 180776))
    cities.append(City("Przemyśl", 62485))
    cities.append(City("Krosno", 46934))
    cities.append(City("Nowy Sącz", 83903))
    cities.append(City("Zakopane", 27486))
    cities.append(City("Lublin", 324637))
    cities.append(City("Łódź", 722022))
    cities.append(City("Wrocław", 631377))
    cities.append(City("Jelenia Góra", 84306))
    cities.append(City("Zielona Góra", 119182))
    cities.append(City("Bielsko Biała", 174291))
    cities.append(City("Radom", 220062))
    cities.append(City("Chełm", 63949))
    cities.append(City("Sieradz", 44045))
    cities.append(City("Garwolin", 16710))
    cities.append(City("Ryki", 9716))
    cities.append(City("Ostrów Wielkopolski", 72360))
    cities.append(City("Kołobrzeg", 46830))
    cities.append(City("Kielce", 201363))
    cities.append(City("Zabrze", 179861))
    cities.append(City("Gliwice", 186347))
    cities.append(City("Gorzów Wielkopolski", 124470))
    cities.append(City("Bytom", 175377))
    cities.append(City("Dąbrowa Górnicza", 125063))
    cities.append(City("Chorzów", 111314))
    cities.append(City("Ruda Śląska", 142672))
    cities.append(City("Płock", 124048))
    cities.append(City("Rybnik", 140863))
    cities.append(City("Legnica", 102708))
    cities.append(City("Opole", 118938))
    cities.append(City("Tarnów", 113188))
    cities.append(City("Tychy", 129087))
    cities.append(City("Wałbrzych", 119216))
    cities.append(City("Elbląg", 123977))
    cities.append(City("Koszalin", 109183))
    cities.append(City("Suwałki", 69527))
    cities.append(City("Zamość", 65149))
    cities.append(City("Warszawa", 1711000))

    for city in cities:
        print (city.cityName)

    return cities

def main():
    setupCities()

if __name__ == "__main__":
    main()

