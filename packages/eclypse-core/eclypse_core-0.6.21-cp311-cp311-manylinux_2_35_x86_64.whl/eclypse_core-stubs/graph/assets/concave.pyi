from typing import (
    Any,
    Callable,
)

from eclypse_core.graph import NodeGroup

from .asset import Asset
from .space import AssetSpace

class Concave(Asset):
    """ConcaveAsset represents a numeric asset where the aggregation is concave."""

    def __init__(
        self,
        lower_bound: float,
        upper_bound: float,
        init_spaces: dict[
            NodeGroup | tuple[NodeGroup, NodeGroup], AssetSpace | Callable[[], Any]
        ],
        functional: bool = True,
    ) -> None:
        """Create a new concave asset.

        Args:
            lower_bound (TAdditive): The lower bound of the asset.
            upper_bound (TAdditive): The upper bound of the asset.
            init_fns (Dict[NodeGroup, Callable]): The functions to initialize the asset.

        Raises:
            ValueError: If $lower_bound > upper_bound$.
        """

    def aggregate(self, *assets) -> float:
        """Aggregate the assets into a single asset by taking the maximum value. If no
        assets are provided, the lower bound is returned.

        Args:
            assets (Iterable[TConcave]): The assets to aggregate.

        Returns:
            TConcave: The aggregated asset.
        """

    def satisfies(self, asset: float, constraint: float) -> bool:
        """Check if asset1 contains asset2. In the ordering of a concave asset, the
        lower value contains the other.

        Args:
            asset1 (TConcave): The "container" asset.
            asset2 (TConcave): The "contained" asset.

        Returns:
            bool: True if asset1 <= asset2, False otherwise.
        """

    def is_consistent(self, asset: float) -> bool:
        """Check if the asset belongs to the interval [lower_bound, upper_bound]."""
