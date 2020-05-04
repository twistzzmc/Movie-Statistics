import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    # plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    #          [29772, 6995, 7869, 11072, 22401, 47699, 132096,
    #           337877, 618224, 990371], 'ro')
    # plt.axis([0, 11, 0, 990371])
    # plt.show()
    t = np.arange(0., 5., 0.2)
    plt.plot(t, t, 'r-')
    plt.plot(t, t**2, 'bo-')
    plt.plot(t, t**3, 'g^')
    plt.show()
