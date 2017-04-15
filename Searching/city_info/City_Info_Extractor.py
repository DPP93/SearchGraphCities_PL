import requests
import json

from city_info import City


def readApiKey(apiKeyFile):
    apiFile = open(apiKeyFile)
    apiKey = apiFile.readline()
    apiFile.close()
    return apiKey

def setupCities():
    apiKey = readApiKey("apiKey")

    requestCity = requests.get(
        "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Poznań&destinations=Warszawa&key=" + apiKey)
    response = json.loads(requestCity.text)
    print(response)

    cities = []
    cities.append(City("Szczecin", 409211))
    cities.append(City("Gdynia", 248574))
    cities.append(City("Bydgoszcz", 409211))
    cities.append(City("Gdańsk", 409211))
    cities.append(City("Białystok", 409211))
    cities.append(City("Olsztyn", 409211))
    cities.append(City("Poznań", 409211))
    cities.append(City("Wrocławek", 409211))
    cities.append(City("Częstochowa", 409211))
    cities.append(City("Katowice", 409211))
    cities.append(City("Kraków", 409211))
    cities.append(City("Rzeszów", 409211))
    cities.append(City("Przemyśl", 409211))
    cities.append(City("Krosno", 409211))
    cities.append(City("Nowy Sącz", 409211))
    cities.append(City("Zakopane", 409211))
    cities.append(City("Lublin", 409211))
    cities.append(City("Łódź", 409211))
    cities.append(City("Wrocław", 409211))
    cities.append(City("Jelenia Góra", 409211))
    cities.append(City("Zielona Góra", 409211))
    cities.append(City("Bielsko Biała", 409211))
    cities.append(City("Radom", 409211))
    cities.append(City("Chełm", 409211))
    cities.append(City("Sieradz", 409211))
    cities.append(City("Garwolin", 409211))
    cities.append(City("Ryki", 409211))
    cities.append(City("Ostrów Wielkopolski", 409211))
    cities.append(City("Kołobrzeg", 409211))
    cities.append(City("Kielce", 409211))
    cities.append(City("Zabrze", 409211))
    cities.append(City("Gliwice", 409211))
    cities.append(City("Gorzów Wielkopolski", 409211))
    cities.append(City("Bytom", 409211))
    cities.append(City("Dąbrowa Górnicza", 409211))
    cities.append(City("Chorzów", 409211))
    cities.append(City("Ruda Śląska", 409211))
    cities.append(City("Płock", 409211))
    cities.append(City("Rybnik", 409211))
    cities.append(City("Legnica", 409211))
    cities.append(City("Opole", 409211))
    cities.append(City("Tarnów", 409211))
    cities.append(City("Tychy", 409211))
    cities.append(City("Wałbrzych", 409211))
    cities.append(City("Elbląg", 409211))
    cities.append(City("Koszalin", 409211))
    cities.append(City("Suwałki", 409211))
    cities.append(City("Zamosc", 409211))

    return cities

def main():

    cities = setupCities()

if __name__ == "__main__":
    main()

