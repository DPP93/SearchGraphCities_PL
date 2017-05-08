import json

def mergeJsons(firstJsonFileName, secondJsonFileName):

    firstJson = ""
    secondJson = ""

    with open(firstJsonFileName) as first_json_data:
        firstJson = json.load(first_json_data)

    with open(secondJsonFileName) as second_json_data:
        secondJson = json.load(second_json_data)

    mergedJson = []

    for city in firstJson:
        if city["name"] != "Warszawa":
            mergedJson.append(city)

    for city in mergedJson:
        if city["ditToWarsaw"] == 6125.918851261341:
            for city_second in secondJson:
                if city["name"] == city_second["name"]:
                    city["ditToWarsaw"] = city_second["ditToWarsaw"]
        for neighbour_city in city["list"]:
            if neighbour_city["distance"] == 0:
                for city_second in secondJson:
                    if city["name"] == city_second["name"]:
                        for neighbour_city_second in city_second["list"]:
                            if neighbour_city["name"] == neighbour_city_second["name"]:
                                neighbour_city["distance"] = neighbour_city_second["distance"]

    mergedcities = open("cities_merged.json", "w+")
    res = json.dumps(mergedJson, ensure_ascii=False)
    mergedcities.write(res)
    mergedcities.close()


def main():
    mergeJsons("cities.json", "cities2.json")

if __name__ == "__main__":
    main()
