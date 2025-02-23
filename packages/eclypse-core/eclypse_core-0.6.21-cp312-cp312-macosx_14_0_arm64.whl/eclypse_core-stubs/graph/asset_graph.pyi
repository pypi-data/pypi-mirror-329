from typing import (
    Callable,
    Literal,
)

import networkx as nx
from networkx.classes.reportviews import (
    EdgeView,
    NodeView,
)

from eclypse_core.graph.assets import Asset
from eclypse_core.graph.node_group import NodeGroup
from eclypse_core.utils._logging import Logger

class AssetGraph(nx.DiGraph):
    """AssetGraph represents an heterogeneous network infrastructure."""

    def __init__(
        self,
        graph_id: str,
        node_assets: dict[str, Asset] | None = None,
        edge_assets: dict[str, Asset] | None = None,
        node_update_policy: (
            Callable[[NodeView], None] | list[Callable[[NodeView], None]] | None
        ) = None,
        edge_update_policy: (
            Callable[[EdgeView], None] | list[Callable[[EdgeView], None]] | None
        ) = None,
        attr_init: Literal["min", "max"] = "min",
        flip_assets: bool = False,
        seed: int | None = None,
    ) -> None:
        """Initializes the AssetGraph object.

        Args:
            graph_id (str): The ID of the graph.
            node_assets (Optional[Dict[str, Asset]], optional): The assets of the nodes.                Defaults to None.
            edge_assets (Optional[Dict[str, Asset]], optional): The assets of the edges.                Defaults to None.
            node_update_policy (Optional[Callable[[NodeView], None]], optional): The policy to update the nodes. Defaults to None.
            edge_update_policy (Optional[Callable[[EdgeView], None]], optional): The policy to update the edges. Defaults to None.
            attr_init (Literal["min", "max"], optional): The initialization policy for the assets. Defaults to "min".
            flip_assets (bool, optional): Whether to flip the assets. Defaults to False.
            seed (Optional[int], optional): The seed for the random number generator.
                Defaults to None.
        """

    def add_node_by_group(
        self, node_group: NodeGroup, node_for_adding: str | None = None, **assets
    ):
        """Adds a node or edge to the graph with the given assets.

        Args:
            group (str): The group to which the asset belongs.
            **assets: The assets of the node or edge.
        """

    def add_symmetric_edge(self, u_of_edge: str, v_of_edge: str, **assets):
        """Adds a symmetric edge to the graph with the given assets.

        Args:
            u_of_edge (str): The source node.
            v_of_edge (str): The target node.
            **assets: The assets of the edge.
        """

    def tick(self) -> None:
        """Updates the graph according to its update policies."""

    def add_edge_by_group(
        self,
        source: str,
        target: str,
        source_group: NodeGroup | None = None,
        target_group: NodeGroup | None = None,
        symmetric: bool = False,
        **assets
    ):
        """Adds a link between two nodes with the given assets.

        Args:
            source (str): The source node.
            target (str): The target node.
            source_group (NodeGroup): The group of the source node.
            target_group (NodeGroup): The group of the target node.
            symmetric (bool, optional): Whether the edge is symmetric. Defaults to False.
            **assets: The assets of the edge.

        Raises:
            ValueError: If the source group is greater than the target group.
        """

    def add_cloud_node(self, node_for_adding: str | None = None, **assets):
        """Adds a cloud node to the graph."""

    def add_far_edge_node(self, node_for_adding: str, **assets):
        """Adds a link between a cloud node and another node."""

    def add_near_edge_node(self, node_for_adding: str, **assets):
        """Adds a link between a cloud node and another node."""

    def add_iot_node(self, node_for_adding: str, **assets):
        """Adds an IoT node to the graph."""

    @property
    def is_dynamic(self) -> bool:
        """Checks if the graph is dynamic, i.e., if it has an update policy.

        Returns:
            bool: True if the graph is dynamic, False otherwise.
        """

    @property
    def logger(self) -> Logger:
        """Get a logger for the graph, binding the graph id in the logs.

        Returns:
            Logger: The logger for the graph.
        """
