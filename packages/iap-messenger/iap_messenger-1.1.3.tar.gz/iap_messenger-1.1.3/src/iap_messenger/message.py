from dataclasses import dataclass
from typing import Any
from iap_messenger.data_decoder import decode

Error = ValueError | None

@dataclass(kw_only=True)
class Message:
    """Class for keeping track of messages."""
    Raw: bytes
    From: str
    To: str
    Parameters: dict | None = None
    Reply: bytes | Any
    error: str | None = None
    decoded: Any = None
    is_decoded: bool = False
    uid: str
    _link: str = ""
    _source: str = ""
    _content_type: str = "application/json"
    _inputs: dict

    def decode(self) -> tuple[Any, Error]:
        """Decode the Raw data."""
        return decode(self.Raw, self._content_type, self._inputs)
        
