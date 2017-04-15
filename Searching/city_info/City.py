
class City:
    def __init__(self, cityName, population):
        self.cityName = cityName
        self.population = population
        self.listOfDistancesToOtherCities = dict()
        self.distanceToWarsaw = 0

