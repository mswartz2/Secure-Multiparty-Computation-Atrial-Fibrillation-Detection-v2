from os import chdir, getcwd, path, listdir
import sys

sys.path.append(getcwd())

import pandas as pd
import numpy as np
import wfdb
from Data.SignalDataset import SignalDataset


def extract_cardiology_challenge_dataset(combine_training_and_vaidation_datasets=True):
    """
    Returns whole SignalDataset or original training and validation sets separetly
    Return:
        SignalDataset: if combine_training_and_vaidation_datasets
        [SignalDataset, SignalDataset]: if !combine_training_and_vaidation_datasets
    """

    training_labels_csv = (
        getcwd() + "\\Data\\Datasets\\CardiologyChallenge\\training\\REFERENCE-v3.csv"
    )
    validation_labels_csv = (
        getcwd() + "\\Data\\Datasets\\CardiologyChallenge\\validation\\REFERENCE-v3.csv"
    )
    Y_training_df = pd.read_csv(training_labels_csv, header=None)
    Y_validation_df = pd.read_csv(validation_labels_csv, header=None)

    training_labels, training_patient_ids = _get_labels_and_patient_ids(Y_training_df)
    validation_labels, validation_patient_ids = _get_labels_and_patient_ids(
        Y_validation_df
    )

    training_raw_data, validation_raw_data = _get_raw_data()

    training_signal_data_set = SignalDataset(
        training_raw_data, training_labels, training_patient_ids
    )
    validation_signal_data_set = SignalDataset(
        validation_raw_data, validation_labels, validation_patient_ids
    )
    both_signal_data_set = SignalDataset(
        training_raw_data + validation_raw_data,
        training_labels + validation_labels,
        training_patient_ids + validation_patient_ids,
    )

    if combine_training_and_vaidation_datasets:
        return both_signal_data_set
    else:
        return training_signal_data_set, validation_signal_data_set


def _get_labels_and_patient_ids(metadata_df):
    labels = np.zeros(len(metadata_df), dtype=int)
    patient_ids = np.empty(len(metadata_df), dtype="U25")

    # patient is the ecg_id - 1
    for i in range(len(metadata_df)):
        patient_ids[i] = metadata_df[0][i]  # patient ID

        if "A" == metadata_df[1][i]:
            # this patient has AF
            labels[i] = 1
        elif "N" == metadata_df[1][i]:
            # this record is normal
            labels[i] = 0
        elif "~" == metadata_df[1][i]:
            # this record is noisy
            labels[i] = 2
        else:
            # this patient isn't norm or AF or noisy
            labels[i] = -1

    # create empty numpy arr to hold only norm and AF records
    clean_labels = []
    clean_patient_ids = []

    # fill numpy arr
    i = 0
    for i in range(len(metadata_df)):
        if labels[i] in [0, 1]:  # AF or Norm
            clean_labels.append(labels[i])
            clean_patient_ids.append(patient_ids[i])

    return clean_labels, clean_patient_ids


def _get_files_list(parent_dir):
    files_list = []

    for f in listdir(parent_dir):
        # append signal file
        if path.isfile(path.join(parent_dir, f)):
            if f.endswith(".hea"):
                files_list.append(parent_dir + "\\" + f.split(".")[0])
        # get files from dirs
        elif path.isdir:
            files_list.extend(_get_files_list(parent_dir + "\\" + f))

    return files_list


def _get_raw_data():
    training_dir = getcwd() + "\\Data\\Datasets\\CardiologyChallenge\\training"
    validation_dir = getcwd() + "\\Data\\Datasets\\CardiologyChallenge\\training"

    training_files_list = _get_files_list(training_dir)
    validation_files_list = _get_files_list(validation_dir)

    training_raw_data = _extract_raw_data_from_WFDB_files(training_files_list)
    validation_raw_data = _extract_raw_data_from_WFDB_files(validation_files_list)

    return training_raw_data, validation_raw_data


def _extract_raw_data_from_WFDB_files(files_list):
    raw_signals_list = []
    for i in range(len(files_list)):
        current_record = files_list[i]
        sig, fields = wfdb.rdsamp(current_record)

        # make signal file 1D
        flattened_signal = sig.flatten()

        raw_signals_list.append(flattened_signal)

    return raw_signals_list
