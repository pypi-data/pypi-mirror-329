"""
Absfuyu: Json Method
--------------------
``.json`` file handling

Version: 5.0.0
Date updated: 25/02/2025 (dd/mm/yyyy)
"""

# Module level
# ---------------------------------------------------------------------------
__all__ = ["JsonFile"]


# Library
# ---------------------------------------------------------------------------
import json
from pathlib import Path
from typing import Any

from absfuyu.core import BaseClass


# Class
# ---------------------------------------------------------------------------
class JsonFile(BaseClass):
    """
    ``.json`` file handling
    """

    def __init__(
        self,
        json_file_location: str | Path,
        *,
        encoding: str | None = "utf-8",
        indent: int | str | None = 4,
        sort_keys: bool = True,
    ) -> None:
        """
        json_file_location: json file location
        encoding: data encoding (Default: utf-8)
        indent: indentation when export to json file
        sort_keys: sort the keys before export to json file
        """
        self.json_file_location = Path(json_file_location)
        self.encoding = encoding
        self.indent = indent
        self.sort_keys = sort_keys
        self.data: dict[Any, Any] = {}

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.json_file_location.name})"

    def load_json(self) -> dict[Any, Any]:
        """
        Load ``.json`` file

        :returns: ``.json`` data
        :rtype: dict
        """
        with open(self.json_file_location, "r", encoding=self.encoding) as file:
            self.data = json.load(file)
        return self.data

    def save_json(self) -> None:
        """Save ``.json`` file"""
        json_data = json.dumps(self.data, indent=self.indent, sort_keys=self.sort_keys)
        with open(self.json_file_location, "w", encoding=self.encoding) as file:
            file.writelines(json_data)

    def update_data(self, data: dict[Any, Any]) -> None:
        """
        Update ``.json`` data without save

        :param data: ``.json`` data
        :type data: dict
        """
        self.data = data
