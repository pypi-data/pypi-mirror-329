import abc
from abc import abstractmethod
from typing import (
    Any,
    Callable,
)

from eclypse_core.graph.node_group import NodeGroup

from .space import AssetSpace

class Asset(metaclass=abc.ABCMeta):
    """Asset represents a resource of the infrastructure, such as CPU, GPU, RAM or
    Availability.

    It provides the inteface for the basic algebraic functions between assets.
    """

    def __init__(
        self,
        lower_bound: Any,
        upper_bound: Any,
        init_spaces: dict[
            NodeGroup | tuple[NodeGroup, NodeGroup], AssetSpace | Callable[[], Any]
        ],
        functional: bool = True,
    ) -> None:
        """Initialize the asset with the lower and upper bounds.

        The lower and the upper bounds represent the element which is always contained in
        and the element the always contains the asset, respectively. Thus, they must
        respect the total ordering of the asset.

        The init_fns are the functions to initialize the asset. It must contain all the
        values of `NodeGroup` as keys for a node asset, and all the ordered combinations
        of `NodeGroup` as keys for a link asset.

        Args:
            lower_bound (Any): The lower bound of the asset.
            upper_bound (Any): The upper bound of the asset.
            group_init_fns (Dict[NodeGroup, Callable]): The functions to initialize the asset.
        """

    @abstractmethod
    def aggregate(self, *assets) -> Any:
        """Aggregate the assets into a single asset.

        Args:
            assets (Any): The assets to aggregate.
        """

    @abstractmethod
    def satisfies(self, asset: Any, constraint: Any) -> bool:
        """Check if the asset satisfies the constraint.

        Args:
            asset (Any): The asset to check.
            constraint (Any): The constraint to check.

        Returns:
            bool: True if the asset satisfies the constraint, False otherwise.
        """

    @abstractmethod
    def is_consistent(self, asset: Any) -> bool:
        """Check if the asset has a feasible value."""
