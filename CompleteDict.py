import os
import hashlib
import json

# Table ready for hashing
def getWholeTableClipped(filePath):
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

# Ordinary table (with new lines etc...)
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
                    tables.append(line)
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

def extractor(string, requirement):

    t = string

    # Split lines

    lines = t.split("Codes of length")

    # Matrix of separate values
    lines2d = []

    for line in lines[1::]:
        line = line.replace('  ', '').replace('\n', '').replace('  ', ' ')
        ar = []
        if line.strip()[line.find(":")::] == '':
            ar.append('')
        else:
            list = (line[line.find(": ") + 2::].strip()).split(" ")
            for val in list:
                ar.append(int(val, 16))
        lines2d.append(ar)

    # Initialize three arrays
    minval = [0]*16
    maxval = [-1]*16
    valptr = [0] * 16

    # Initialize counter (valptr)
    ctr = 0

    # find valptrs
    for i, line in enumerate(lines[1::]):
        num = line[line.find("(") + 1:line.find(" tot")]
        if len(num) == 0 or num == '000':
            continue
        valptr[i] = ctr
        ctr += int(num)

    # Initialize counter (Min/Max val)
    p = 0

    # find Min/Max vals
    for i, line in enumerate(lines2d):
        if len(line)==1 and line[0]=='' and i != 0:
            p = p - 1
            p = p+1
            p = p*2
            continue
        if len(line)==1 and line[0]=='' and i == 0:
            continue
        minval[i]=p
        p=p+len(line)-1
        maxval[i]=p
        p=2*(p+1)

    # Find HuffVals of table
    huffvals = []
    for val in lines2d:
        for val2 in val:
            if  val2 != '':
                huffvals.append(val2)
            # else:
            #     huffvals.append(0)

    # Print output
    if requirement == 'valptr':
        return str(valptr)
    elif requirement == 'huffval':
        return str(huffvals)
    elif requirement == 'mincode':
        return str(minval)
    elif requirement == 'maxcode':
        return str(maxval)

def makeDict():
    dictionary = {}

    for file in os.listdir("/Users/Uni/Downloads/SIE1"):

        whole_table_clipped = getWholeTableClipped("/Users/Uni/Downloads/SIE1/" + file)
        whole_table = getWholeTable("/Users/Uni/Downloads/SIE1/" + file)
        hash_of_whole_table = hashlib.sha256(whole_table_clipped.encode()).hexdigest()

        huffvals = []
        mincodes = []
        maxcodes = []
        valptrs = []

        image = getFileName("/Users/Uni/Downloads/SIE1/" + file)
        model = getModel("/Users/Uni/Downloads/SIE1/" + file)
        make = getMake("/Users/Uni/Downloads/SIE1/" + file)

        if hash_of_whole_table not in dictionary:
            dictionary[hash_of_whole_table] = {}
            dictionary[hash_of_whole_table]['details'] = {}
            dictionary[hash_of_whole_table]['0/0']['huffvals'] = []
            dictionary[hash_of_whole_table]['0/0']['mincodes'] = []
            dictionary[hash_of_whole_table]['0/0']['maxcodes'] = []
            dictionary[hash_of_whole_table]['0/0']['valptrs'] = []

            dictionary[hash_of_whole_table]['0/1']['huffvals'] = []
            dictionary[hash_of_whole_table]['0/1']['mincodes'] = []
            dictionary[hash_of_whole_table]['0/1']['maxcodes'] = []
            dictionary[hash_of_whole_table]['0/1']['valptrs'] = []

            dictionary[hash_of_whole_table]['1/0']['huffvals'] = []
            dictionary[hash_of_whole_table]['1/0']['mincodes'] = []
            dictionary[hash_of_whole_table]['1/0']['maxcodes'] = []
            dictionary[hash_of_whole_table]['1/0']['valptrs'] = []

            dictionary[hash_of_whole_table]['1/1']['huffvals'] = []
            dictionary[hash_of_whole_table]['1/1']['mincodes'] = []
            dictionary[hash_of_whole_table]['1/1']['maxcodes'] = []
            dictionary[hash_of_whole_table]['1/1']['valptrs'] = []

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

            dictionary[hash_of_whole_table]['whole'] = whole_table_clipped


        dictionary[hash_of_whole_table]['details']['models'].append(model)
        dictionary[hash_of_whole_table]['details']['makes'].append(make)
        dictionary[hash_of_whole_table]['details']['images'].append(image)

        for val in whole_table.split('----')[1::]:
            val = val.strip()
            if '''Destination ID = 0
        Class = 0 (DC / Lossless Table)''' in val:
                # TODO - Need to find a way to add huffval, mincode, valptr, and maxcode to dict...


        for substring in whole_table_clipped.split("----"):
            print(substring)
            if len(substring) > 0:
                if "DestinationID=0Class=0" in substring:
                    dictionary[hash_of_whole_table]['huffvals'].append(extractor(substring, 'huffval'))
                    dictionary[hash_of_whole_table]['mincodes'].append(extractor(substring, 'mincode'))
                    dictionary[hash_of_whole_table]['maxcodes'].append(extractor(substring, 'maxcode'))
                    dictionary[hash_of_whole_table]['valptrs'].append(extractor(substring, 'valptr'))

                    dictionary[hash_of_whole_table]['0/0']['val'] = substring
                    dictionary[hash_of_whole_table]['0/0']['models'].append(model)
                    dictionary[hash_of_whole_table]['0/0']['makes'].append(make)
                    dictionary[hash_of_whole_table]['0/0']['images'].append(image)

                elif "DestinationID=0Class=1" in substring:
                    dictionary[hash_of_whole_table]['huffvals'].append(extractor(substring, 'huffval'))
                    dictionary[hash_of_whole_table]['mincodes'].append(extractor(substring, 'mincode'))
                    dictionary[hash_of_whole_table]['maxcodes'].append(extractor(substring, 'maxcode'))
                    dictionary[hash_of_whole_table]['valptrs'].append(extractor(substring, 'valptr'))

                    dictionary[hash_of_whole_table]['0/1']['val'] = substring
                    dictionary[hash_of_whole_table]['0/1']['models'].append(model)
                    dictionary[hash_of_whole_table]['0/1']['makes'].append(make)
                    dictionary[hash_of_whole_table]['0/1']['images'].append(image)

                elif "DestinationID=1Class=0" in substring:
                    dictionary[hash_of_whole_table]['huffvals'].append(extractor(substring, 'huffval'))
                    dictionary[hash_of_whole_table]['mincodes'].append(extractor(substring, 'mincode'))
                    dictionary[hash_of_whole_table]['maxcodes'].append(extractor(substring, 'maxcode'))
                    dictionary[hash_of_whole_table]['valptrs'].append(extractor(substring, 'valptr'))

                    dictionary[hash_of_whole_table]['1/0']['val'] = substring
                    dictionary[hash_of_whole_table]['1/0']['models'].append(model)
                    dictionary[hash_of_whole_table]['1/0']['makes'].append(make)
                    dictionary[hash_of_whole_table]['1/0']['images'].append(image)

                elif "DestinationID=1Class=1" in substring:
                    dictionary[hash_of_whole_table]['huffvals'].append(extractor(substring, 'huffval'))
                    dictionary[hash_of_whole_table]['mincodes'].append(extractor(substring, 'mincode'))
                    dictionary[hash_of_whole_table]['maxcodes'].append(extractor(substring, 'maxcode'))
                    dictionary[hash_of_whole_table]['valptrs'].append(extractor(substring, 'valptr'))

                    dictionary[hash_of_whole_table]['1/1']['val'] = substring
                    dictionary[hash_of_whole_table]['1/1']['models'].append(model)
                    dictionary[hash_of_whole_table]['1/1']['makes'].append(make)
                    dictionary[hash_of_whole_table]['1/1']['images'].append(image)

    return dictionary


myDict = makeDict()
print(myDict)

# with open("/Users/Uni/PycharmProjects/QCRI2/newestDict2.json", "a") as file:
#     json.dump(myDict, file)


