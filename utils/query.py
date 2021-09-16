import numpy as np


ALL_HITS: int = 0
INNER_ONE: int = -1


def hashedDataset(
    query: np.array,
    hashedDataset: dict,
    amount: int = ALL_HITS,
    axis: int = INNER_ONE
) -> np.array:
    return dataset(
        query,
        hashedDataset.get(
            getHash(query),
            np.array([])
        ),
        amount=amount,
        axis=axis
    )


def dataset(
    query: np.array,
    dataset: np.array,
    amount: int = ALL_HITS,
    axis: int = INNER_ONE
) -> np.array:
    assert 2 == len(dataset.shape), f'Data shape {dataset.shape} should have only 2 dimentions'
    return dataset[np.argsort(np.sum((query - dataset)**2, axis=axis))[:_getNearestNeighborsAmount(dataset, amount)]]


def getHash(query: np.array) -> str:
    return str(np.array)


def _getNearestNeighborsAmount(dataset: np.array, amount: int):
    print(len(dataset))
    return amount if amount > ALL_HITS else len(dataset)
