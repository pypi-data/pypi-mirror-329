import copy
import json
import os
from typing import Any, Dict, List, Optional, Tuple

from .base import DataHandler


class JSONLDataHandler(DataHandler):
    def __init__(self, data_path: str, read_mode: str):
        super().__init__(data_path, read_mode)

    def data_size(self) -> Optional[int]:
        """Return the size of the data if possible."""
        if self.read_mode == "load":
            return len(self.current_data)
        elif self.read_mode == "stream":
            return None
        else:
            raise ValueError("JSONLDataHandler does not support read_mode: "
                             f"{self.read_mode}")

    def read_data(self):
        """Read JSONL data from a location on the disk."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"File does not exist: {self.data_path}")
        if self.read_mode == "load":
            # load the JSONL data from disk
            try:
                self.data = [json.loads(l) for l in open(self.data_path)]
            except:
                raise Exception("Could not parse JSONs in the file properly")
            self.current_data = copy.deepcopy(self.data)
        
        elif self.read_mode == "stream":
            # stream the JSONL data from disk
            self.current_data = open(self.data_path, "r")
        
        else:
            raise ValueError("JSONLDataHandler does not support read_mode: "
                             f"{self.read_mode}")
        
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
            # check if file is open
            if self.current_data.closed:
                return (False, {
                    "error_message": "ERROR: Reached end of file. Load the file again."
                })
            # file is open, so read a line
            # while an index is provided, this has nothing to do with the index
            line = self.current_data.readline()
            # nothing was read, so close the file
            if not line:
                self.current_data.close()
                return (False, {
                    "error_message": "ERROR: Reached end of file. Load the file again."
                })
            # found a non-empty line
            if line.strip():
                try:
                    self.current_item = json.loads(line)
                    self.current_index = new_index
                except json.JSONDecodeError:
                    return (False, {
                        "error_message": "ERROR: Invalid JSON format for the JSON."
                    })
                return (True, self.current_item)
            # found an empty line, so try again
            return self.get_item(new_index)
        
        else:
            raise ValueError(f"Invalid read_mode: {self.read_mode}")

    def _filter_data(self, filter_list_str: List[str], data: Any) -> Any:
        """
        Filter the data passed to it. 
        If successful -> return the filtered data
        If fails -> return a str explaining what went wrong
        """
        if self.read_mode == "stream":
            raise ValueError(f"Filter operation not allowed in stream mode")
        
        elif self.read_mode == "load":
            # curate filters
            for f in filter_list_str:
                try:
                    # dynamically create the lambda function
                    func = eval("lambda x: " + f)
                    data = list(filter(func, data))
                except:
                    # render appropriate error
                    return f"ERROR: Unable to apply filter: `{f}`"
            # check for empty data
            if len(data) == 0:
                return "ERROR: No items matching these filters."
            return data
        
        else:
            raise ValueError(f"Invalid read_mode: {self.read_mode}")
    
    def _sort_data(self, sort_list_str: List[str], data: Any) -> Any:
        """
        Sort the data passed to it. 
        If successful -> return the sorted data
        If fails -> return a str explaining what went wrong
        """
        if self.read_mode == "stream":
            raise ValueError(f"Sort operation not allowed in stream mode") 
        elif self.read_mode == "load":
            try:
                # create a tuple of keys
                combined_key = "("
                for sorting_key in sort_list_str:
                    combined_key += f"{sorting_key}, "
                combined_key = combined_key.rstrip(", ") + ")"
                # create a lambda out of the tuple of keys
                func = eval("lambda x: " + combined_key)
                # sort the data
                data = sorted(data, key=func)
                return data
            except:
                return "ERROR: Unable to sort using these keys."
        else:
            raise ValueError(f"Invalid read_mode: {self.read_mode}")

    def operate_on_data(
        self, 
        filter_list_str: List[str], 
        sort_list_str: List[str]
    ) -> Optional[Dict]:
        """
        Sort and filter the data. 
        Optionally return a dict explaining errors if any.
        """
        # make a fresh copy of original data
        # note this means that current copy of current_data is 
        # going to be lost
        data = copy.deepcopy(self.data)
        # filter data
        if len(filter_list_str):
            data = self._filter_data(filter_list_str, data)
            if isinstance(data, str):
                return {
                    "filter_error_message": data,
                    "filter_list": filter_list_str
                }

        # sort data
        if len(sort_list_str):
            data = self._sort_data(sort_list_str, data)
            if isinstance(data, str):
                return {
                    "sort_error_message": data,
                    "key_list": sort_list_str
                }

        # successfully filtered and sorted, so can update state and render
        del self.current_data
        self.current_data = data
        return None
