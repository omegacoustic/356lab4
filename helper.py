# data helpers
def turn_record_to_sample(row_record):
    """turn every row record from csv file into a sample record"""
    elems = row_record.strip().split(',')
    for elem in elems:
        elem = elem.strip()

    samples = []



    #list of useless string
    gabage = ["NULL", "null", "\\N",""]

    for elem in elems[1:]:
        if elem in gabage:
            samples.append(-1)
        elif elem[0].isalpha():
            samples.append(-1)
        else:
            elem = elem.split(".")[0]
            samples.append(int(elem))

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
    content = ''

    if iteration == 0:
        content = "Iteration, Classification, Predictions\n"

    for i in range(len(classification)):
        content += str(iteration) + ", " + str(classification[i]) + ", " + str(prediction[i][0]) + ",\n"

    output.write(content)
    output.close

def generate_metrics(confusion_matrices):
    from matplotlib import pyplot as plt
    labels = ['', 'elected', 'nominee']
    for label, cm in confusion_matrices.items():
        fig, ax = plt.subplots()
        cax = ax.matshow(cm)
        plt.title(label)
        ax.set_xticklabels(labels)
        ax.set_yticklabels(labels)
        plt.xlabel('Predicted')
        plt.ylabel('Sampled')
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, cm[i, j], ha="center", va="center", color="black")
        fig.savefig(label + '.png')