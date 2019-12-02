import sys, helper
from sklearn import tree
from sklearn.model_selection import train_test_split
import graphviz


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
    x_train, x_test, y_train, y_test = train_test_split(dataset[0], dataset[1], test_size=0.2)

    # train
    clf = tree.DecisionTreeClassifier(criterion=classifier_type)
    clf = clf.fit(x_train, y_train)


    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render(classifier_type)

    count = 0
    correct = 0
    predictions = []

    # predict
    for test_sample in x_test:
        print(test_sample)
        test_result = clf.predict([test_sample])
        if test_result[0] ==  y_test[count]:
            correct += 1
        predictions.append(test_result)
        count += 1
    
    helper.print_prediction(iteration, y_test, predictions, classifier_type)
  
    accuracy = (correct/count)*100
    return accuracy

def multi_iterate(iteration, classifier_type, csvdir):
    out = open("g19_DT_"+classifier_type+"_predictions.csv", 'w')
    out.close

    accuracy = [0]*iteration
    for i in range(iteration):
        accuracy[i] = train_plus_test(i, csvdir, classifier_type)

    helper.print_accuracy(iteration, accuracy, classifier_type)
    print("Average accuracy: ", sum(accuracy)/iteration, "Source csv: ", csvdir)

if __name__ == "__main__":
    multi_iterate(iteration = int(sys.argv[1]), classifier_type = sys.argv[2], csvdir = sys.argv[3])

# import os.path
# import sys
# import graphviz 

# from tqdm import tqdm
# from sklearn import tree
# from sklearn.model_selection import train_test_split

# import helper as hp

# def generate_sample_label(csvLocation):
#     samples = []
#     labels = []

#     samples_csv = open(csvLocation, 'r')
#     samples_csv.readline()

#     for entry in samples_csv:
#         playerId, features, label = hp.turn_record_to_sample(entry)

#         samples.append(features)
#         labels.append(label)

#     samples_csv.close
#     return samples, labels

# def train_and_test_on_data(iteration, csvlocation, classifier_type):
#     dataset = generate_sample_label(csvlocation)
#     x_train, x_test, y_train, y_test = train_test_split(dataset[0], dataset[1], test_size=0.2)

#     # training
#     clf = tree.DecisionTreeClassifier(criterion=classifier_type)
#     clf = clf.fit(x_train, y_train)

#     dot_data = tree.export_graphviz(clf, out_file=None) 
#     graph = graphviz.Source(dot_data) 
#     graph.render("out/"+classifier_type+"_"+os.path.splitext(csvlocation)[0]) 

#     cnt = 0
#     correct = 0
#     predictions = []
#     # predicting
#     for test_sample in x_test:
#         test_result = clf.predict([test_sample])
#         if test_result[0] ==  y_test[cnt]:
#             correct += 1
#         predictions.append(test_result)
#         cnt += 1
    
#     hp.print_prediction(iteration, y_test, predictions, classifier_type)

    
    
#     accuracy = (correct/cnt)*100
#     #print("Total: ", cnt, "Correct: ", correct, "Accuracy: ", accuracy)

#     return accuracy

# def multiple_data_set(iteration, classifier_type, csv_location):
#     accuracy = [0]*iteration

#     out = open("out/g14_DT_"+classifier_type+"_precision.csv", 'w')
#     out.close

#     for i in tqdm(range(iteration)):
#         accuracy[i] = train_and_test_on_data(i, csv_location, classifier_type)

#     hp.print_accuracy(iteration, accuracy, classifier_type)
#     print("Avg: ", sum(accuracy)/iteration, "CSV: ", csv_location)

# if __name__ == "__main__":
#     #python3 scikit_learn.py 5 entropy data2_7.csv
#     #python3 scikit_learn.py 5 gini data2_7.csv
    
#     i = int(sys.argv[1])
#     multiple_data_set(iteration = i, classifier_type = sys.argv[2], csv_location = sys.argv[3])