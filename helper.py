# clean data helpers
def clean(input_list):
    """get rid of ' ' in every field for a sample record"""
    l = []
    for elem in input_list:
        l.append(elem.strip())

    return l

def get_leagueid_identifier():
    """transform league id into numbers"""
    return {"UA":1,"AL":2,"NL":3,"PL":4,"NA":5,"AA":6,"FL":7}


def turn_record_to_sample(row_record):
    """turn every row record from csv file into a sample record"""
    elems = row_record.strip().split(',')
    elems = clean(elems)
    samples = []
    leagueid_dict = get_leagueid_identifier()

    for x in elems[1:]:
        if x == "NULL" or x == "null" or x == "":
            samples.append(-1)
        elif not x.isdigit():
            samples.append(leagueid_dict.get(x, -1))
        else:
            samples.append(int(x))

    #return playerid, features, label
    return samples[0], samples[1:-1], samples[-1]

# csv helpers
def print_accuracy(iteration, accuracy, classification_type):
    output = open("g19_DT_"+classification_type+"_accuracy.csv", 'w')
    content = "Dataset number, Accuracy,\n"

    i=0
    if iteration == len(accuracy):
        for a in accuracy:
            content += str(i) + ", " + str(a) + ",\n"
            i += 1

        output.write(content)
        output.close

def print_prediction(iteration, classification, prediction, classification_type):
    output = open("g19_DT_"+classification_type+"_predictions.csv", 'a')
    content = ""

    if iteration == 0:
        content = "Iteration, Classification, Predictions\n"
    for i in range(len(classification)):
        content += str(iteration) + ", " + str(classification[i]) + ", " + str(prediction[u][0]) + ",\n"

    output.write(content)
    output.close