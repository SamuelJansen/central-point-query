from python_helper import log
from globals import newGlobalsInstance
globalsInstance = newGlobalsInstance(
    __file__,
    successStatus = True,
    errorStatus = True,
    infoStatus = True,
    # debugStatus = True,
    failureStatus = True
)
log.info(__name__, 'Importiong libraries')


import time
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from python_helper import Constant as c
from python_helper import RandomHelper, StringHelper, ObjectHelper

from utils import query as queryFrom
from utils.query import Dataset, HashedDataset, DatasetKeys


log.info(__name__, 'Libraries imported')


def plotSamples(data: np.array, target, samples: int = 1, shape: tuple = (28, 28)):
    """Plot the first 5 images and their labels in a row."""
    for index, (img, target) in enumerate(zip(data[:samples].reshape(tuple([samples, *list(shape)])), target[:samples])):
        plt.subplot(151 + index)
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.title(target)


def loadDataset(datasetName: str, dataType: str, targetType: str, cache: bool = False) -> Dataset:
    log.info(loadDataset, 'Loading dataset')
    originalDataset = fetch_openml(datasetName, cache=cache)
    dataset = Dataset(
        originalDataset.data.astype(dataType).values,
        originalDataset.target.astype(targetType)
    )
    log.debug(loadDataset, 'Dataset loaded')
    return dataset


def roundToInt(value):
    return int(round(value))


def resizeByAverage(dataset: Dataset, dataShape: tuple)-> Dataset:
    log.info(resizeByAverage, f'Resizing dataset to {dataShape} by avarege')
    return Dataset(
        resizeDataByAverage(dataset.data, dataShape),
        dataset.target
    )


def resizeDataByAverage(data: np.array, dataShape: tuple)-> Dataset:
    log.debug(resizeDataByAverage, f'Resizing data to {dataShape} by avarege')
    #TODO: actualy write this "flattenedData" thing
    flattenedData = [
        dataUnit for dataUnit in data
    ]
    stepSize = len(flattenedData[0]) / sum(dataShape)
    resized = np.asarray(
        [
            [
                np.mean(dataUnit[roundToInt(step * stepSize):]) if roundToInt((step+1) * stepSize) >= len(dataUnit) else np.mean(dataUnit[roundToInt(step * stepSize):roundToInt((step+1) * stepSize)]) for step in range(roundToInt(len(dataUnit) / stepSize))
            ] for dataUnit in flattenedData
        ]
    )
    log.debug(resizeDataByAverage, f'Original shape: {data.shape}')
    log.debug(resizeDataByAverage, f'Step size: {stepSize}')
    log.debug(resizeDataByAverage, f'Resized shape: {resized.shape}')
    return resized


def resizeSampleByAverage(query: np.array, displayShape: tuple) -> np.array:
    return resizeDataByAverage(
        np.asarray([query]),
        (np.product(np.asarray(displayShape)),)
    )[0]


def reshape(dataset: Dataset, shape: tuple, weigth: float = 1.0, displayShape: tuple = None) -> Dataset:
    log.info(reshape, f'Reshaping dataset to {shape}')
    reshapeDataset = None
    try:
        reshapeDataset = Dataset(
            dataset.data.reshape(*shape) * weigth,
            dataset.target,
            displayShape = displayShape
        )
    except Exception as exception:
        log.error(reshape, f'No possible to reshape {queryFrom.arrayToString(dataset.data)}', exception, muteStackTrace=True)
        raise exception
    reshapeDataset.displaySample()
    return reshapeDataset


def reduceShape(dataset: Dataset, shape: tuple) -> Dataset:
    return resizeByAverage(dataset, (np.product(np.asarray(shape)),))


def getHashedDataset(resampledMnist: Dataset, displayShape: tuple) -> dict:
    log.info(getHashedDataset, 'Building hashed dataset over central point')
    hashedDataset = HashedDataset(resampledMnist, displayShape)
    log.debug(getHashedDataset, f'hashedDataset keys length: {len(list(hashedDataset.get()[DatasetKeys.VALUES].keys()))}')
    log.debug(getHashedDataset, f'hashedDataset sampledDigit: {queryFrom.arrayToString(queryFrom.buildDatasetMean(RandomHelper.sample(list(hashedDataset.get().values()))[DatasetKeys.VALUES]), shape=displayShape)}')
    return hashedDataset


def mnist():
    mnistDataset = loadDataset('mnist_784', 'float32', 'int64')
    flattenMnist = reshape(mnistDataset, (-1, 784), weigth=1/255, displayShape=(28, 28))
    # reshapedMnist = reshape(mnistDataset, (-1, 28, 28), weigth=1/255, displayShape=(28, 28))
    reducedDisplaySchape = (3, 3)
    resampledMnist = reduceShape(flattenMnist, reducedDisplaySchape)
    reshapedResampledMnist = reshape(resampledMnist, (-1, *reducedDisplaySchape))
    hashedDataset = getHashedDataset(resampledMnist, reducedDisplaySchape)

    startedAt = time.time()
    log.info(mnist, f'Query started at {startedAt}')
    sampledIndex = RandomHelper.integer(minimum=0, maximum=flattenMnist.data.shape[0]-1)
    predictions = hashedDataset.query(resizeSampleByAverage(flattenMnist.data[sampledIndex], reducedDisplaySchape), 10)
    results = []
    for prediction in predictions:
        results.append(
            hashedDataset.get()[DatasetKeys.VALUES][
                queryFrom.arrayToString(
                    resizeSampleByAverage(prediction, hashedDataset.displayShape),
                    roundTo=2,
                    shape=hashedDataset.displayShape
                )
            ][DatasetKeys.TARGET]
        )
    log.success(mnist, f'Expected result: {flattenMnist.target[sampledIndex]}')
    log.success(mnist, f'Predicted result: {sorted(results, key=results.count, reverse=True)[0]}')
    finishedAt = time.time()
    log.info(mnist, f'Query finished at {finishedAt}')
    log.info(mnist, f'Query last {finishedAt - startedAt} seconds')


if __name__ == '__main__':
    mnist()
