import copy
import json
import os
from typing import Dict, Tuple

import ijson

from .jsonl_data_handler import JSONLDataHandler


class JSONDataHandler(JSONLDataHandler):
    def __init__(self, data_path: str, read_mode: str):
        super().__init__(data_path, read_mode)

    def read_data(self):
        """Read JSONL data from a location on the disk."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"File does not exist: {self.data_path}")
        if self.read_mode == "load":
            # load the JSONL data from disk
            try:
                with open(self.data_path, "r") as f:
                    self.data = json.load(f)
            except:
                raise Exception("Could not parse the JSON file properly")
            self.current_data = copy.deepcopy(self.data)
        
        elif self.read_mode == "stream":
            # stream the JSONL data from disk
            self.current_data = iter(self._stream())
        
        else:
            raise ValueError("JSONLDataHandler does not support read_mode: "
                             f"{self.read_mode}")
    
    def _stream(self):
        """Stream the data path"""
        with open(self.data_path, "rb") as f:
            for item in ijson.items(f, "item"):
                yield item
        
    def get_item(self, new_index: str) -> Tuple[bool, Dict]:
        """Get the item accessed by `new_index`"""
        if self.read_mode == "load":
            # check if the specified index is valid
            if new_index >= len(self.current_data) or new_index < 0:
                return (False, {
                    "error_message": "ERROR: Index out of range or invalid index "
                                     f"for a dataset of {len(self.current_data)} rows."
                })
            # can read the item now
            self.current_index = new_index
            self.current_item = self.current_data[self.current_index]
            return (True, self.current_item)
        
        elif self.read_mode == "stream":
            try:
                self.current_item = next(self.current_data)
            except StopIteration:
                return (False, {
                    "error_message": "ERROR: Reached end of file. Load the file again."
                })
            except:
                raise Exception("Could not parse the JSON file properly.")
            # got an item successfully
            self.current_index = new_index
            return (True, self.current_item)
        
        else:
            raise ValueError(f"Invalid read_mode: {self.read_mode}")
