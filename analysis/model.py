"""
The Logistic Regression Model Design
"""

# Potential TODO:
#    1) Implement dynamic learning rate for effiiciency
#    2) Occasional loss calculation in place of every step

from typing import Optional, List, Tuple
import numpy as np
from numpy.typing import NDArray

from gd import gradient_descent, loss_function, sigmoid

class LogisticRegression:
    """
    Logistic regression model.
    """


    # ##################################
    # Actual model definition (params)
    weights: NDArray[np.float64]
    intercept: float
    # ##################################

    # ——————————————————————————
    # Used only in training

    # Number of training steps
    step: int
    steps_limit: int

    # # of data points
    n: int

    # Learning rate
    lr: float

    # The number of steps where we'll tolerate training-validation loss divergence before stopping
    tolerance: int

    # The actual number of divergences in a row
    divs: int

    currLoss: float
    prevLoss: float

    # Minimum % decrease in loss to consider the model as still improving
    ld: float

    # ——————————————————————————

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Used only in prediction
    threshold: float

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def __init__(self, weights: Optional[NDArray[np.float64]] = None, intercept: float = 0.0,
                n: int = 1, p: int = 1,
                steps_limit: int = 10000, tolerance: int = 5, ld: float = 0.001,
                threshold: float = 0.5):
        """
        Initializes the model with default conditions
        n stands for the number of data points
        p stands for the number of features

        Initial values can be provided for intercept and weights.
        """
        if weights is None:
            weights = np.zeros(p)

        self.weights = weights
        self.intercept = intercept

        self.steps_limit = steps_limit
        self.step = 0
        self.lr = 0.01
        self.tolerance = tolerance
        self.divs = 0
        self.currLoss = float("inf")
        self.prevLoss = float("inf")
        self.ld = ld # each step must decease loss by at least 0.1% by default
        self.n = n

        # This is the classification threshold.
        # Might need to run cross-validation to find the optimal value.
        self.threshold = threshold


    def train(self):
        """
        Train the model using gradient descent.
        Calls gradient descent function iteratively
        """
        while self.check_conditions(self):
            self.gradient_descent()
            self.step += 1
            if self.currLoss < self.prevLoss:
                self.divs = 0
            else:
                self.divs += 1
             


    def predict(self, X) -> bool:
        """
        Predict whether or not X should be assigned a positive class.
        """
        z = X @ self.weights + self.intercept
        return sigmoid(z) > self.threshold

        
    def gradient_descent(self):
        """
        Takes in the current state of the model and updates the weights and intercept
        using the gradient (just a single step).
        """
        w, b = self.loss_gradient(self.X, self.predict(self.X), self.y)
        self.weights -= self.lr * w
        self.intercept -= self.lr * b
        

    def check_conditions(self):
        """
        Gradient Descent Pauses if any of these conditions is met:

        1) Step limit is reached
        2) Training and Validation loss start to diverge (5 consecutive steps)
        3) Loss does not decrease by the required amount (ld) in a row
        """

        if self.step >= self.steps_limit or self.divs > self.tolerance or 1 - (self.currLoss / self.prevLoss) < self.ld: 
            return False

        return True


    def loss_function(self, p: np.ndarray, a: np.ndarray) -> float:
        """
        Cross-entropy loss function. Returns the average loss over the given sample.
            p: predicted values
                Shape: (n_training_samples,)
            a: actual values
                Shape: (n_training_samples,)
        """
        p = np.clip(p, 1e-15, 1 - 1e-15)  # Avoid log(0)
        t1 = a * np.log(p)
        t2 = (1 - a) * np.log(1 - p)

        return (-1 / self.n ) * (np.sum(t1 + t2))


    def loss_gradient(self, X: np.ndarray, predictions: np.ndarray, a: np.ndarray) -> tuple[np.ndarray, float]:
        """
        Derivative of cross-entropy for weight updates
        Returns gradients w.r.t. weights and bias
        """
        error = predictions - a
        grad_w = (1 / self.n) * X.T @ error
        grad_b = (1 / self.n) * np.sum(error)
        
        return grad_w, grad_b
        

    def sigmoid(self, z):
        """
        Sigmoid Function
        """
        return 1 / (1 + np.exp(-z))

