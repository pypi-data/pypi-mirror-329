from typing import (
    Any,
    Callable,
)

from eclypse_core.graph.node_group import NodeGroup

from .asset import Asset
from .space import AssetSpace

class Convex(Asset):
    """ConvexAsset represents a numeric asset where the aggregation is convex."""

    def __init__(
        self,
        lower_bound: float,
        upper_bound: float,
        init_spaces: dict[
            NodeGroup | tuple[NodeGroup, NodeGroup], AssetSpace | Callable[[], Any]
        ],
        functional: bool = True,
    ) -> None:
        """Create a new convex asset.

        Args:
            lower_bound (float): The lower bound of the asset.
            upper_bound (float): The upper bound of the asset.
            init_fns (Dict[NodeGroup, Callable]): The functions to initialize the asset.

        Raises:
            ValueError: If $lower_bound < upper_bound$.
        """

    def aggregate(self, *assets) -> float:
        """Aggregate the assets into a single asset by taking the minimum value. If no
        assets are provided, the upper bound is returned.

        Args:
            assets (Iterable[NumericAsset]): The assets to aggregate.

        Returns:
            NumericAsset: The aggregated asset.
        """

    def satisfies(self, asset: float, constraint: float) -> bool:
        """Check if asset1 contains asset2. In the ordering of a convex asset, the
        higher value contains the other.

        Args:
            asset1 (NumericAsset): The "container" asset.
            asset2 (NumericAsset): The "contained" asset.

        Returns:
            bool: True if asset1 >= asset2, False otherwise.
        """

    def is_consistent(self, asset: float) -> bool:
        """Check if the asset belongs to the interval [lower_bound, upper_bound].

        Args:
            asset (NumericAsset): The asset to check.

        Returns:
            bool: True if the asset is within the interval, False otherwise.
        """
