from toyoildata import ToyOilSpillDataset
import matplotlib.pyplot as plt
import numpy as np


def example_and_properties():
    ds = ToyOilSpillDataset()
    img, pred, lab = ds[0]

    assert img.shape == (256, 256)
    assert pred.shape == (256, 256)
    assert lab.shape == (256, 256)

    assert -np.inf <= img.min() <= img.max() <= np.inf
    assert 0 <= pred.min() <= pred.max() <= 1
    assert lab.min() in [0, 1]
    assert lab.max() in [0, 1]

    ds.show_examples()
    plt.show()


if __name__ == "__main__":
    example_and_properties()
