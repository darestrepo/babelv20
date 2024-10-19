from abc import ABC, abstractmethod
from typing import Dict
from app.api.models.message_model import MessageModel

class PlatformAdapter(ABC):
    """
    Abstract base class for platform adapters.
    Defines methods for converting messages to and from the universal format.
    """

    @abstractmethod
    def to_universal(self, platform_message: Dict) -> MessageModel:
        """
        Convert a platform-specific message to the universal MessageModel.
        """
        pass

    @abstractmethod
    def from_universal(self, universal_message: MessageModel) -> Dict:
        """
        Convert a universal MessageModel to a platform-specific message.
        """
        pass
