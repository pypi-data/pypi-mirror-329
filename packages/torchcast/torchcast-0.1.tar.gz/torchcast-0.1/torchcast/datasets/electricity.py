from datetime import datetime
from typing import Callable, Optional, Union

import numpy as np
import pandas as pd
import torch

from ..data import Metadata, TensorSeriesDataset
from .utils import _download_and_extract, _split_ltsf

__all__ = ['ElectricityLoadDataset']

ELECTRICITY_LOAD_URL = 'https://github.com/laiguokun/multivariate-time-series-data/raw/master/electricity/electricity.txt.gz'  # noqa
ELECTRICITY_LOAD_FILE_NAME = 'electricity.txt'


class ElectricityLoadDataset(TensorSeriesDataset):
    '''
    Electricity Load dataset, obtained from:

        https://github.com/laiguokun/multivariate-time-series-data

    This is derived from:

        https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014

    But the data has been subsetted and pre-processed. It is sometimes
    abbreviated as the `ECL` dataset.
    '''
    def __init__(self, path: Optional[str] = None, split: str = 'all',
                 download: Union[str, bool] = True, scale: bool = True,
                 columns_as_channels: bool = True,
                 transform: Optional[Callable] = None,
                 input_margin: Optional[int] = 336,
                 return_length: Optional[int] = None):
        '''
        Args:
            path (optional, str): Path to find the dataset at.
            split (str): What split of the data to return. The splits are taken
                from Zeng et al. Choices: 'all', 'train', 'val', 'test'.
            download (bool): Whether to download the dataset if it is not
                already available.
            scale (bool): Whether to normalize the data, as in the benchmark.
            columns_as_channels (bool): If true, each column is treated as a
                separate channel. If false, each column is treated as a
                separate series.
            transform (optional, callable): Pre-processing functions to apply
                before returning.
            input_margin (optional, int): The amount of margin to include on
                the left-hand side of the dataset, as it is used as an input to
                the model.
            return_length (optional, int): If provided, the length of the
                sequence to return. If not provided, returns an entire
                sequence.
        '''
        buff = _download_and_extract(
            ELECTRICITY_LOAD_URL,
            ELECTRICITY_LOAD_FILE_NAME,
            path,
            download=download,
        )

        df = pd.read_csv(buff, header=None)

        data = np.array(df, dtype=np.float32).T
        data = torch.from_numpy(data.reshape(1, *data.shape))

        # Per the README at:
        # https://github.com/laiguokun/multivariate-time-series-data
        # The data is taken hourly, starting at 2012-01-01.
        t = pd.date_range(
            datetime(2012, 1, 1), datetime(2014, 12, 31, 23, 59, 59), freq='h'
        )
        t = torch.from_numpy(t.astype(np.int64).values).view(1, 1, -1)

        if scale:
            train_data = _split_ltsf('train', input_margin, data)
            mean, std = train_data.mean((0, 2)), train_data.std((0, 2))
            data = (data - mean.reshape(1, -1, 1)) / std.reshape(1, -1, 1)

        data, t = _split_ltsf(split, input_margin, data, t)

        if not columns_as_channels:
            data = data.permute(1, 0, 2)

        super().__init__(
            t, data,
            transform=transform,
            return_length=return_length,
            metadata=[Metadata(name='Datetime'), Metadata(name='Load')],
        )
