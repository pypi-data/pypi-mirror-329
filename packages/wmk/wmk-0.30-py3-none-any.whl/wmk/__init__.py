from .client_messages import ClientMessages
from .loader import Loader
from .media_consumer import MediaConsumer
from .messenger import Messenger
from .packager import Packager
from .player import Player
from .system_messages import SystemMessages
from .world_messages import WorldMessages


# Lazy loading for PipecatVideoOutputProcessor
def __getattr__(name):
    if name == "PipecatVideoOutputProcessor":
        from .pipecat_transport import PipecatVideoOutputProcessor

        return PipecatVideoOutputProcessor
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "Player",
    "Messenger",
    "WorldMessages",
    "ClientMessages",
    "SystemMessages",
    "Packager",
    "Loader",
    "MediaConsumer",
]
