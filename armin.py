import sys
import csv
import collections

inputFile = sys.argv[1]
output = sys.argv[2]
min_perc = float(sys.argv[3])
min_conf = float(sys.argv[4])
tot = 0
content = []


def genRules(overall_dict, csvfile):
    rules = {}
    rulesA = []
    count = 0

    for index1, item1 in enumerate(overall_dict.keys()):
        for index2, item2 in enumerate(overall_dict.keys()):
            contain = False
            for i in item1:
                if i in item2:
                    contain = True
                    break
            if contain:  # at least one char in item1 is in item2
                continue
            else:
                test = set()
                for c in item1:
                    test.add(c)
                for c in item2:
                    test.add(c)
                test = sorted(test)
                phrase = ()
                for t in test:
                    phrase += (t,)
                if phrase in overall_dict.keys():
                    support_percentage = overall_dict[phrase][0]
                    conf = overall_dict[phrase][1] / overall_dict[item1][1]
                    if support_percentage >= min_perc and conf >= min_conf:
                        rulesA.append([])
                        rulesA[count].append(support_percentage)
                        rulesA[count].append(conf)
                        rulesA[count].append(item1)
                        rulesA[count].append(item2)
                        count += 1
                        csvfile.write('R,')
                        csvfile.write(str("%0.6f" % support_percentage))
                        csvfile.write(',')
                        csvfile.write(str("%0.6f" % conf))
                        csvfile.write(',')
                        for i in item1:
                            csvfile.write(str(i))
                            csvfile.write(',')
                        csvfile.write('\'=>\'')
                        csvfile.write(',')
                        for index, i in enumerate(item2):
                            csvfile.write(i)
                            if not index == len(item2) - 1:
                                csvfile.write(',')
                        csvfile.write('\n')

    return rules


def genCfIVfI(cfI, vfI, overall_dict):
    cfI = collections.OrderedDict(sorted(cfI.items()))
    vfI = {}
    rules = {}
    if cfI == {}:
        with open(inputFile) as csvfile:
            reader = csv.reader(csvfile)
            for itemset in reader:
                for index, i in enumerate(itemset):
                    itemset[index] = i.strip()
                content.append(itemset[1:len(itemset)])
                for key, item in enumerate(itemset):
                    if key > 0:
                        item = (item.strip(),)
                        print(item)
                        if not item in cfI:
                            cfI[item] = []
                            cfI[item].append(0)
                            cfI[item].append(1)
                        else:
                            cfI[item][1] += 1
            for key in cfI.keys():
                print(key)
                support_percentage = cfI[key][1] / len(content)
                cfI[key][0] = support_percentage
                if support_percentage >= min_perc:
                    vfI[key] = [support_percentage, cfI[key][1]]
    else:
        for key in cfI.keys():
            print(type(key))
            print(key, cfI[key][0])
            if cfI[key][0] >= min_perc:
                vfI[key] = [cfI[key][0], cfI[key][1]]
    return [cfI, vfI, rules]


def genLargeCfI(vfI, cfI):
    vfI = collections.OrderedDict(sorted(vfI.items()))
    cfI = collections.OrderedDict(sorted(cfI.items()))
    keys = list(vfI.keys())
    print(keys)
    if len(keys) < 2:
        return {}
    for i in range(len(keys)):
        for j in range(len(keys)):
            key1 = keys[i]
            key2 = keys[j]
            test = set()
            for item1 in key1:
                test.add(item1)
            for item2 in key2:
                test.add(item2)
            test = sorted(test)
            if len(test) == len(keys[0]) + 1:
                new_key = ()  # tuple
                support_count = 0
                for item in test:
                    new_key += (item,)
                cfI[new_key] = []

                for trans in content:
                    flag = True
                    for index, k in enumerate(new_key):
                        if not k in trans:
                            flag = False
                        if index == len(new_key) - 1:
                            if flag:
                                support_count += 1

                cfI[new_key].append(support_count / len(content))
                cfI[new_key].append(support_count)
    return cfI


def sendToOutput(mydict, csvfile):
    orderedDict = collections.OrderedDict(sorted(mydict.items()))
    for key, value in orderedDict.items():
        csvfile.write('S,')
        csvfile.write(str("%0.6f" % value[0]))
        csvfile.write(',')
        for idx in range(len(key)):
            csvfile.write(key[idx])
            if idx == len(key) - 1:
                csvfile.write('\n')
            else:
                csvfile.write(',')

index = 1
cfI = {}
vfI = {}
overall_dict = {}
with open(output, 'w') as csvfile:
    while True:
        [cfI, vfI, rules] = genCfIVfI(cfI, vfI, overall_dict)
        sendToOutput(vfI, csvfile)
        overall_dict = {**overall_dict, **vfI}

        cfI = {}
        cfI = genLargeCfI(vfI, cfI)

        if cfI == {}:
            break
        index += 1
    genRules(overall_dict, csvfile)