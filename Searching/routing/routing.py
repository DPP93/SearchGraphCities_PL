import json

class GraphCity:
    def __init__(self, name, neighbours):
        self.name = name
        self.neighbours = neighbours

class NeighbourCity:
    def __init__(self, name, population, parentName, distanceToParent, distanceToWarsaw):
        self.name = name
        self.population = population
        self.parentName = parentName
        self.distanceToParent = distanceToParent
        self.distanceToWarsaw = distanceToWarsaw

def getDistanceBetweenCities(city1Name, city2Name, citiesJson):
    for city in citiesJson:
        if city["name"] == city1Name:
            for neighbour in city["list"]:
                if neighbour["name"] == city2Name:
                    return neighbour["distance"]

def getPopulation(city, jsonCity):
    for c in jsonCity:
        if city == c["name"]:
            return c["population"]

def getDistanceToWarsaw(cityName, citiesJson):
    if cityName == "Warszawa":
        return 0
    for city in citiesJson:
        if city["name"] == cityName:
            return city["distToWarsaw"]

def generateGraph(citiesJson):
    #Zasada: każde miasto łączy się z czterama najbliższymi sobie miastom + jeśli już ma połączenie z innym
    citiesGraph = []

    for cityJson in citiesJson:
        sortedNeighbours = sorted(cityJson["list"], key=lambda x: x["distance"])
        # print(sortedNeighbours)
        newGraphCityName = cityJson["name"]
        newNeighbours = []

        neighboursLeft = 3 - len(newNeighbours)
        for i in range(0, neighboursLeft):
            neighbour = sortedNeighbours[i]
            neighbourName = neighbour["name"]
            population = getPopulation(neighbourName, citiesJson)
            parentName = newGraphCityName
            distanceToParent = getDistanceBetweenCities(parentName, neighbourName, citiesJson)
            distanceToWarsaw = getDistanceToWarsaw(neighbourName, citiesJson)
            newNeighbours.append(NeighbourCity(neighbourName, population, parentName, distanceToParent, distanceToWarsaw))

        citiesGraph.append(GraphCity(newGraphCityName, newNeighbours))

    # Znajdź powtórzenia w sąsadach (ta sama trasa)
    print ("Powtórzenia")
    citiesGraph2 = citiesGraph
    for cityFromGraph in citiesGraph:
        neighbours = []
        for cityFromGraph2 in citiesGraph2:
            if cityFromGraph.name == cityFromGraph2.name:
                continue
            for neighbourFromGraph in cityFromGraph2.neighbours:
                if neighbourFromGraph.name == cityFromGraph.name:
                    neighbourName = cityFromGraph2.name
                    population = getPopulation(cityFromGraph2.name, citiesJson)
                    parentName = cityFromGraph.name
                    distanceToParent = getDistanceBetweenCities(parentName, neighbourName, citiesJson)
                    distanceToWarsaw = getDistanceToWarsaw(neighbourName, citiesJson)
                    neighbours.append(NeighbourCity(neighbourName, population, parentName, distanceToParent, distanceToWarsaw))
        cityFromGraph.neighbours = cityFromGraph.neighbours + neighbours

    # Usuń powtarzających się sąsiadów
    for cityFromGraph in citiesGraph:
        neighbours = []
        for n in cityFromGraph.neighbours:
            found = False
            for n2 in neighbours:
                if n.name == n2.name:
                    found = True
            if found == False:
                neighbours.append(n)
        cityFromGraph.neighbours = neighbours

    for city in citiesGraph:
        print(city.name + " -------------")
        for n in city.neighbours:
            print(n.name + " " + str(n.distanceToParent) + " " + str(n.distanceToWarsaw))
        print()

    return citiesGraph



def computeBFS(graphCities, citiesJson, startingCity, numberOfCitiesWithparticularPopulation=0, minPopulation=0):
    maxDepth=6
    citiesRoute = []
    cityQueue = []
    numberOfStepsInTree = 0
    lastCityName = ""
    visitedCities = []
    cityQueue.append(startingCity)
    isOver = False
    currentDepth = 1
    while isOver !=  True or currentDepth <= maxDepth:
        print()

    return citiesRoute

def getNeighbours(city, visitedCities):
    returnedCities = []
    for neigh in city.neighbours:
        found = False
        for visitedCity in visitedCities:
            if visitedCities == neigh:
                found = True
                break
        if found == False:
            returnedCities.append(neigh)
    return returnedCities

def main():
    jsonCities = ""
    with open("cities_merged.json") as cities_json:
        jsonCities = json.load(cities_json)
    graph = generateGraph(jsonCities)


if __name__ == "__main__":
    main()