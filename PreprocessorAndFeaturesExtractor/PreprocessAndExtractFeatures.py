# based on example code from Sebastian Goodfellow
import numpy as np
from biosppy.signals import ecg
from biosppy.signals.tools import filter_signal
import pandas as pd
import scipy as sp


def preprocess_and_extract_features_multiple_signals(raw_data, sample_rate):
    features_multiple_signals = []
    for i in range(len(raw_data)):
        features_one_signal = preprocess_and_extract_features_one_signal(
            raw_data[i], sample_rate
        )
        if not features_one_signal == False:
            # remove signals that were too noisy
            features_multiple_signals.append(features_one_signal)

    return features_multiple_signals


def preprocess_and_extract_features_one_signal(signal, sample_rate):
    (
        ts,
        signal_raw,
        signal_filtered,
        rpeaks,
        templates_ts,
        templates,
    ) = _pre_process_signal(signal, sample_rate)

    signal_features = _extract_features(
        sample_rate, ts, signal_filtered, rpeaks, templates_ts, templates
    )

    return signal_features


def _extract_templates(signal, sample_rate, rpeaks, before, after):

    # convert delimiters to samples
    before = int(before * sample_rate)
    after = int(after * sample_rate)

    # Sort R-Peaks in ascending order
    rpeaks = np.sort(rpeaks)

    # Get number of sample points in waveform
    length = len(signal)

    # Create empty list for templates
    templates = []

    # Create empty list for new rpeaks that match templates dimension
    rpeaks_new = np.empty(0, dtype=int)

    # Loop through R-Peaks
    for rpeak in rpeaks:

        # Before R-Peak
        a = rpeak - before
        if a < 0:
            continue

        # After R-Peak
        b = rpeak + after
        if b > length:
            break

        # Append template list
        templates.append(signal[a:b])

        # Append new rpeaks list
        rpeaks_new = np.append(rpeaks_new, rpeak)

    # Convert list to numpy array
    templates = np.array(templates).T

    return templates, rpeaks_new


def _apply_filter(signal, sample_rate, filter_bandwidth):

    # Calculate filter order
    order = int(0.3 * sample_rate)

    # Filter signal
    signal, _, _ = filter_signal(
        signal=signal,
        ftype="FIR",
        band="bandpass",
        order=order,
        frequency=filter_bandwidth,
        sampling_rate=sample_rate,
    )

    return signal


def _pre_process_signal(
    signal_raw,
    sample_rate,
    filter_bandwidth=[3, 45],
    normalize=True,
    polarity_check=True,
    template_before=0.2,
    template_after=0.4,
):

    # Filter signal
    signal_filtered = _apply_filter(signal_raw, sample_rate, filter_bandwidth)

    # Get BioSPPy ECG object
    ecg_object = ecg.ecg(signal=signal_raw, sampling_rate=sample_rate, show=False)

    # Get BioSPPy output
    ts = ecg_object["ts"]  # Signal time array
    rpeaks = ecg_object["rpeaks"]  # rpeak indices

    # Get templates and template time array
    templates, rpeaks = _extract_templates(
        signal_filtered, sample_rate, rpeaks, template_before, template_after
    )
    templates_ts = np.linspace(
        -template_before, template_after, templates.shape[1], endpoint=False
    )

    # Polarity check
    if polarity_check:

        # Get extremes of median templates
        templates_min = np.min(np.median(templates, axis=1))
        templates_max = np.max(np.median(templates, axis=1))

        if np.abs(templates_min) > np.abs(templates_max):

            # Flip polarity
            signal_raw *= -1
            signal_filtered *= -1
            templates *= -1

    # Normalize waveform
    if normalize:

        # Get median templates max
        templates_max = np.max(np.median(templates, axis=1))

        # Normalize ECG signals
        signal_raw /= templates_max
        signal_filtered /= templates_max
        templates /= templates_max

    return ts, signal_raw, signal_filtered, rpeaks, templates_ts, templates


def _extract_waveform_stats():
    # can add to later to improve accuracy
    stats = []

    return stats


def _extract_template_stats():
    # can add to later to improve accuracy
    stats = []

    return stats


def _extract_hrv_stats(rpeaks, sample_rate):
    stats = []

    # RRI
    rri = np.diff(rpeaks) * 1 / sample_rate
    rri_ts = rpeaks[0:-1] / sample_rate + rri / 2

    # RRI Velocity
    diff_rri = np.diff(rri)
    diff_rri_ts = rri_ts[0:-1] + diff_rri / 2

    # RRI Acceleration
    diff2_rri = np.diff(diff_rri)
    diff2_rri_ts = diff_rri_ts[0:-1] + diff2_rri / 2

    # compute heart rate
    heart_rate_ts = rri_ts
    heart_rate = 60.0 / rri

    # Calculate basic statistics
    if len(heart_rate) > 0:
        heart_rate_min = np.min(heart_rate)
        heart_rate_max = np.max(heart_rate)
        heart_rate_mean = np.mean(heart_rate)
        heart_rate_median = np.median(heart_rate)
        heart_rate_std = np.std(heart_rate, ddof=1)
        heart_rate_skew = sp.stats.skew(heart_rate)
        heart_rate_kurtosis = sp.stats.kurtosis(heart_rate)

        stats.extend(
            [
                heart_rate_min,
                heart_rate_max,
                heart_rate_mean,
                heart_rate_median,
                heart_rate_std,
                heart_rate_skew,
                heart_rate_kurtosis,
            ]
        )
    else:
        # signal is too noisy, exclude it from the data set
        stats.extend(False)

    return stats


def _extract_features(
    sample_rate,
    ts,
    signal_filtered,
    rpeaks,
    templates_ts,
    templates,
    template_before=0.2,
    template_after=0.4,
):

    features = _extract_hrv_stats(rpeaks, sample_rate)

    return features
