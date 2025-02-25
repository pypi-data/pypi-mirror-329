"""Relative center-of-mass task implementation."""

from __future__ import annotations

from typing import Optional

import mujoco
import numpy as np
import numpy.typing as npt

from ..configuration import Configuration
from .exceptions import InvalidTarget, TargetNotSet, TaskDefinitionError
from .task import Task


class RelativeComTask(Task):
    """Regulate the center-of-mass (CoM) of a robot relative to another frame.

    Attributes:
        root_name: Name of the root frame.
        root_type: The root frame type: 'body', 'geom', or 'site'.
        target_com_in_root_frame: Target CoM position expressed in the root frame.
    """

    k: int = 3
    target_com_in_root_frame: Optional[np.ndarray]

    def __init__(
        self,
        root_name: str,
        root_type: str,
        cost: npt.ArrayLike,
        gain: float = 1.0,
        lm_damping: float = 0.0,
    ):
        super().__init__(cost=np.zeros((self.k,)), gain=gain, lm_damping=lm_damping)
        self.root_name = root_name
        self.root_type = root_type
        self.target_com_in_root_frame = None

        self.set_cost(cost)

    def set_cost(self, cost: npt.ArrayLike) -> None:
        cost = np.atleast_1d(cost)
        if cost.ndim != 1 or cost.shape[0] not in (1, self.k):
            raise TaskDefinitionError(
                f"{self.__class__.__name__} cost must be a vector of shape (1,) "
                f"(aka identical cost for all coordinates) or ({self.k},). "
                f"Got {cost.shape}"
            )
        if not np.all(cost >= 0.0):
            raise TaskDefinitionError(f"{self.__class__.__name__} cost must be >= 0")
        self.cost[:] = cost

    def set_target(self, target_com_in_root_frame: npt.ArrayLike) -> None:
        """Set the target CoM position in the root frame.

        Args:
            target_com_in_root_frame: Desired center-of-mass position in the root frame.
        """
        target_com_in_root_frame = np.atleast_1d(target_com_in_root_frame)
        if target_com_in_root_frame.ndim != 1 or target_com_in_root_frame.shape[0] != (self.k):
            raise InvalidTarget(
                f"Expected target CoM in root frame to have shape ({self.k},) but got "
                f"{target_com_in_root_frame.shape}"
            )
        self.target_com_in_root_frame = target_com_in_root_frame.copy()

    def set_target_from_configuration(self, configuration: Configuration) -> None:
        """Set the target CoM position in the root frame from a given robot configuration.

        Args:
            configuration: Robot configuration :math:`q`.
        """
        # Get CoM position in world frame
        current_com = configuration.data.subtree_com[1]
        # Get transform from root frame to world frame
        transform_root_to_world = configuration.get_transform_frame_to_world(
            self.root_name, self.root_type
        )
        # Get inverse transform (world to root frame)
        transform_world_to_root = transform_root_to_world.inverse()
        # Compute current CoM in root frame coordinates
        current_com_in_root_frame = transform_world_to_root.apply(current_com)
        # Set target_com_in_root_frame
        self.set_target(current_com_in_root_frame)

    def compute_error(self, configuration: Configuration) -> np.ndarray:
        """Compute the CoM task error relative to the root frame.

        Args:
            configuration: Robot configuration :math:`q`.

        Returns:
            Center-of-mass task error vector :math:`e(q)`.
        """
        if self.target_com_in_root_frame is None:
            raise TargetNotSet(self.__class__.__name__)

        # Get CoM position in world frame
        current_com = configuration.data.subtree_com[1]
        # Get transform from root frame to world frame
        transform_root_to_world = configuration.get_transform_frame_to_world(
            self.root_name, self.root_type
        )
        # Get inverse transform (world to root frame)
        transform_world_to_root = transform_root_to_world.inverse()
        # Compute current CoM in root frame coordinates
        current_com_in_root_frame = transform_world_to_root.apply(current_com)
        # Compute error
        error = current_com_in_root_frame - self.target_com_in_root_frame
        return error

    def compute_jacobian(self, configuration: Configuration) -> np.ndarray:
        """Compute the CoM task Jacobian relative to the root frame.

        Args:
            configuration: Robot configuration :math:`q`.

        Returns:
            Center-of-mass task Jacobian :math:`J(q)`.
        """
        if self.target_com_in_root_frame is None:
            raise TargetNotSet(self.__class__.__name__)

        # Get CoM Jacobian in world frame
        J_com = np.empty((self.k, configuration.nv))
        mujoco.mj_jacSubtreeCom(configuration.model, configuration.data, J_com, 1)

        # Get Jacobian of root frame position in world frame
        J_root_full = configuration.get_frame_jacobian(self.root_name, self.root_type)
        J_root_pos = J_root_full[:3, :]  # First 3 rows: position Jacobian

        # Get rotation matrix from world frame to root frame
        transform_root_to_world = configuration.get_transform_frame_to_world(
            self.root_name, self.root_type
        )
        R_wr = transform_root_to_world.rotation().as_matrix()
        R_rw = R_wr.T  # Transpose to get world to root frame rotation

        # Compute Jacobian of CoM in root frame coordinates
        J_com_root = R_rw @ (J_com - J_root_pos)

        return J_com_root
