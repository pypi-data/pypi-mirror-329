import copy
import glob
import os
from typing import Dict, List, Optional, Tuple

from datasets import Dataset, load_dataset

from .base import DataHandler


class HFDataHandler(DataHandler):
    def __init__(self, data_path: str, read_mode: str, 
                 split: Optional[str] = None,
                 cache_dir: Optional[str] = None,
                 config_name: Optional[str] = None):
        super().__init__(data_path, read_mode)
        self.split = split
        self.config_name = config_name
        self.cache_dir = cache_dir

    def data_size(self) -> Optional[int]:
        """Return the size of the data if possible."""
        if self.read_mode == "load":
            return len(self.current_data)
        elif self.read_mode == "stream":
            return None
        else:
            raise ValueError("HFDataHandler does not support read_mode: "
                             f"{self.read_mode}")

    def read_data(self):
        """Read HF data."""
        if os.path.exists(self.data_path):
            # loading the local dataset. 
            # NOTE: assumes that the dataset is stored as .parquet files
            data_files = glob.glob(os.path.join(self.data_path, "*.parquet"))
            if len(data_files) == 0:
                raise RuntimeError(f"{self.data_path} contains no .parquet "
                                    "file and only .parquet files are supported.")
            # attempt to load from local disk
            if self.read_mode == "load":
                # load the HF data from disk
                self.data = load_dataset(
                    "parquet", data_files=data_files, split=self.split,
                    cache_dir=self.cache_dir
                )
                self.current_data = copy.deepcopy(self.data)
            
            elif self.read_mode == "stream":
                # stream the HF data from disk
                self.data = load_dataset(
                    "parquet", data_files=data_files, split=self.split, 
                    streaming=True, cache_dir=self.cache_dir
                )
                self.iterator = iter(self.data)
            
            else:
                raise ValueError("HFDataHandler does not support read_mode: "
                                f"{self.read_mode}")
        else:
            try:
                # attempt obtaining the dataset from the web
                if self.read_mode == "load":
                    # load the dataset
                    self.data = load_dataset(
                        self.data_path, split=self.split, cache_dir=self.cache_dir,
                        name=self.config_name
                    )
                    self.current_data = copy.deepcopy(self.data)
                elif self.read_mode == "stream":
                    # stream the dataset
                    self.data = load_dataset(
                        self.data_path, split=self.split, cache_dir=self.cache_dir,
                        name=self.config_name, streaming=True
                    )
                    self.iterator = iter(self.data)
                else:
                    raise ValueError("HFDataHandler does not support read_mode: "
                                    f"{self.read_mode}")
            except Exception as e:
                raise RuntimeError(f"Unable to load dataset from {self.data_path}. "
                                   "It's possible that loading this dataset is not supported.\n\n"
                                   f"Faced this error when attempting to load: {e}")

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
                self.current_item = next(self.iterator)
                self.current_index = new_index
                return (True, self.current_item)
            except:
                return (False, {
                    "error_message": "ERROR: Reached end of file. Load the file again."
                })
        else:
            raise ValueError(f"Invalid read_mode: {self.read_mode}")

    def _filter_data(self, filter_list_str: List[str], data: Dataset) -> Dataset:
        """
        Filter the data passed to it. 
        If successful -> return the filtered data
        If fails -> return a str explaining what went wrong
        """
        # curate filters
        for f in filter_list_str:
            try:
                # dynamically create the lambda function
                func = eval("lambda x: " + f)
                data = data.filter(func)
            except:
                # render appropriate error
                return f"ERROR: Unable to apply filter: `{f}`"
        # check for empty data
        if self.read_mode == "load":
            if len(data) == 0:
                return "ERROR: No items matching these filters."
        elif self.read_mode == "stream":
            # try to get an item after streaming
            iterator = iter(data)
            try:
                next(iterator)
            except StopIteration:
                return "ERROR: No items matching these filters."
            except:
                return "ERROR: Unable to apply filters. Something went wrong while streaming."
        else:
            raise ValueError(f"Invalid read_mode: {self.read_mode}")
        return data
    
    def _sort_data(self, sort_list_str: List[str], data: Dataset) -> Dataset:
        """
        Sort the data passed to it. 
        If successful -> return the sorted data
        If fails -> return a str explaining what went wrong
        """
        if self.read_mode == "stream":
            raise ValueError(f"Sort operation not allowed in stream mode") 
        elif self.read_mode == "load":
            try:
                # map the data to have keys
                sorting_keys = [f"__key__{i}__" for i in range(len(sort_list_str))]
                mapped = data.map(lambda x: {
                    sorting_keys[i]: eval(sort_list_str[i], {}, {"x": x}) 
                                     for i in range(len(sort_list_str))
                })
                # sort with keys
                sorted = mapped.sort(sorting_keys)
                data = sorted.remove_columns(sorting_keys)
                # remove the keys from sorted
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
        
        # for load mode it means copying the data itself
        if self.read_mode == "load":
            data = copy.deepcopy(self.data)
        # for stream mode it means creating a new iterator over the original data
        elif self.read_mode == "stream":
            self.read_data()
            data = self.data

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
        if self.read_mode == "load":
            del self.current_data
            self.current_data = data
        elif self.read_mode == "stream":
            del self.iterator
            self.data = data
            self.iterator = iter(self.data)
        
        return None
