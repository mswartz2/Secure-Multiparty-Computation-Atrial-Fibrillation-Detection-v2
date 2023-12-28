from os import chdir, getcwd
import sys

sys.path.append(getcwd())

from Utils import PickleFileUtils
from PreprocessorAndFeaturesExtractor import PreprocessAndExtractFeatures
from Data.SignalDataset import SignalDataset
from Logger import Log

# read in raw data pickles
raw_data_pickles_folder = getcwd() + "\\Data\\PickleFiles\\CardiologyChallenge\\Raw\\"

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
        original_training_data_set.raw_data, sample_rate
    )
)
original_validation_data_features = (
    PreprocessAndExtractFeatures.preprocess_and_extract_features_multiple_signals(
        original_validation_data_set.raw_data, sample_rate
    )
)

complete_data_set_features = (
    original_training_data_features + original_validation_data_features
)


# write features to pickle files
save_data_folder = getcwd() + "\\Data\\PickleFiles\\CardiologyChallenge\\Features\\"

PickleFileUtils.write_to_pickle_file(
    complete_data_set_features, save_data_folder + "CompleteDataSetFeatures.pickle"
)
PickleFileUtils.write_to_pickle_file(
    original_training_data_features,
    save_data_folder + "OriginalTrainingDataSetFeatures.pickle",
)
PickleFileUtils.write_to_pickle_file(
    original_validation_data_features,
    save_data_folder + "OriginalValidationDataSetFeatures.pickle",
)
