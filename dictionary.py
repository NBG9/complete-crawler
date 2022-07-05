import os
import hashlib
import json

def getWholeTable(filePath):
    with open(filePath, errors="ignore") as file:
        lines = file.readlines()
        string = ""

        starts = [i for i in range(len(lines)) if lines[i].startswith('  Destination ID = ')]
        ends = [i for i in range(len(lines)) if lines[i].startswith('    Total number of codes: ')]

        tables = []

        try:
            for i in range(len(starts)):
                for line in lines[starts[i] - 1:ends[i] + 1]:
                    tables.append(line.replace(" ", "").strip().replace("\n", ""))
        except:
            tables.append("")

        for s in tables:
            string += s

        return string

def getFileName(filePath):
    with open(filePath, errors="ignore") as file:
        try:
            lines = file.readlines()

            fileName = [i for i in range(len(lines)) if lines[i].startswith('  Filename:')]

            return (lines[fileName[0]].strip().replace(" ", ""))

        except:
            return("")

def getMake(filePath):
    with open(filePath, errors="ignore") as file:
        try:
            lines = file.readlines()

            brand = [i for i in range(len(lines)) if lines[i].startswith('    [Make')]

            return (lines[brand[0]].strip().replace(" ", ""))

        except:
            return("")

def getModel(filePath):
    with open(filePath, errors="ignore") as file:
        try:
            lines = file.readlines()

            model = [i for i in range(len(lines)) if lines[i].startswith('    [Model')]

            return (lines[model[0]].strip().replace(" ", ""))

        except:
            return("")

def makeDict(path):
    dictionary = {}
    
    for file in os.listdir(path):
        filepath = path + "/" + file)

        whole_table = getWholeTable(filepath)
        hash_of_whole_table = hashlib.sha256(whole_table.encode()).hexdigest()

        image = getFileName(filepath)
        model = getModel(filepath)
        make = getMake(filepath)

        if hash_of_whole_table not in dictionary:
            dictionary[hash_of_whole_table] = {}
            dictionary[hash_of_whole_table]['details'] = {}
            dictionary[hash_of_whole_table]['0/0'] = {}
            dictionary[hash_of_whole_table]['0/1'] = {}
            dictionary[hash_of_whole_table]['1/0'] = {}
            dictionary[hash_of_whole_table]['1/1'] = {}

            dictionary[hash_of_whole_table]['0/0']['models'] = []
            dictionary[hash_of_whole_table]['0/1']['models'] = []
            dictionary[hash_of_whole_table]['1/0']['models'] = []
            dictionary[hash_of_whole_table]['1/1']['models'] = []

            dictionary[hash_of_whole_table]['0/0']['makes'] = []
            dictionary[hash_of_whole_table]['0/1']['makes'] = []
            dictionary[hash_of_whole_table]['1/0']['makes'] = []
            dictionary[hash_of_whole_table]['1/1']['makes'] = []

            dictionary[hash_of_whole_table]['0/0']['images'] = []
            dictionary[hash_of_whole_table]['0/1']['images'] = []
            dictionary[hash_of_whole_table]['1/0']['images'] = []
            dictionary[hash_of_whole_table]['1/1']['images'] = []

            dictionary[hash_of_whole_table]['details']['models'] = []
            dictionary[hash_of_whole_table]['details']['makes'] = []
            dictionary[hash_of_whole_table]['details']['images'] = []

            dictionary[hash_of_whole_table]['whole'] = whole_table


        dictionary[hash_of_whole_table]['details']['models'].append(model)
        dictionary[hash_of_whole_table]['details']['makes'].append(make)
        dictionary[hash_of_whole_table]['details']['images'].append(image)


        for substring in whole_table.split("----"):
            if len(substring) > 0:
                if "DestinationID=0Class=0" in substring:
                    dictionary[hash_of_whole_table]['0/0']['val'] = substring
                    dictionary[hash_of_whole_table]['0/0']['models'].append(model)
                    dictionary[hash_of_whole_table]['0/0']['makes'].append(make)
                    dictionary[hash_of_whole_table]['0/0']['images'].append(image)

                elif "DestinationID=0Class=1" in substring:
                    dictionary[hash_of_whole_table]['0/1']['val'] = substring
                    dictionary[hash_of_whole_table]['0/1']['models'].append(model)
                    dictionary[hash_of_whole_table]['0/1']['makes'].append(make)
                    dictionary[hash_of_whole_table]['0/1']['images'].append(image)

                elif "DestinationID=1Class=0" in substring:
                    dictionary[hash_of_whole_table]['1/0']['val'] = substring
                    dictionary[hash_of_whole_table]['1/0']['models'].append(model)
                    dictionary[hash_of_whole_table]['1/0']['makes'].append(make)
                    dictionary[hash_of_whole_table]['1/0']['images'].append(image)

                elif "DestinationID=1Class=1" in substring:
                    dictionary[hash_of_whole_table]['1/1']['val'] = substring
                    dictionary[hash_of_whole_table]['1/1']['models'].append(model)
                    dictionary[hash_of_whole_table]['1/1']['makes'].append(make)
                    dictionary[hash_of_whole_table]['1/1']['images'].append(image)

    return dictionary


myDict = makeDict("""TODO: enter path""")
print(myDict)

with open("""TODO: enter path""", 'a') as file:
    json.dump(myDict, file)

