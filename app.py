import numpy as np
from utils import query as queryFrom

def example():
    dataset = np.asarray(
        [
            [1,2,3,4],
            [2,3,4,5],
            [3,4,5,6]
        ]
    )
    queries = np.asarray(
        [
            [1,2,3,4],
            [2,3,4,5],
            [3,4,5,6]
        ]
    )
    print('\n\n'+3*'========================')
    print('FULL QUERIES')
    for query in queries:
        print(f'\n\nquery:\n{query}\n\nfrom dataset:\n{dataset}\n\nhits:\n{queryFrom.dataset(query, dataset)}')
    print('\n\n'+3*'========================')
    print('NEAREST HIT QUERIES -> axis: -1')
    for query in queries:
        print(f'\n\nquery:\n{query}\n\nfrom dataset:\n{dataset}\n\nhits:\n{queryFrom.dataset(query, dataset, amount=1)}')
    print('\n\n'+3*'========================')
    axis = 1
    print(f'NEAREST HIT QUERIES -> axis: {axis}')
    for query in queries:
        print(f'\n\nquery:\n{query}\n\nfrom dataset:\n{dataset}\n\nhits:\n{queryFrom.dataset(query, dataset, amount=1, axis=axis)}')


    # dataset = np.asarray(
    #     [
    #         [
    #             [1,2,3,5],
    #             [2,3,4,6],
    #             [3,4,5,7]
    #         ],
    #         [
    #             [2,2,3,6],
    #             [3,3,4,7],
    #             [4,4,5,8]
    #         ],
    #         [
    #             [3,2,3,7],
    #             [4,3,4,8],
    #             [5,4,5,9]
    #         ],
    #         [
    #             [9,2,3,7],
    #             [9,3,4,8],
    #             [9,4,5,9]
    #         ]
    #     ]
    # )
    # queries = np.asarray(
    #     [
    #         [1,2,3,4],
    #         [2,3,4,5],
    #         [5,4,5,9]
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
    # axis = 2
    # print(f'NEAREST HIT QUERIES -> axis: {axis}')
    # for query in queries:
    #     print(f'\n\nquery:\n{query}\n\nfrom dataset:\n{dataset}\n\nhits:\n{queryFrom.dataset(query, dataset, amount=1, axis=axis)}')

if __name__ == '__main__':
    example()

    # import numpy as np
    # from scipy import spatial
    #
    # xy1 = np.array(
    #     [[243,  3173],
    #      [525,  2997]])
    #
    # xy2 = np.array(
    #     [[682, 2644],
    #      [277, 2651],
    #      [396, 2640]])
    #
    # # This solution is optimal when xy2 is very large
    # tree = spatial.cKDTree(xy2)
    # mindist, minid = tree.query(xy1)
    # print(mindist)
    #
    # # This solution by @denis is OK for small xy2
    # mindist = np.min(spatial.distance.cdist(xy1, xy2), axis=1)
    # print(mindist)
