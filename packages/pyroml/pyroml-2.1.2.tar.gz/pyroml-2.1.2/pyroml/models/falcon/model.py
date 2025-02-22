from typing import TYPE_CHECKING

import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
from torch_ema import ExponentialMovingAverage

import pyroml as p
from pyroml.core.stage import Stage

from .heads import with_model_head
from .loss import FalconLoss

if TYPE_CHECKING:
    from pyroml.callbacks import CallbackArgs
    from pyroml.core.trainer import Trainer
    from pyroml.loop import Loop


class Falcon(p.PyroModule):
    def __init__(
        self,
        backbone: nn.Module,
        # Number of fine and coarse classes
        fine_classes: int,
        coarse_classes: int,
        # Model
        embed_dim: int,  # Model embedding size (last layer output shape)
        head_type: str = "Linear",
        # Training parameters
        beta_reg: float = 0.1,
        time_limit: float = 30,  # in seconds
        soft_labels_epochs: int = 30,
        solve_every: int = 20,
        ## Loss
        loss_temp: float = 0.9,
        loss_lambda1: float = 0.5,
        loss_lambda2: float = 0.5,
        loss_lambda3: float = 0.5,
    ):
        """
        Default values are mostly taken from https://github.com/mlbio-epfl/falcon/blob/main/configs/cifar100/coarse2fine/base.yaml
        """
        super().__init__()
        self.backbone = with_model_head(
            model=backbone,
            head_type=head_type,
            num_class=fine_classes,
            embed_dim=embed_dim,
        )

        self.ema = ExponentialMovingAverage(self.parameters(), decay=0.99)
        self.loss = FalconLoss(
            model=self,
            fine_classes=fine_classes,
            coarse_classes=coarse_classes,
            beta_reg=beta_reg,
            time_limit=time_limit,
            soft_labels_epochs=soft_labels_epochs,
            solve_every=solve_every,
            loss_temp=loss_temp,
            loss_lambda1=loss_lambda1,
            loss_lambda2=loss_lambda2,
            loss_lambda3=loss_lambda3,
        )

    def _setup(self, trainer: "Trainer"):
        super()._setup(trainer)
        # Register the loss as a trainer callback
        trainer.callbacks.append(self)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.backbone(x)
        return x

    def configure_optimizers(self, _: "Loop"):
        self.optimizer = torch.optim.SGD(
            self.parameters(),
            lr=0.1,
            weight_decay=0,
            nesterov=False,
            momentum=0.9,
        )
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            self.optimizer, T_0=30, eta_min=0.001
        )
        self.scaler = torch.amp.GradScaler(
            device=self.trainer.device, enabled=self.trainer.dtype == torch.float16
        )

    def on_train_start(self, _: "CallbackArgs"):
        cudnn.benchmark = True

    def step(self, batch, stage: Stage):
        if stage == Stage.TRAIN:
            loss: torch.Tensor = self.loss(batch, stage=stage)
            return loss

        x: torch.Tensor = batch["img"]
        logits: torch.Tensor = self(x)
        conf, pred = logits.cpu().softmax(-1).max(-1)
        return dict(conf=conf, pred=pred)

        # ged = compute_ged(
        #     make_adjacency_matrix(M.cpu().numpy()),
        #     make_adjacency_matrix(ev_ds.get_graph()),
        # )

        # # === EVAL

        # # total_conf = 0.0

        # # x: torch.Tensor = data["x"]
        # # y_fine: torch.Tensor = data["fine_label"]
        # # actual.append(y_fine)

        # # x = x.to(self.device)
        # # logits: torch.Tensor = model(x)
        # # conf, pred_ = logits.softmax(-1).max(-1)
        # # total_conf += conf.sum().item()

        # # pred.append(pred_)
        # # pbar.update(1)

        # # actual = torch.cat(actual, dim=0).cpu()
        # # _pred = torch.cat(pred, dim=0).cpu()

        # ari = adjusted_rand_score(_pred, actual)
        # avg_conf = total_conf / len(dataset)
        # acc = cluster_acc(_pred, actual)
        # mapper = compute_matchings(_pred, actual)
        # macc = macro_accuracy(mapper[_pred], actual)

    def on_train_epoch_end(self, _):
        self.scheduler.step()

    def _fit(self, loss: torch.Tensor):
        self.optimizer.zero_grad()
        self.scaler.scale(loss).backward()
        self.scaler.step(self.optimizer)
        self.scaler.update()
        self.ema.update()
