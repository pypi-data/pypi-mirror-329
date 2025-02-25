from neurionpy.ganglion.interface import GanglionQuery, GanglionMessage
from neurionpy.synapse.client import NeurionClient
from neurionpy.synapse.config import NetworkConfig
from .wallet import get_wallet


def get_query_client() -> GanglionQuery:
    """Get query client."""
    return NeurionClient(NetworkConfig.neurion_localnet(), get_wallet()).ganglion


def get_message_client() -> GanglionMessage:
    """Get message client."""
    return NeurionClient(NetworkConfig.neurion_localnet(), get_wallet()).ganglion.tx
