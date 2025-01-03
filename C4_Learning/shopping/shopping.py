import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    month_2_number = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 
        'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 
        'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
    }

    visitor_2_number = {
        'New_Visitor':          0,
        'Returning_Visitor':    1
    }

    weekend_2_number = {
        'FALSE':   0,
        'TRUE':    1
    }

    evidence = []
    labels = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)

        for index, row in enumerate(reader):
            if index != 0:

                revenue = row.pop()
                if revenue == 'TRUE':
                    labels.append(1)
                else:
                    labels.append(0)

                evidence.append(
                    [
                    int(row[0]),
                    float(row[1]),
                    int(row[2]),
                    float(row[3]),
                    int(row[4]),
                    float(row[5]),
                    float(row[6]), #BounceRates, a floating point number
                    float(row[7]), #ExitRates, a floating point number
                    float(row[8]), #PageValues, a floating point number
                    float(row[9]), #SpecialDay, a floating point number
                    # .
                    int(month_2_number.get(row[10].capitalize(), None)), #Month, an index from 0 (January) to 11 (December)
                    int(row[11]), #OperatingSystems, an integer
                    int(row[12]), #Browser, an integer
                    int(row[13]), #Region, an integer
                    int(row[14]), #TrafficType, an integer
                    int(visitor_2_number.get(row[15], 0)), #VisitorType, an integer 0 (not returning) or 1 (returning)
                    int(weekend_2_number.get(row[16], None)) #Weekend, an integer 0 (if false) or 1 (if true)
                    ]
                )
    
    return(evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # x_train, x_test, y_train, y_test = train_test_split(
    #     evidence,
    #     labels,
    #     test_size=TEST_SIZE
    # )

    knn = KNeighborsClassifier(n_neighbors=1)
    # knn.fit(x_train, y_train)
    knn.fit(evidence, labels)
    # print(knn)
    return knn


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    actual_pos  = 0
    true_pos    = 0
    actual_neg  = 0
    true_neg    = 0
    
    for index, label in enumerate(labels):
        if label == 1:
            actual_pos += 1
            if predictions[index] == 1:
                true_pos += 1
        else:
            actual_neg += 1
            if predictions[index] == 0:
                true_neg += 1
    
    rate_pos = true_pos/actual_pos      #sensitivity 
    rate_neg = true_neg/actual_neg      #specificity 

    return(rate_pos, rate_neg)


if __name__ == "__main__":
    main()
