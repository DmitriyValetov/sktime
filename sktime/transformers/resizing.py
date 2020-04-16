import numpy as np
import pandas as pd
from scipy import interpolate

from sktime.transformers.base import BaseTransformer

class TSResizeTransform(BaseTransformer):
    """Transformer that get casual dataframe of time series and resizes 
            Series to user length via scipy interp1d between received points.
    """

    def __init__(self, length):
        """
        Parameters
        ----------
        length : integer, the length of time series to resize to.
        """
        if length<=0 or (not isinstance(length, int)):
            raise ValueError("resizing length must be integer and > 0")

        self.length = length
        super(TSResizeTransform).__init__()
        
    def _resize_cell(self, cell):
        f = interpolate.interp1d(list(np.linspace(0, 1, len(cell))), list(cell))
        return f(np.linspace(0, 1, self.length))
    
    def _resize_col(self, coll):
        return coll.apply(self._resize_cell)
    
    def transform(self, X, y=None):
        """Resizes time series in each cell of dataframe and returns it.

        Parameters
        ----------
        X : nested pandas DataFrame of shape [n_samples, n_features]
            Nested dataframe with time-series in cells.

        Returns
        -------
        Xt : pandas DataFrame
          Transformed pandas DataFrame with same number of rows and columns
        """
        return X.apply(self._resize_col)