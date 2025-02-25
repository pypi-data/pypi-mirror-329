from toyoildata.ToyOilSpillDataset import ToyOilSpillDataset
from lightning import LightningDataModule
from torch.utils.data import DataLoader


class ToyOilSpillDataModule(LightningDataModule):
    def __init__(self, batch_size=4, **kwargs):
        super().__init__()
        self.kwargs = kwargs
        self.batch_size = batch_size

    def setup(self, stage=None):
        self.train_dataset = ToyOilSpillDataset(**self.kwargs)
        self.val_dataset = ToyOilSpillDataset(**self.kwargs)
        self.test_dataset = ToyOilSpillDataset(**self.kwargs)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size)
