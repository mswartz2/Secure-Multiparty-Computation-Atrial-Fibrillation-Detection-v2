from sklearn.model_selection import train_test_split
import random
import logging


# DESCRIPTION:  Splits the dataset into a training and test sets.
# INPUTS:   (a) data - full dataset values
#           (b) labels - dataset labels
#           (c) train_size - a value indicating the percentage of the train size over the entire dataset
#           (c) test_size - a value indicating the percentage of the test size over the entire dataset
#           (d) new_split - a boolean value indicating whether a different split is to be returned
# RETURNS:  (a) X_train - a numpy array with the values of resulting training set
#           (b) X_test - a numpy array with the values of the resulting test set
#           (c) y_train - a numpy array with the labels of the resulting training set
#           (d) y_test - a numpy array withe the labels of the resulting test set
# NOTES: test_size is should be a value between 0 and 1;
def random_split_dataset(data, labels, train_size, test_size, new_split=True):

    logging.info("splitDataset: Splitting the dataset into training and test sets")
    logging.debug("Argument folder_paths_list: %s", data)
    logging.debug("Argument file_types_list: %s", labels)
    logging.debug("Argument file_types_list: %s", test_size)

    seed = 400
    if new_split in [True, "True", 1]:
        seed = random.randint(0, 1000)
    X_train, X_test, y_train, y_test = train_test_split(
        data, labels, train_size=train_size, test_size=test_size, random_state=seed
    )

    logging.debug("Return value X_train dimensions: %s", X_train)
    logging.debug("Return value X_test dimensions: %s", X_test)
    logging.debug("Return value y_train dimensions: %s", y_train)
    logging.debug("Return value y_test dimensions: %s", y_test)

    return X_train, X_test, y_train, y_test
