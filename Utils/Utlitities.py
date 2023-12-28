def getDiagnosisText(diagnosis):
    diagnosisText = ""

    if diagnosis == 0:
        diagnosisText = "NORM"
    elif diagnosis == 1:
        diagnosisText = "AF"
    elif diagnosis == 2:
        diagnosisText = "NOISY"
    else:
        diagnosisText = "OTHER"

    return diagnosisText


def plotOneSingleLeadECGSignal(
    data, signalName, diagnosis, sampleRate, saveRec, saveDir=""
):
    """saveRec is a boolean field, if True, put where to save the file in saveDir"""

    diagnosisText = getDiagnosisText(diagnosis)
    plotTitle = f"ECG Signal - Patient {signalName} - {diagnosisText} - Sample Rate: {sampleRate} Hz"


def getIdsToVisualize(labelsMetaDataArr, numRecs):
    """Returns numRecs # of signals for nosiy, af, and norm records
    The returned values are just a list of the IDs (not other metadata)"""
    normIds = []
    afIds = []
    noisyIds = []
    i = 0
    while len(normIds) < numRecs or len(afIds) < numRecs or len(noisyIds) < numRecs:
        currentRecType = labelsMetaDataArr[i][1]
        if currentRecType == 0 and len(normIds) < numRecs:
            normIds.append(labelsMetaDataArr[i][0])  # append the signal filepath
        elif currentRecType == 1 and len(afIds) < numRecs:
            afIds.append(labelsMetaDataArr[i][0])  # append the signal filepath
        elif currentRecType == 2 and len(noisyIds) < numRecs:
            noisyIds.append(labelsMetaDataArr[i][0])  # append the signal filepath

        i += 1
        if i == len(labelsMetaDataArr):
            break
    return normIds, afIds, noisyIds
