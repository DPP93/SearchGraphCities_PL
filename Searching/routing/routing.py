import json
from random import shuffle

class City:
    def __init__(self, cityName, population):
        self.cityName = cityName
        self.population = population
        self.listOfDistancesToOtherCities = []
        self.distanceToInStraightLineWarsaw = 0
        self.latitude = 0
        self.longitude = 0

class GraphCity:
    def __init__(self, name, neighbours, position):
        self.name = name
        self.neighbours = neighbours
        self.position = position

class NeighbourCity:
    def __init__(self, name, population, parentName, distanceToParent, distanceToWarsaw):
        self.name = name
        self.population = population
        self.parentName = parentName
        self.distanceToParent = distanceToParent
        self.distanceToWarsaw = distanceToWarsaw


class TreeNode:
    def __init__(self, name, parentNode, childNodes, position, population = 0, distance = 0, distanceWarsaw = 0):
        self.name = name
        self.parentNode = parentNode
        self.childNodes = childNodes
        self.population = population
        self.distance = distance
        self.position = position
        self.distanceWarsaw = distanceWarsaw

def getDistanceBetweenCities(city1Name, city2Name, citiesJson):
    for city in citiesJson:
        if city["name"] == city1Name:
            for neighbour in city["list"]:
                if neighbour["name"] == city2Name:
                    return neighbour["distance"]

def getPopulation(cityName, jsonCity):
    for c in jsonCity:
        if cityName == c['name']:
            return c["population"]


def getDistanceToWarsaw(cityName, citiesJson):
    if cityName == "Warszawa":
        return 0
    for city in citiesJson:
        if city["name"] == cityName:
            return city["distToWarsaw"]

def generateGraph(citiesJson, maxNumbersOfNeighbours=5):
    #Zasada: każde miasto łączy się z czterama najbliższymi sobie miastom + jeśli już ma połączenie z innym
    citiesGraph = []

    for cityJson in citiesJson:
        sortedNeighbours = sorted(cityJson["list"], key=lambda x: x["distance"])
        # print(sortedNeighbours)
        newGraphCityName = cityJson["name"]
        newNeighbours = []
        position = getPosition(cityJson["lat"], cityJson["lng"])
        neighboursLeft = maxNumbersOfNeighbours - len(newNeighbours)
        for i in range(0, neighboursLeft):
            neighbour = sortedNeighbours[i]
            neighbourName = neighbour["name"]
            population = getPopulation(neighbourName, citiesJson)
            parentName = newGraphCityName
            distanceToParent = getDistanceBetweenCities(parentName, neighbourName, citiesJson)
            distanceToWarsaw = getDistanceToWarsaw(neighbourName, citiesJson)
            newNeighbours.append(NeighbourCity(neighbourName, population, parentName, distanceToParent, distanceToWarsaw))

        citiesGraph.append(GraphCity(newGraphCityName, newNeighbours, position))

    # Znajdź powtórzenia w sąsadach (ta sama trasa)
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

    return citiesGraph

def computeBFS(graphCities, citiesJson, startingCityName, numberOfCitiesWithparticularPopulation=0, minPopulation=0, maxDepth = 10):
    vNodes = []

    rootNode = TreeNode(startingCityName, None, [], getJsonPosition(startingCityName, citiesJson),
                        getPopulation(startingCityName, citiesJson), 0,
                        getDistanceToWarsaw(startingCityName, citiesJson))
    rootNode.childNodes = getNodeNeighbours(rootNode, graphCities, citiesJson)

    vNodes.append(rootNode)
    nodeQueue = list()
    nodeQueue += rootNode.childNodes

    lastNode = ""
    while True:
        if len(nodeQueue) == 0:
            break

        #Odczytaj pierwszy node z kolejki
        currentNode = nodeQueue.pop(0)

        if len(getRouteToRootNode(currentNode)) > maxDepth:
            continue

        #Sprtawdź czy to Warszawa, jak tak to kończ i podstaw pod lastNode
        if currentNode.name != "Warszawa":
            vNodes.append(currentNode)
        if checkEnd(currentNode, numberOfCitiesWithparticularPopulation, minPopulation):
            lastNode = currentNode
            break

        #Pobierz sąsiednie Node'y (dodaj na koniec kolejki te nieodwiedzone)
        currentNode.childNodes = getNodeNeighbours(currentNode, graphCities, citiesJson)
        for child in currentNode.childNodes:
            found = False
            # visitedNumber = len(visitedNodes)
            # if visitedNumber > 4:
            #     for i in range(visitedNumber - 4, visitedNumber-1):
            #         if visitedNodes[i].name == child.parentNode.name:
            #             found = True
            # else:
            visitedNodes = getRouteToRootNode(currentNode)
            for visited in visitedNodes:
                if visited.name == child.name:
                    found = True
            if found == False:
                nodeQueue.append(child)

    printResult(lastNode, vNodes, "BFS")

def getJsonPosition (cityName, citiesJson):
    for c in citiesJson:
        if cityName == c['name']:
            return getPosition(c["lat"], c["lng"])

def getPosition (lat, lng):
    midLng = 19
    midLat = 52

    if lat >= midLat:
        if lng <= midLng:
            return "I"
        else:
            return "II"
    else:
        if lng <= midLng:
            return "III"
        else:
            return "IV"

def computeDFS(graphCities, citiesJson, startingCityName, numberOfCitiesWithparticularPopulation=0, minPopulation=0, maxDepth = 10):
    vNodes = []

    rootNode = TreeNode(startingCityName, None, [], getJsonPosition(startingCityName, citiesJson),
                        getPopulation(startingCityName, citiesJson), 0,
                        getDistanceToWarsaw(startingCityName, citiesJson))
    rootNode.childNodes = getNodeNeighbours(rootNode, graphCities, citiesJson)

    vNodes.append(rootNode)
    nodeQueue = list()
    nodeQueue += rootNode.childNodes

    lastNode = ""
    while True:

        if len(nodeQueue) == 0:
            break

        #Odczytaj pierwszy node z kolejki
        currentNode = nodeQueue.pop(0)

        if len(getRouteToRootNode(currentNode)) > maxDepth:
            continue

        #Sprtawdź czy to Warszawa, jak tak to kończ i podstaw pod lastNode
        if currentNode.name != "Warszawa":
            vNodes.append(currentNode)
        if checkEnd(currentNode, numberOfCitiesWithparticularPopulation, minPopulation):
            lastNode = currentNode
            break

        #Pobierz sąsiednie Node'y (dodaj na początek kolejki te nieodwiedzone)
        currentNode.childNodes = getNodeNeighbours(currentNode, graphCities, citiesJson)
        for child in currentNode.childNodes:
            found = False
            visitedNodes = getRouteToRootNode(currentNode)
            for visited in visitedNodes:
                if visited.name == child.name:
                    found = True
            if found == False:
                nodeQueue = [child] + nodeQueue

    printResult(lastNode, vNodes, "DFS")

def printResult(lastNode, visitedNodes, algorithmName):
    # print ("----------------" + algorithmName + " Route-----------------")
    route = getRouteToRootNode(lastNode)
    distance = 0
    citiesNames = []
    for r in route:
        if r != "":
            # print (r.name + " " + str(r.position) + " pop. " + str(r.population))
            citiesNames = [r.name] + citiesNames
            distance += r.distance
    # print (citiesNames)

    # print ("Depth " + str(len(route)))
    # print ("WHOLE DISTANCE " + str(distance) + "km")
    # print ("Visited nodes " + str(len(visitedNodes)))
    return distance, len(route), len(visitedNodes)


def getRouteToRootNode (lastNode):
    route = []
    node = lastNode
    while True:
        route.append(node)
        if node == "" or node.parentNode == None:
            break
        node = node.parentNode
    return route

def checkEnd(node, numberofCitiesWithParticularPopulation, minPopulation):
    if node.name != "Warszawa":
        return False

    route = getRouteToRootNode(node)
    visitedCitiesWithPopulation = 0
    polandParts = set()
    for r in route:
        if r.name != "Warszawa":
            polandParts.add(r.position)
        if r.name != "Warszawa" and r.population >= minPopulation:
            visitedCitiesWithPopulation += 1
    if visitedCitiesWithPopulation >= numberofCitiesWithParticularPopulation and len(polandParts) > 1:
        return True

    return False

def checkPopulation(node, numberofCitiesWithParticularPopulation, minPopulation):

    route = getRouteToRootNode(node)
    visitedCitiesWithPopulation = 0

    for r in route:
        if r.name != "Warszawa" and r.population >= minPopulation:
            visitedCitiesWithPopulation += 1
    if visitedCitiesWithPopulation >= numberofCitiesWithParticularPopulation:
        return True
    return False

def computeGreedySearch(graphCities, citiesJson, startingCityName, numberOfCitiesWithparticularPopulation=0, minPopulation=0, maxDepth = 10):
    vNodes = []
    rootNode = TreeNode(startingCityName, None, [], getJsonPosition(startingCityName, citiesJson),getPopulation(startingCityName, citiesJson), 0, getDistanceToWarsaw(startingCityName, citiesJson))
    rootNode.childNodes = getNodeNeighbours(rootNode, graphCities, citiesJson)

    rootNode.childNodes = sorted(rootNode.childNodes, key=lambda x: x.distanceWarsaw)

    vNodes.append(rootNode)
    nodeQueue = []

    nodeQueue = rootNode.childNodes + nodeQueue

    lastNode = ""
    while True:

        if len(nodeQueue) == 0:
            break

        currentNode = nodeQueue.pop(0)

        if len(getRouteToRootNode(currentNode)) > maxDepth:
            continue

        if checkEnd(currentNode, numberOfCitiesWithparticularPopulation, minPopulation):
            lastNode = currentNode
            break

        currentNode.childNodes = getNodeNeighbours(currentNode, graphCities, citiesJson)
        currentNode.childNodes = getSortedChilds(currentNode, numberOfCitiesWithparticularPopulation, minPopulation)
        if currentNode.name != "Warszawa":
            vNodes.append(currentNode)

        visitedNodes = getRouteToRootNode(currentNode)
        for child in currentNode.childNodes:
            found = False
            for visited in visitedNodes:
                if visited.name == child.name:
                    found = True
            if found == False:
                nodeQueue.append(child)

    return printResult(lastNode, vNodes, "Greedy")

def getSortedChilds (parent, numberOfCitiesWithparticularPopulation, minPopulation):
    childs = []
    route = getRouteToRootNode(parent)
    #Check if we changed part of Poland
    changedPart = checkChangedPart(route)
    #Check population
    changedPopulation = checkPopulation(parent, numberOfCitiesWithparticularPopulation, minPopulation)

    for c in parent.childNodes:
        if c.name == "Warszawa":
            c.population = 0

    #Najpierw na populacje, potem na zmianę częsci polski
    if changedPopulation == False:
        parent.childNodes = sorted(parent.childNodes, key=lambda x: x.distanceWarsaw)
        parent.childNodes = sorted(parent.childNodes, key=lambda x: x.population, reverse=True)
        return parent.childNodes

    if changedPart == False:
        childs = getElementsWithOtherPosition(parent)
        return childs

    childs = sorted(parent.childNodes, key=lambda x: x.distanceWarsaw)
    return childs


def checkChangedPart(route):
    parts = set()
    for r in route:
        parts.add(r)
    if len(parts) > 1:
        return True
    return False

def getElementsWithOtherPosition(parent):
    childs = list()
    parentBase = parent.position
    for c in parent.childNodes:
        if str(c.position) != str(parent.position):
            childs.append(c)

    for c in parent.childNodes:
        found = False
        for ch in childs:
            if c.name == ch.name:
                found = True
        if found == False:
            childs.append(c)
    return childs

def computeAStarSearch(graphCities, citiesJson, startingCityName, numberOfCitiesWithparticularPopulation=0, minPopulation=0, maxDepth = 10):
    vNodes = []
    rootNode = TreeNode(startingCityName, None, [], getJsonPosition(startingCityName, citiesJson),
                        getPopulation(startingCityName, citiesJson), 0,
                        getDistanceToWarsaw(startingCityName, citiesJson))
    rootNode.childNodes = getNodeNeighbours(rootNode, graphCities, citiesJson)

    rootNode.childNodes = sorted(rootNode.childNodes, key=lambda x: x.distanceWarsaw)

    vNodes.append(rootNode)
    nodeQueue = []

    nodeQueue = rootNode.childNodes + nodeQueue

    lastNode = ""
    while True:

        if len(nodeQueue) == 0:
            break

        currentNode = nodeQueue.pop(0)

        if len(getRouteToRootNode(currentNode)) > maxDepth:
            continue

        if checkEnd(currentNode, numberOfCitiesWithparticularPopulation, minPopulation):
            lastNode = currentNode
            break

        currentNode.childNodes = getNodeNeighbours(currentNode, graphCities, citiesJson)
        currentNode.childNodes = getSortedChilds(currentNode, numberOfCitiesWithparticularPopulation, minPopulation)
        currentNode.childNodes = sortChildsByDistanceWhichIneedToTravel(currentNode)
        if currentNode.name != "Warszawa":
            vNodes.append(currentNode)

        visitedNodes = getRouteToRootNode(currentNode)
        for child in currentNode.childNodes:
            found = False
            for visited in visitedNodes:
                if visited.name == child.name:
                    found = True
            if found == False:
                nodeQueue.append(child)

    return printResult(lastNode, vNodes, "A*")

def sortChildsByDistanceWhichIneedToTravel(currentNode):
    route = getRouteToRootNode(currentNode)
    traveledDistance = 0
    for r in route:
        traveledDistance += r.distance

    childs = []
    for c in currentNode.childNodes:
        childs.append({'name': c.name, 'val': (traveledDistance + c.distance + c.distanceWarsaw)})
    childs = sorted(childs, key=lambda x: x['val'])
    returnChilds = []
    for c in childs:
        for ch in currentNode.childNodes:
            if str(c['name']) == str(ch.name):
                returnChilds.append(ch)
    return returnChilds


def getNodeNeighbours(parentNode, graphCities, citiesJson):
    #Znajdź parenta grafie
    neighboursGraph = []
    neighboursNodes = []
    for parent in graphCities:
        if parentNode.name == parent.name:
            neighboursGraph = parent.neighbours
            break
    #Nie podpisanaj parenta jako sąsiada
    for n in neighboursGraph:
        neighboursNodes.append(TreeNode(n.name, parentNode, [], getJsonPosition(n.name, citiesJson), getPopulation(n.name, citiesJson), getDistanceBetweenCities(parentNode.name, n.name, citiesJson), getDistanceToWarsaw(n.name, citiesJson)))

    return neighboursNodes

def getNonVisitedNeighbours(neighbours, visitedCities):
    citiesToVisit = []
    for n in neighbours:
        found = False
        for v in visitedCities:
            if n.name == v.name:
                found = True
        if found == False:
            citiesToVisit.append(n)
    return citiesToVisit


def main():
    jsonCities = ""
    with open("cities_merged.json") as cities_json:
        jsonCities = json.load(cities_json)

    minimumCities = 2
    maxDepth = 10
    minimalPopulation = 400000
    minNumberOfNeighbours = 15

    graph = generateGraph(jsonCities, minNumberOfNeighbours)

    print("-+-+-+-+GRAPH+-+-+-+")

    for g in graph:
        shuffle(g.neighbours)
        for n in g.neighbours:
            if n.name == "Warszawa":
                n.population = 0



    # print("-+-+-+-+-+-+-+")
    cities = []
    cities.append(City("Warszawa", 1711000))
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


    greedyDistance = 0
    greedyDepth = 0
    greedyVisited = 0
    for c in cities:
        startingCity = c.cityName
        if c.cityName != "Warszawa":
            # print (c.cityName+"+++++++++++++++++")
            distance, depth, visited = computeGreedySearch(graph, jsonCities, startingCity, minimumCities, minimalPopulation, maxDepth)
            greedyDistance += distance
            greedyDepth += depth
            greedyVisited += visited

    print ("Greedy distance " + str(greedyDistance/(len(cities))))
    print("Greedy depth " + str(greedyDepth / (len(cities))))
    print("Greedy visited " + str(greedyVisited/ (len(cities))))

    greedyDistance = 0
    greedyDepth = 0
    greedyVisited = 0

    for c in cities:
        startingCity = c.cityName
        if c.cityName != "Warszawa":
            # print (c.cityName+"+++++++++++++++++")
            distance, depth, visited = computeAStarSearch(graph, jsonCities, startingCity, minimumCities, minimalPopulation, maxDepth)
            greedyDistance += distance
            greedyDepth += depth
            greedyVisited += visited

    print ("A* distance " + str(greedyDistance/(len(cities))))
    print("A* depth " + str(greedyDepth / (len(cities))))
    print("A* visited " + str(greedyVisited/ (len(cities))))
    # print("-+-+-+-+-+-+-+")
    # computeAStarSearch(graph, jsonCities, startingCity, minimumCities, minimalPopulation, maxDepth)

    #TODO: 

if __name__ == "__main__":
    main()