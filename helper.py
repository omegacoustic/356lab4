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