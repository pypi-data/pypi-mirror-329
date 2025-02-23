from typing import Any

from .asset import Asset

class AssetBucket(dict[str, Asset]):
    """Class to store a set of nodes/services assets."""

    def __init__(self, **assets) -> None:
        """Create a new asset bucket.

        Args:
            **assets (Dict[str, Asset]): The assets to store in the bucket.
        """

    def __setitem__(self, key: str, value: Asset) -> None:
        """Set an asset in the bucket.

        Args:
            key (str): The key of the asset.
            value (Asset): The asset to store.
        """

    def aggregate(self, *assets: dict[str, Any]) -> dict[str, Any]:
        """Aggregate the assets into a single asset.

        Args:
            assets (Iterable[Dict[str, Any]]): The assets to aggregate.

        Returns:
            Dict[str, Any]: The aggregated asset.
        """

    def satisfies(self, asset: dict[str, Any], constraint: dict[str, Any]) -> bool:
        """Check if the assets of the other asset are contained in the assets of this
        asset.

        Args:
            asset1 (Dict[str, Any]): The "container" asset.
            asset2 (Dict[str, Any]): The "contained" asset.

        Returns:
            bool: True if the assets of asset2 are contained in asset1, False otherwise.
        """

    def consume(self, asset: dict[str, Any], amount: dict[str, Any]) -> dict[str, Any]:
        """Consume the `amount` of the asset from the `asset`.

        Args:
            asset (Dict[str, Any]): The asset to consume from.
            amount (Dict[str, Any]): The amount to consume.

        Returns:
            Dict[str, Any]: The remaining asset after the consumption.
        """

    def is_consistent(self, asset: dict[str, Any]) -> bool:
        """Check if the asset belongs to the interval [lower_bound, upper_bound].

        Args:
            asset (Dict[str, Any]): The asset to be checked.

        Returns:
            bool: True if the asset is within the interval, False otherwise.
        """

    def flip(self):
        """Flip the assets of the bucket, thus moving from node capabilities to service.

        requirements:
        - Convex assets become Concave assets, and vice versa.
        - Multiplicative assets become Concave assets.

        N.B. Cannot be used more than once, since the flip is not reversible.
        """

    @property
    def lower_bound(self) -> dict[str, Any]:
        """Return the lower bound of the asset bucket, i.e. the lower bound of each
        asset in the bucket.

        Returns:
            Dict[str, Any]: The lower bound of the asset bucket.
        """

    @property
    def upper_bound(self) -> dict[str, Any]:
        """Return the upper bound of the asset bucket, i.e. the upper bound of each
        asset in the bucket.

        Returns:
            Dict[str, Any]: The upper bound of the asset bucket.
        """
