from datetime import datetime
from AI.Response import dataset

def PatternUnderstanding(query):
    data_positivity = []
    data_negativity = []
    for question in dataset:
        question = list(question.keys())[0]
        length = len(question.split())
        negative = positive = 0
        for word in query.split():
            if word in question.split():
                positive += 1
            elif negative > length/2:
                break
            else:
                negative += 1
        data_positivity.append(positive)
        data_negativity.append(negative)

    try:
        Max_Value = max(data_positivity)
        if Max_Value >= len(query.split())/2:
            data_Index = list_duplicates_of(data_positivity, Max_Value)
            i = get_negative_value(data_negativity, data_Index)
            return dataset[i][list(dataset[i].keys())[0]]
        return False
    except:
        return False

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def get_negative_value(nega, indexes):
    min = 1000
    ind = 0
    for index in indexes:
        if nega[index]<min:
            min = nega[index]
            ind = index
    return ind


# print(list(dataset[0].keys())[0])
