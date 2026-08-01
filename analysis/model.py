""""
The Linear Regression MODEL DESIGN

"""

import numpy as np
from typing import List, Tuple, Optional
from numpy.typing import NDArray

class LogisticRegression:
    """
    Implementation of our logistic regression model.

    """

    weights: NDArray[np.float64]
    intercept: float


    def __init__(self, weights: Optional[NDArray[np.float64]] = None, bias: float = 0.0, n: int = 1):
        if weights is None:
            weights = np.zeros(n)
        self.weights: NDArray[np.float64] = weights
        self.bias: float = bias

    def predict(self, X):
        """
        Predict whether or not X should be assigned a positive class.
        """
        z = self._linear_combination(X)
        return sigmoid(z)

    def train(self):
        """
        Train the model using gradient descent.
        Calls gradient descent function iteratively
        """


def sigmoid(z):
    """
    Sigmoid Function
    """
