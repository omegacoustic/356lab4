import sys, helper
from sklearn import tree
from sklearn.model_selection import train_test_split
import graphviz
from sklearn.metrics import confusion_matrix
import numpy as np
from datetime import datetime
# import random

def generate_sample_label(csvdir):
    samples = []
    labels = [] 

    sample_csv = open(csvdir, 'r')
    sample_csv.readline()

    for record in sample_csv:
        playerid, features, label = helper.turn_record_to_sample(record)
        samples.append(features)
        labels.append(label)

    sample_csv.close
    return samples, labels

def train_plus_test(iteration, csvdir, classifier_type):
    dataset = generate_sample_label(csvdir)
    np.random.seed(datetime.now().microsecond)
    x_train, x_test, y_train, y_test = train_test_split(dataset[0], dataset[1], test_size=0.2)

    # train
    clf = tree.DecisionTreeClassifier(criterion=classifier_type)
    clf = clf.fit(x_train, y_train)

    y_predict = clf.predict(x_test)
    conf_matrix = confusion_matrix(y_test, y_predict)
    tn, fp, fn, tp = conf_matrix.ravel()
    accuracy = (tp + tn) / (tn + fp + fn + tp)



    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render(classifier_type)

    # count = 0
    # true_pos = 0
    # false_pos = 0
    # true_neg = 0
    # false_neg = 0
    predictions = []

    # predict
    for test_sample in x_test:
        test_result = clf.predict([test_sample])
    #     if y_test[count]==1:
    #         if test_result[0]==1:
    #             true_pos += 1
    #         else:
    #             false_neg += 1
    #     else:
    #         if test_result[0]==1:
    #             true_neg += 1
    #         else:
    #             false_pos += 1
        predictions.append(test_result)
        # count += 1

    # recall = true_pos/(true_pos+false_pos)
    # precision = true_pos/(true_pos+false_neg)
    gen_recall = tp/(tp+fp)
    gen_precision = tp/(tp+fn)
    # print("True positives: {}".format(true_pos))
    # print("False positives: {}".format(false_pos))
    # print("True negatives: {}".format(true_neg))
    # print("False negatives: {}".format(false_neg))
    # print("calculated (recall, precision): ({}, {})".format(recall, precision))
    print("(accuracy, recall, precision): ({}, {}, {})".format(accuracy, gen_recall, gen_precision))

    helper.print_prediction(iteration, y_test, predictions, classifier_type)
  

    # return accuracy, conf_matrix, [true_pos, false_pos, true_neg, false_neg]
    return accuracy, conf_matrix, gen_recall, gen_precision

def multi_iterate(iteration, classifier_type, csvdir):
    out = open("g19_DT_"+classifier_type+"_predictions.csv", 'w')
    out.close

    accuracy = [0]*iteration
    total_stats = [0]*4
    recalls = [0]*iteration
    precisions = [0]*iteration
    for i in range(iteration):
        np.random.seed(123)
        confusion_matrices = {}
        accuracy[i],confusion_matrices["{0}-confusion-matrix-iteration-{1}".format(classifier_type, i)], recalls[i], precisions[i] = train_plus_test(i, csvdir, classifier_type)
    recall = sum(recalls)/iteration
    precision = sum(precisions)/iteration
    print("Total (recall, precision): ({}, {})".format(recall, precision))

    helper.print_accuracy(iteration, accuracy, classifier_type)
    helper.generate_metrics(confusion_matrices)
    print("Average accuracy: ", sum(accuracy)/iteration, "Source csv: ", csvdir)

if __name__ == "__main__":
    multi_iterate(iteration = int(sys.argv[1]), classifier_type = sys.argv[2], csvdir = sys.argv[3])
