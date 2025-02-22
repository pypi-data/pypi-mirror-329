from os import PathLike
from typing import Optional

from torchvision.transforms.v2 import Transform

from pyroml.template.base.dataset import TemplateDataset


class MVTecDataset(TemplateDataset):
    def __init__(
        self,
        folder: PathLike | str = "data/mvtec",
        transform: Optional[Transform] = None,
        split: str = "train",
        save: bool = True,
    ):
        super().__init__(
            dataset_path="Voxel51/mvtec-ad",
            folder=folder,
            transform=transform,
            split=split,
            save=save,
        )
