from os import PathLike
from typing import Optional

from torchvision.transforms.v2 import Transform

from pyroml.template.base import TemplateDataset


class Cifar100Dataset(TemplateDataset):
    def __init__(
        self,
        folder: PathLike | str = "data/cifar100",
        transform: Optional[Transform] = None,
        split: str = "train",
        save: bool = True,
    ):
        super().__init__(
            dataset_path="uoft-cs/cifar100",
            folder=folder,
            transform=transform,
            split=split,
            save=save,
        )
        self.fine_labels: list[str] = self.ds.info.features["fine_label"].names
        self.coarse_labels: list[str] = self.ds.info.features["coarse_label"].names
