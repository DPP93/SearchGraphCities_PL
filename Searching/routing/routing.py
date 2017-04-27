import json

class GraphCity:
    def __init__(self, name, neighbours):
        self.name = name
        self.neighbours = neighbours


def getDistanceBetweenCities(city1, city2, citiesJson):
    for city in citiesJson:
        if city["name"] == city1.name:
            for neighbour in city["list"]:
                if neighbour["name"] == city2.name:
                    return neighbour["distance"]

def generateGraph(citiesJson):
    #Zasada: każde miasto łączy się z czterama najbliższymi sobie miastom + jeśli już ma połączenie z innym
    citiesGraph = []

    for cityJson in citiesJson:
        sortedNeighbours = sorted(cityJson["list"], key=lambda x: x["distance"])
        # print(sortedNeighbours)
        name = cityJson["name"]
        neighbours = []
        for cityGraph in citiesGraph:
            for neigh in cityGraph.neighbours:
                if name == neigh:
                    neighbours.append(cityGraph.name)
        lastCitiesToAdd = 7 - len(neighbours)
        if lastCitiesToAdd > 0:
            for i in range(0, lastCitiesToAdd):
                neighbours.append(sortedNeighbours[i]["name"])
        # print(name)
        # print(neighbours)
        # print()
        citiesGraph.append(GraphCity(name, neighbours))

    return citiesGraph

def main():
    print("Router")
    jsonCities = ""
    with open("cities_merged.json") as cities_json:
        jsonCities = json.load(cities_json)
    graph = generateGraph(jsonCities)


if __name__ == "__main__":
    main()