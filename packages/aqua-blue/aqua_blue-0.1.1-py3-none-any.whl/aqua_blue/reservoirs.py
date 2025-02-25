"""
Module defining reservoirs
"""


from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, Callable, TYPE_CHECKING

import numpy as np


#: Type alias for activation function. Callable taking in a numpy array, and returning a numpy array of the same shape
ActivationFunction = Callable[[np.typing.NDArray[np.floating]], np.typing.NDArray[np.floating]]

# pdoc needs it to be a string, but type checker needs it to be a true alias, so replace if not type checking
if not TYPE_CHECKING:
    ActivationFunction = "ActivationFunction"


@dataclass
class Reservoir(ABC):

    """
    Abstract base reservoir class defining input state -> reservoir state
    """

    input_dimensionality: int
    """dimensionality of the input state"""

    reservoir_dimensionality: int
    """dimensionality of the reservoir state, equivalently the reservoir size"""

    @abstractmethod
    def input_to_reservoir(self, input_state: np.typing.NDArray[np.floating]) -> np.typing.NDArray[np.floating]:

        """
        Map from input state to reservoir state

        Args:
            input_state: input state to map to reservoir state
        """

        pass


@dataclass
class DynamicalReservoir(Reservoir):

    """
    Dynamical reservoir state, defined by the mapping:
    y_t = f(w_in @ x_t)
    where f is some nonlinear activation function
    """

    generator: Optional[np.random.Generator] = None
    """
    random generator for the class to use
    will be set to np.random.default_rng(seed=0) if not specified
    """

    w_in: Optional[np.typing.NDArray[np.floating]] = None
    """
    input linear mapping. must be shape (self.reservoir_dimensionality, self.input_dimensionality)
    if not defined at initialization, will be auto generated
    """

    activation_function: ActivationFunction = np.tanh
    """
    activation function f. defaults to np.tanh
    """

    def __post_init__(self):

        if self.generator is None:
            self.generator = np.random.default_rng(seed=0)

        if self.w_in is None:
            self.w_in = self.generator.uniform(
                low=-0.5,
                high=0.5,
                size=(self.reservoir_dimensionality, self.input_dimensionality)
            )

    def input_to_reservoir(self, input_state: np.typing.NDArray[np.floating]) -> np.typing.NDArray[np.floating]:

        """
        Map from input state to reservoir state via y_t = f(w_in @ x_t)

        Args:
            input_state: input state to map to reservoir state
        """

        assert isinstance(self.w_in, np.ndarray)
        return self.activation_function(self.w_in @ input_state)
