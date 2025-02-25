import torch
import numpy as np
from torch.utils.data import Dataset
from toyoildata.utils import gen_lab_pred_pair, gen_sar_like_image, overlap_grid
import cv2
from typing import Tuple, Literal
from dataclasses import dataclass


@dataclass
class ToyOilSpillDataset(Dataset):
    resolution: int = 256
    tp: int = 4
    fp: int = 1
    fn: int = 1
    num: int = 64
    confidence_range: Tuple[float, float] = (0.6, 1.0)
    pred_blur: int = 1
    size_range: Tuple[int, int] = (1, 16)
    shapes: Literal["simple", "nrksat"] = "simple"

    def _gen_lab_pred_pair(self):
        confidences = np.random.uniform(*self.confidence_range, self.tp + self.fp)
        return gen_lab_pred_pair(
            tp=self.tp,
            fp=self.fp,
            fn=self.fn,
            resolution=self.resolution,
            confidences=confidences,
            size_range=self.size_range,
        )

    def __len__(self):
        return self.num

    def __getitem__(self, idx):
        if idx >= len(self):
            raise IndexError()

        pred, label = self._gen_lab_pred_pair()
        label = torch.tensor(label)
        pred = torch.tensor(pred)
        if self.pred_blur > 0:
            pred = pred.numpy()
            sides = int(self.pred_blur * 2)
            ## make sure sides are odd
            sides = sides + 1 if sides % 2 == 0 else sides
            pred = cv2.GaussianBlur(
                pred, (self.pred_blur, self.pred_blur), self.pred_blur
            )
            pred = torch.tensor(pred)
        img = torch.tensor(gen_sar_like_image(label))
        if self.shapes == "nrksat":
            img, pred, label = self._shapes_as_nrksat(img, pred, label)
        return img, pred, label

    def _shapes_as_nrksat(self, img, pred, label):
        img = img.repeat(2, 1, 1)
        pred = pred.repeat(1, 1, 1)
        label = label.repeat(1, 1, 1)
        return img, pred, label

    def show_examples(self):
        ds_str = repr(self).replace("nrksat", "simple")
        ds = eval(ds_str)
        print(f"Showing examples from {ds}")
        imgs, preds, labs = zip(*[ds[i] for i in range(16)])
        preds_hard = [1.0 * (p > 0.5) for p in preds]
        overlap_grid(
            labs,
            preds_hard,
            imgs,
            title=f"Examples with tp: {self.tp}, fp: {self.fp}, fn: {self.fn}",
        )


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from torch.utils.data import DataLoader

    ds = ToyOilSpillDataset(shapes="nrksat")
    dl = DataLoader(ds, batch_size=4)
    img, pred, lbl = next(iter(dl))

    print(img.shape, pred.shape, lbl.shape)

    ds.show_examples()
    plt.show()
