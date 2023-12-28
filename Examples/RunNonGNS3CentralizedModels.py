from os import chdir, getcwd
import sys

sys.path.append(getcwd())

from Utils import PickleFileUtils
from PreprocessorAndFeaturesExtractor import PreprocessAndExtractFeatures
from Data.SignalDataset import SignalDataset
from Logger import Log

# read in raw data pickles
raw_data_pickles_folder = getcwd() + "\\Data\\PickleFiles\\CardiologyChallenge\\"

complete_data_set = PickleFileUtils.read_in_pickle_file(
    raw_data_pickles_folder + "CompleteDataSet.pickle"
)
original_training_data_set = PickleFileUtils.read_in_pickle_file(
    raw_data_pickles_folder + "OriginalTrainingDataSet.pickle"
)
original_validation_data_set = PickleFileUtils.read_in_pickle_file(
    raw_data_pickles_folder + "OriginalValidationDataSet.pickle"
)

sample_rate = 300

# preprocess signals and features extraction
original_training_data_features = (
    PreprocessAndExtractFeatures.preprocess_and_extract_features_multiple_signals(
        sample_rate, original_training_data_set.raw_data
    )
)
original_validation_data_features = (
    PreprocessAndExtractFeatures.preprocess_and_extract_features_multiple_signals(
        sample_rate, original_validation_data_set.raw_data
    )
)

compete_data_set_features = (
    original_training_data_features + original_validation_data_features
)

# machine learning
