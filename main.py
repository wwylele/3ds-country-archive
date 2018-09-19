import country
import region
import json
import os
import shutil

def loadFromArchive(path):
    result = {}

    regions = result["regions"] = []
    for regionCode in ["CN", "EU", "JP", "KR", "TW", "US"]:
        regions.append(region.loadRegionFromArchive(path, regionCode))

    countries = result["countries"] = []

    for i in range(256):
        countryResult = country.loadCountryFromArchive(path, i)
        if countryResult is not None:
            countries.append(countryResult)

    return result

def writeToArchive(path, archive):
    shutil.rmtree(path, ignore_errors = True)
    os.mkdir(path)
    for regionCode in ["CN", "EU", "JP", "KR", "TW", "US"]:
        os.mkdir(os.path.join(path, regionCode))

    for x in archive["regions"]:
        region.writeRegionToArchive(path, x)


    for x in archive["countries"]:
        country.writeCountryToArchive(path, x)

inPath = "/home/wwylele/3ds-country-archive/origin"
outPath = "/home/wwylele/3ds-country-archive/new"
archive = loadFromArchive(inPath)
print(json.dumps(archive, indent = 2))
writeToArchive(outPath, archive)

for path, dirs, files in os.walk(inPath):
    for f in files:
        a = os.path.join(path, f)
        b = os.path.join(outPath, os.path.relpath(path, inPath) ,f)
        with open(a, "rb") as inFile, open(b, "rb") as outFile:
            assert inFile.read() == outFile.read()
