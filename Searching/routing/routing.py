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

class TreeNode:
    def __init__(self, name, parentNode, childNodes, population = 0, distance = 0, distanceWarsaw = 0):
        self.name = name
        self.parentNode = parentNode
        self.childNodes = childNodes
        self.population = population
        self.distance = distance
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

        neighboursLeft = maxNumbersOfNeighbours - len(newNeighbours)
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
    visitedNodes = []

    rootNode = TreeNode(startingCityName, None, [], getPopulation(startingCityName, citiesJson), 0, getDistanceToWarsaw(startingCityName, citiesJson))
    rootNode.childNodes = getNodeNeighbours(rootNode, graphCities, citiesJson)

    visitedNodes.append(rootNode)
    nodeQueue = []
    nodeQueue += rootNode.childNodes

    currentDepth = 2
    lastNode = ""
    parentNode = rootNode
    widthIndex = 0
    while currentDepth <= maxDepth:
        #Odczytaj pierwszy node z kolejki
        currentNode = nodeQueue.pop(0)
        if len(getRouteToRootNode(currentNode)) > maxDepth:
            break
        #Sprtawdź czy to Warszawa, jak tak to kończ i podstaw pod lastNode
        if currentNode.name != "Warszawa":
            visitedNodes.append(currentNode)
        if checkEnd(currentNode, numberOfCitiesWithparticularPopulation, minPopulation):
        # if currentNode.name == "Warszawa":
            lastNode = currentNode
            break
        #Pobierz sąsiednieNode'y (dodaj do kolejki te nieodwiedzone)
        currentNode.childNodes = getNodeNeighbours(currentNode, graphCities, citiesJson)
        for child in currentNode.childNodes:
            found = False
            for visited in visitedNodes:
                if visited.name == child.name:
                    found = True
            if found == False:
                nodeQueue.append(child)
        widthIndex += 1;
    printResult(lastNode, visitedNodes, "BFS")



def printResult(lastNode, visitedNodes, algorithmName):
    print ("----------------" + algorithmName + " Route-----------------")
    route = getRouteToRootNode(lastNode)
    distance = 0

    for r in route:
        if r != "":
            print (r.name + " pop. " + str(r.population))
            distance += r.distance

    print ("Depth " + str(len(route)))
    print ("WHOLE DISTANCE " + str(distance) + "km")
    print ("Visited nodes " + str(len(visitedNodes)))

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

    for r in route:

        if r.name != "Warszawa" and r.population >= minPopulation:
            visitedCitiesWithPopulation += 1
    if visitedCitiesWithPopulation >= numberofCitiesWithParticularPopulation:
        return True

    return False

def computeGreedySearch(graphCities, citiesJson, startingCityName, numberOfCitiesWithparticularPopulation=0, minPopulation=0, maxDepth = 10):
    visitedNodes = []

    rootNode = TreeNode(startingCityName, None, [], getPopulation(startingCityName, citiesJson), 0, getDistanceToWarsaw(startingCityName, citiesJson))
    rootNode.childNodes = getNodeNeighbours(rootNode, graphCities, citiesJson)
    print (rootNode.name)

    rootNode.childNodes = sorted(rootNode.childNodes, key=lambda x: x.distanceWarsaw)

    visitedNodes.append(rootNode)
    nodeQueue = []

    nodeQueue = rootNode.childNodes + nodeQueue

    lastNode = ""
    parentNode = rootNode
    widthIndex = 0
    while True:
        #Odczytaj pierwszy node z kolejki
        if len(nodeQueue) == 0:
            break
        currentNode = nodeQueue.pop(0)

        if len(getRouteToRootNode(currentNode)) > maxDepth:
            continue

        if len(getRouteToRootNode(currentNode)) > maxDepth:
            if len(nodeQueue) == 0:
                break
            else:
                continue

        #Sprtawdź czy to Warszawa, jak tak to kończ i podstaw pod lastNode
        if checkEnd(currentNode, numberOfCitiesWithparticularPopulation, minPopulation):
            lastNode = currentNode
            break

        #Pobierz sąsiednieNode'y (dodaj do kolejki te nieodwiedzone)
        currentNode.childNodes = getNodeNeighbours(currentNode, graphCities, citiesJson)
        currentNode.childNodes = sorted(currentNode.childNodes, key=lambda x: x.distance, reverse=True)
        if currentNode.name != "Warszawa":
            visitedNodes.append(currentNode)
        for child in currentNode.childNodes:
            found = False
            for visited in visitedNodes:
                if visited.name == child.name:
                    found = True
            if found == False:
                nodeQueue = nodeQueue + [child]
        widthIndex += 1;

    printResult(lastNode, visitedNodes, "Greedy")



def getNodeNeighbours(parentNode, graphCities, citiesJson):
    #Znajdź parenta grafie
    parentGraphCity = ""
    neighboursGraph = []
    neighboursNodes = []
    for parent in graphCities:
        if parentNode.name == parent.name:
            parentGraphCity = parent
            neighboursGraph = parent.neighbours
            break
    #Nie podpisanaj parenta jako sąsiada
    for n in neighboursGraph:
        neighboursNodes.append(TreeNode(n.name, parentNode, [], getPopulation(n.name, citiesJson), getDistanceBetweenCities(parentNode.name, n.name, citiesJson), getDistanceToWarsaw(n.name, citiesJson)))

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

    minimumCities = 1
    maxDepth = 5
    minimalPopulation = 300000
    maxNumberOfNeighbours = 9

    graph = generateGraph(jsonCities, maxNumberOfNeighbours)
    startingCity = "Szczecin"
    print("-+-+-+-+-+-+-+")
    computeBFS(graph, jsonCities, startingCity, minimumCities, minimalPopulation, maxDepth)
    print("-+-+-+-+-+-+-+")
    computeGreedySearch(graph, jsonCities, startingCity, minimumCities, minimalPopulation, maxDepth)

if __name__ == "__main__":
    main()