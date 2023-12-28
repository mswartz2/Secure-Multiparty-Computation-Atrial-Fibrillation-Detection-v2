from os import chdir, getcwd
import sys

sys.path.append(getcwd())

from Utils import PickleFileUtils

# DESCRIPTION:
# INPUTS:
# RETURNS:
# NOTES:

# Read in raw data pickles
raw_data_pickles_folder = getcwd() + "\\Data\\PickleFiles\\CardiologyChallenge\\Raw\\"

complete_signal_data_set = PickleFileUtils.read_in_pickle_file(
    raw_data_pickles_folder + "CompleteDataSet.pickle"
)
original_training_data_set = PickleFileUtils.read_in_pickle_file(
    raw_data_pickles_folder + "OriginalTrainingDataSet.pickle"
)
original_validation_data_set = PickleFileUtils.read_in_pickle_file(
    raw_data_pickles_folder + "OriginalValidationDataSet.pickle"
)


# Cut shuffled data in to 10 folds
folds = []

# Save 10 folds

# Train 10 models
# fold_n is the testing fold, exclude it from model training
for fold_n in folds:
    # train model

    # save model

    pass
