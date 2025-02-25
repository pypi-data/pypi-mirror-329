from toyoildata import ToyOilSpillDataset


def test_ToyOilSpillDataset():
    import matplotlib.pyplot as plt

    ds = ToyOilSpillDataset()
    assert len(ds) == 64
    img, pred, label = ds[0]
    assert img.shape == (256, 256)
    assert pred.shape == (256, 256)
    assert label.shape == (256, 256)

    ## Just make sure it runs
    ds.show_examples()
    plt.close()
