import copy
import json
import random
from pprint import pformat
from typing import Dict, List, Optional

from flask import render_template

from datahawk.data_handler import (DataHandler, HFDataHandler, 
                                   JSONDataHandler, JSONLDataHandler)


class Datahawk:
    """
    An interface between the UI and the data handler. This class maintains what
    the user wants/sees and talks to the data handler to maintain or update
    this state.
    """
    def __init__(self, data_path: str, read_mode: str, source: str, 
                 split: Optional[str] = None,
                 config_name: Optional[str] = None,
                 cache_dir: Optional[str] = None):
        # data handler and metadata
        self.data_path: str = data_path
        self.read_mode: str = read_mode
        self.source: str = source
        self.split: Optional[str] = split
        self.config_name: Optional[str] = config_name
        self.handler: DataHandler = self._get_handler(
            data_path, read_mode, source, 
            split=split, config_name=config_name,
            cache_dir=cache_dir
        )
        # state
        self.current_index: int = None                          # index of item being rendered
        self.current_item: Optional[Dict] = None                # current item being rendered
        self.filter_list_str: List[str] = []                    # filters to filter with
        self.key_list_str: List[str] = []                       # keys to sort data with
        self.is_filtered_data: bool = False                     # is data filtered?
        self.is_sorted_data: bool = False                       # is data sorted?
        # read the data and render initial sample
        try:
            self.handler.read_data()
            self._setup()
        except:
            # handler raises an error during the read operation
            raise


    def render(self):
        """Render the template with the current state"""
        return self._update_index_and_render()
    

    def _setup(self):
        """Setup the state"""
        self.new_index: Optional[int] = 0
        self.data_size: Optional[int] = self.handler.data_size()
        self.can_filter: bool = False
        self.can_sort: bool = False
        # handle individual cases
        if self.read_mode == "load":
            self.can_filter, self.can_sort = True, True
        elif self.read_mode == "stream":
            if self.source == "hf":
                self.can_filter = True


    def _get_handler(self, data_path: str, read_mode: str, source: str, 
                     split: Optional[str] = None,
                     cache_dir: Optional[str] = None,
                     config_name: Optional[str] = None) -> DataHandler:
        """Route to specific DataHandler based on the request"""
        if source == "jsonl":
            return JSONLDataHandler(data_path, read_mode)
        elif source == "json":
            return JSONDataHandler(data_path, read_mode)
        elif source == "hf":
            return HFDataHandler(data_path, read_mode, split=split,
                                 cache_dir=cache_dir, config_name=config_name)
        else:
            raise NotImplementedError("Datahawk does not support source "
                                      f"{source}.")
        

    def _prepare_rendering_args(self):
        return {
            "json_entry": json.dumps(
                self.prepare_for_rendering(self.current_item),
                indent=4
            ),
            "data_path": self.data_path,
            "data_size": self.handler.data_size(),
            "index": self.current_index,
            "filter_list": self.filter_list_str,
            "key_list": self.key_list_str,
            "is_filtered_data": self.is_filtered_data,
            "is_sorted_data": self.is_sorted_data,
            "read_mode": self.read_mode,
            "can_filter": self.can_filter,
            "can_sort": self.can_sort
        }


    def _update_index_and_render(self) -> str:
        """Update the viewing index and render the template"""
        # attempt to get next item
        ok, item = self.handler.get_item(self.new_index)

        # if fails render error
        if not ok:
            # do not update the index
            # `item` contains an error message
            self.new_index = None
            return self.render_error(item)
        
        # got an item, so render it now
        # update all variables before rendering
        # clear out new_index after copying over to current_index
        self.current_index = self.new_index
        self.new_index = None
        self.current_item = item
        # render
        rendering_args = self._prepare_rendering_args()
        return render_template("item.html", **rendering_args)


    @staticmethod
    def prepare_for_rendering(json_item: Dict) -> Dict:
        """Take `json_item` and convert it into a format 
        such that it can be rendered. Currently this involves:
            1. Converting all values to appropriate strings
        Will return a deep copy of `json_item` and leave `data` unmodified."""
        x = copy.deepcopy(json_item)
        for k in x:
            if (
                isinstance(x[k], str) or isinstance(x[k], int) or 
                isinstance(x[k], float) or isinstance(x[k], bool)
            ):
                # convert to string
                x[k] = str(x[k])
            else:
                # let pprint format the output
                x[k] = pformat(x[k], width=100, compact=False)
        return x


    def render_error(self, error_dict: Dict) -> str:
        """Render an error message. `error_dict` should at least contain 
        one error with the key indicating the type of error message and the
        value being the error message to render. `error_dict` can update 
        other fields in the render as well.
        
        Note: the front-end logic will look at the key of the error and handle 
        it accordingly. For example, if the error name is `filter_error_message`
        then the error will be shown in the Filters box appropriately, and so on."""

        # sanity checks
        if not isinstance(error_dict, Dict):
            raise ValueError("error_dict should be a dictionary")
        if len(error_dict) == 0:
            raise ValueError("error_dict should have at least one key")
        _error_in_dict = False
        for key in error_dict:
            if "error" in key:
                _error_in_dict = True
                break
        if not _error_in_dict:
            raise ValueError("error_dict should have at least one '*error*' key")

        # set default render_args
        # render
        rendering_args = self._prepare_rendering_args()
        # update with error_dict to override any existing keys
        # and add the error message
        rendering_args.update(error_dict)
        return render_template("item.html", **rendering_args)
    

    def user_update_index(self, new_index: str) -> str:
        """Update to a user specified index"""
        try:
            self.new_index = int(new_index)
        except:
            # simulate error condition
            self.new_index = self.handler.data_size()
        return self._update_index_and_render()


    def random_json(self) -> str:
        """Update to a random item"""
        self.new_index = random.choice(range(self.handler.data_size()))
        return self._update_index_and_render()


    def first_item(self) -> str:
        """Update to the first item"""
        self.new_index = 0
        return self._update_index_and_render()


    def previous_item(self) -> str:
        """Update to the previous item"""
        self.new_index = self.current_index - 1
        return self._update_index_and_render()


    def next_item(self) -> str:
        """Update to the next item"""
        self.new_index = self.current_index + 1
        return self._update_index_and_render()


    def last_item(self) -> str:
        """Update to the last item"""
        self.new_index = self.handler.data_size() - 1
        return self._update_index_and_render()
    

    def operate_on_data(
        self, 
        filter_list_str: Optional[List[str]], 
        key_list_str: Optional[List[str]]
    ) -> str:
        """Curate the filter and sort list if needed and invoke the handler to 
        operate on the data."""
        is_filtered_data, is_sorted_data = False, False
        # operate on the data
        error_dict = self.handler.operate_on_data(
            filter_list_str, key_list_str
        )
        # render errors if any
        if error_dict:
            return self.render_error(error_dict)
        # successfully sorted and filtered, so render as such
        if filter_list_str:
            is_filtered_data = True
        if key_list_str:
            is_sorted_data = True
        self.filter_list_str = filter_list_str
        self.key_list_str = key_list_str
        self.is_filtered_data = is_filtered_data
        self.is_sorted_data = is_sorted_data
        self.new_index = 0
        return self._update_index_and_render()
    

    def filter_data(self, filter_list_str: List[str]) -> str:
        """Filter data"""
        return self.operate_on_data(filter_list_str, self.key_list_str)
    

    def sort_data(self, key_list_str: str) -> str:
        """Sort data"""
        return self.operate_on_data(self.filter_list_str, key_list_str)
