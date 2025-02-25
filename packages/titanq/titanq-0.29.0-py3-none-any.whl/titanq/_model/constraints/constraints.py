# Copyright (c) 2024, InfinityQ Technology, Inc.
import logging
from typing import Any, Optional
import numpy as np
import numpy.typing as npt

from .base_constraints import BaseConstraints
from ...errors import ConstraintSizeError, MaximumConstraintLimitError

log = logging.getLogger("TitanQ")

_MAX_CONSTRAINTS_COUNT = 32_000


class Constraints(BaseConstraints):
    def __init__(self) -> None:
        self._constraint_weights = None
        self._constraint_bounds = None


    def is_empty(self) -> bool:
        """return if all constraints are empty"""
        return self._constraint_weights is None and self._constraint_bounds is None


    def add_constraint(
        self,
        num_variables: int,
        constraint_weights: npt.NDArray[Any],
        constraint_bounds: npt.NDArray[Any]
    ) -> None:
        """
        Add a constraint to the existing ones

        :param num_variables: the number of variables from the model
        :param constraint_weights: constraint_weights to append to the existing ones.
        :param constraint_bounds: constraint_bounds to append to the existing ones.

        :raises ConstraintSizeError:
            Number of constraints is different than the number of
            variables.
        :raises MaximumConstraintLimitError: the number of constraints exceeds the limit.
        """
        # shape validation
        if constraint_weights.shape[1] != num_variables:
            raise ConstraintSizeError(
                "Constraint mask shape does not match the number of variables. "
                + f"Number of constraints: {constraint_weights.shape[1]}, "
                + f"Number of variables: {num_variables}")

        # limit validation
        if num_variables + self._rows_count(self._constraint_weights) + constraint_weights.shape[0] > _MAX_CONSTRAINTS_COUNT:
            raise MaximumConstraintLimitError(
                "Cannot add additional constraints. The limit of constraints have been reached. " \
                f"The sum of variables and constraints cannot exceed {_MAX_CONSTRAINTS_COUNT}." \
                f"Number of constraints: {self._rows_count(self._constraint_weights)}; " \
                f"Number of variables: {num_variables}; " \
                f"while trying to add {constraint_weights.shape[0]} new constraints."
            )

        self._constraint_weights = self._append_constraint(constraint_weights, self._constraint_weights)
        self._constraint_bounds = self._append_constraint(constraint_bounds, self._constraint_bounds)


    def weights(self) -> Optional[npt.NDArray[np.float32]]:
        """
        :return: The weights constraints.
        """
        return self._constraint_weights


    def bounds(self) -> Optional[npt.NDArray[np.float32]]:
        """
        :return: The bounds constraints.
        """
        return self._constraint_bounds
