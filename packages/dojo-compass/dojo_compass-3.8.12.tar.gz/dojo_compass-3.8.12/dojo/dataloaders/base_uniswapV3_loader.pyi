import abc
from abc import ABC
from dojo.dataloaders.base_loader import BaseLoader as BaseLoader
from dojo.dataloaders.formats import UniswapV3Event as UniswapV3Event

class BaseUniswapV3Loader(BaseLoader, ABC, metaclass=abc.ABCMeta): ...
