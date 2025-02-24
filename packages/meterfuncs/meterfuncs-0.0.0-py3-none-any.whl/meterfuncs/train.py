import pathlib
import sys
import typing as t
from datetime import datetime
import torch

from loguru import logger
from tensorboardX import SummaryWriter


def handleExit(logger, msg: str):
    """exit with logger and msg"""
    logger.error(msg)
    sys.exit(1)


def enableHyperConfig(trainner):
    """might useful?"""
    old_train = trainner.main

    def main(self, config, **kwargs):
        """write hyperConfig to tensorboard"""
        self.writer.add_hparams(config, kwargs)
        return old_train(config, **kwargs)

    trainner.main = main

    return trainner


class Trainer(object):
    def __init__(self) -> None:
        self.writer = SummaryWriter()
        self.start_time = datetime.now()
        self.stop_time = None
        self.logger = logger


def getBaseTrain() -> t.Type[Trainer]:
    return Trainer


def log_value(
    writer: SummaryWriter,
    name: str,
    value,
    step: int,
):
    writer.add_scalar(f"data/{name}", value, step)


def log_tensor(
    stop_time: t.Optional[datetime],
    name: str,
    value,
    step: int,
):
    if stop_time is None:
        stop_time = datetime.now()  #
    date_time = stop_time.strftime("%m-%d-%Y-%H-%M-%S")

    p = pathlib.Path("./log") / date_time / str(step) / name
    p.parent.mkdir(parents=True, exist_ok=True)
    torch.save(value, p.with_suffix(".pt"))
