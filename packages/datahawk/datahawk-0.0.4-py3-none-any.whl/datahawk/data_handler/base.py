from abc import ABC
from typing import Any, Dict, Optional, Tuple


class DataHandler(ABC):
    """
    The backend data handler. Maintains current data state and operates on it
    to give the Inspector what it is asking for.
    """
    def __init__(self, data_path: str, read_mode: str, *args, **kwargs):
        self.data_path: str = data_path
        self.read_mode: str = read_mode
        self.current_index: int = None
        self.data: Optional[Any] = None
        self.current_data: Optional[Any] = None

    def data_size(self):
        """Return the size of the data if possible."""
        raise NotImplementedError
    
    def read_data(self):
        """Read the data and prepare for applying operations and navigation"""
        raise NotImplementedError
    
    def get_item(self, new_index: int) -> Tuple[bool, Dict]:
        """Get the item accessed by `new_index`"""
        raise NotImplementedError
    
    def operate_on_data(self, *args, **kwargs) -> Any:
        """Perform some operations on the data"""
        raise NotImplementedError
