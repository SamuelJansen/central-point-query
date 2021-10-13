import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from utils import query as queryFrom


mnist = fetch_openml('mnist_784', cache=False)


def example():
    # dataset = np.asarray(
    #     [
    #         [1,2,3,4],
    #         [2,3,4,5],
    #         [3,4,5,6]
    #     ]
    # )
    # queries = np.asarray(
    #     [
    #         [1,2,3,4],
    #         [2,3,4,5],
    #         [3,4,5,6]
    #     ]
    # )
    # print('\n\n'+3*'========================')
    # print('FULL QUERIES')
    # for query in queries:
    #     print(f'\n\nquery:\n{query}\n\nfrom dataset:\n{dataset}\n\nhits:\n{queryFrom.dataset(query, dataset)}')
    # print('\n\n'+3*'========================')
    # print('NEAREST HIT QUERIES -> axis: -1')
    # for query in queries:
    #     print(f'\n\nquery:\n{query}\n\nfrom dataset:\n{dataset}\n\nhits:\n{queryFrom.dataset(query, dataset, amount=1)}')
    # print('\n\n'+3*'========================')
    # axis = 1
    # print(f'NEAREST HIT QUERIES -> axis: {axis}')
    # for query in queries:
    #     print(f'\n\nquery:\n{query}\n\nfrom dataset:\n{dataset}\n\nhits:\n{queryFrom.dataset(query, dataset, amount=1, axis=axis)}')

if __name__ == '__main__':
    example()
