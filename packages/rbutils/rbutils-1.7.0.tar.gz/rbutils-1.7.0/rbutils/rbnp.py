import numpy as np


def linspace_2d(x1, y1, x2, y2, num):
    X = np.linspace(x1, x2, num)
    Y = np.linspace(y1, y2, num)
    list = np.array([])
    for i in range(len(X)):
        list = np.append(list, [X[i], Y[i]])
    return list.reshape(-1, 2)


if __name__ == "__main__":
    # 本地测试使用
    ret = linspace_2d(1, 2, 3, 4, 51)
    print('test:', ret)
