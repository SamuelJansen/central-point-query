import numpy as np

from python_helper import Constant as c
from python_helper import log, RandomHelper, StringHelper, ObjectHelper

ALL_HITS: int = 0
INNER_ONE: int = -1


class DatasetKeys:
    DATASET_MEAN = 'datasetMean'
    VALUES = 'values'
    DATA = 'data'
    TARGET = 'target'


class Dataset:

    def __init__(self, data: np.array, target: np.array, displayShape: tuple = None):
        self.data: np.array = data
        self.target: np.array = target
        self.displayShape: tuple = displayShape
        log.debug(self.__init__, f'data.shape: {self.data.shape}')
        log.debug(self.__init__, f'target.shape: {self.target.shape}')
        log.debug(self.__init__,  f'data.min: {self.data.min()}, data.max: {self.data.max()}')
        log.debug(self.__init__,  f'target.min: {self.target.min()}, target.max: {self.target.max()}')

    def displaySample(self):
        sampledIndex = RandomHelper.integer(minimum=0, maximum=self.data.shape[0]-1)
        log.debug(self.displaySample, f'data sampled: {arrayToString(self.data[sampledIndex], shape=self.displayShape)}')
        log.debug(self.displaySample, f'respective target: {self.target[sampledIndex]}')


class HashedDataset:

    def __init__(self, dataset: Dataset, displayShape: tuple):
        self.dataset = {
            DatasetKeys.DATASET_MEAN: buildDatasetMean(dataset.data),
            DatasetKeys.VALUES: {}
        }
        self.displayShape = displayShape
        self.add(dataset)

    def get(self):
        return self.dataset

    def getDatasetMean(self):
        return self.dataset.get(DatasetKeys.DATASET_MEAN)

    def add(self, dataset: Dataset):
        for index, sample in enumerate(dataset.data):
            self.append(index, sample, dataset)

    def append(self, index: int, sample: np.array, dataset: Dataset):
        hash = getDatasetMeanHash(sample, self.getDatasetMean())
        if not hash in self.dataset:
            self.dataset[hash] = {
                DatasetKeys.VALUES: np.array([sample])
            }
        else :
            self.dataset[hash][DatasetKeys.VALUES] = appendArray(self.dataset[hash][DatasetKeys.VALUES], sample)
        self.dataset[DatasetKeys.VALUES][arrayToString(sample, shape=self.displayShape)] = {
            DatasetKeys.DATA: sample,
            DatasetKeys.TARGET: dataset.target[index]
        }

    def query(self, query: np.array, amount: int = ALL_HITS, axis: int = INNER_ONE) -> np.array:
        return queryFromDataset(
            query,
            self.dataset.get(
                getDatasetMeanHash(query, self.getDatasetMean())
            ).get(DatasetKeys.VALUES),
            amount=amount,
            axis=axis
        )


def queryFromDataset(query: np.array, dataset: np.array, amount: int = ALL_HITS, axis: int = INNER_ONE) -> np.array:
    assert 2 == len(dataset.shape), f'Data shape {dataset.shape} should have only 2 dimentions'
    return dataset[np.argsort(np.sum((query - dataset)**2, axis=axis))[:_getAmount(dataset, amount)]]


def arrayToString(data: np.array, roundTo: int = 2, shape: tuple = None, title: str = c.BLANK):
    log.log(arrayToString, f'initial data.shape: {data.shape}')
    if ObjectHelper.isNotNone(shape) and not shape == data.shape:
        try:
            data = data.reshape(shape)
        except Exception as exception:
            log.error(arrayToString, f'Not possible to reshape {c.NEW_LINE}{data} of shape {data.shape} into shape {shape}', exception, muteStackTrace=True)
            raise exception
    log.log(arrayToString, f'data.shape: {data.shape}')
    if 2 <= len(data.shape):
        return StringHelper.join(
            [
                title,
                *[
                    StringHelper.join(
                        [
                            f'{str(int(round((10**roundTo) * round(value, roundTo)))).center(roundTo+1)}' for value in line
                        ],
                        character=c.BLANK
                    ) for line in data
                ]
            ],
            character=c.NEW_LINE
        )
    else:
        return StringHelper.join(
            [
                title,
                str(data)
            ],
            character=c.NEW_LINE
        )


def buildDatasetMean(data: np.array, displayShape: tuple = None) -> np.array:
    log.info(buildDatasetMean, 'Calculating data mean')
    # centralPoint = np.mean(flattenMnist.data, axis=0)
    if 1 == len(data.shape):
        return data
    dataMean = None
    try:
        dataMean = np.mean(data, axis=0)
    except Exception as exception:
        log.failure(buildDatasetMean, 'No possible to evaluate np.mean(data, axis=0). Going for a splicit approach')
        for index, dataElement in enumerate(list(data)):
            if ObjectHelper.isNone(dataMean):
                dataMean = dataElement
            else:
                dataMean += (dataElement - dataMean) / index
    log.debug(buildDatasetMean, f'Data mean: {arrayToString(dataMean, shape=displayShape)}')
    return dataMean


def getDatasetMeanHash(query: np.array, centralPoint: np.array) -> str:
    if ObjectHelper.isNone(centralPoint):
        raise Exception('Central point cannot be null')
    try:
        return str([1 if v else 0 for v in query > centralPoint])
    except Exception as exception:
        log.error(getDatasetMeanHash, f'not possible to compare: {query} with {centralPoint}', exception, muteStackTrace=True)
        raise exception


def appendArray(array: np.array, arrayToAppend: np.array) -> np.array:
    return np.append(array, [arrayToAppend], axis=0)


def _getAmount(dataset: np.array, amount: int):
    return amount if amount > ALL_HITS else len(dataset)
