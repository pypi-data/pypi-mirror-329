from toyoildata import ToyOilSpillDataModule


def test_ToyDataModule():
    dm = ToyOilSpillDataModule()
    dm.setup()
    ## check if dataloaders are not empty
    assert len(dm.train_dataloader()) > 0
    assert len(dm.val_dataloader()) > 0
    assert len(dm.test_dataloader()) > 0

    ## check if dataloaders return 3 tensors
    train_sample = next(iter(dm.train_dataloader()))
    assert len(train_sample) == 3

    val_sample = next(iter(dm.val_dataloader()))
    assert len(val_sample) == 3

    test_sample = next(iter(dm.test_dataloader()))
    assert len(test_sample) == 3

    ## Check the shape of the tensors
    img, pred, label = train_sample
    assert pred.shape == label.shape
