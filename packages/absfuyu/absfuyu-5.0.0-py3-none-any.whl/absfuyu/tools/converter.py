"""
Absufyu: Converter
------------------
Convert stuff

Version: 5.0.0
Date updated: 11/02/2025 (dd/mm/yyyy)

Feature:
--------
- Text2Chemistry
- Str2Pixel
- Base64EncodeDecode
"""

# Module level
# ---------------------------------------------------------------------------
__all__ = [
    "Text2Chemistry",
    "Str2Pixel",
    "Base64EncodeDecode",
]


# Library
# ---------------------------------------------------------------------------
import base64
import math
import re
import string
from itertools import chain, combinations
from pathlib import Path
from typing import Self

from absfuyu.core import BaseClass, CLITextColor, versionadded
from absfuyu.logger import logger
from absfuyu.pkg_data import DataList, DataLoader
from absfuyu.util import set_min


# Class
# ---------------------------------------------------------------------------
@versionadded("3.0.0")
class Base64EncodeDecode(BaseClass):
    """
    Encode and decode base64
    """

    @staticmethod
    def encode(data: str) -> str:
        """Base64 encode"""
        return base64.b64encode(data.encode()).decode()

    @staticmethod
    def decode(data: str) -> str:
        """Base64 decode"""
        return base64.b64decode(data).decode()

    @staticmethod
    @versionadded("4.1.0")
    def encode_image(img_path: Path | str, data_tag: bool = False) -> str:
        """
        Encode image file into base64 string

        Parameters
        ----------
        img_path : Path | str
            Path to image

        data_tag : bool, optional
            Add data tag before base64 string, by default ``False``

        Returns
        -------
        str
            Encoded image
        """
        img = Path(img_path)
        with open(img, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode("utf-8")
        if data_tag:
            return f"data:image/{img.suffix[1:]};charset=utf-8;base64,{b64_data}"
        return b64_data


class ChemistryElement(BaseClass):
    """Chemistry Element"""

    def __init__(self, name: str, number: int, symbol: str, atomic_mass: float) -> None:
        """
        name: element name
        number: order in periodic table
        symbol: short symbol of element
        atomic_mass: atomic mass of element
        """
        self.name = name
        self.number = number
        self.symbol = symbol
        self.atomic_mass = atomic_mass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.symbol})"

    def to_dict(self) -> dict[str, str | int | float]:
        """
        Output content to dict

        :rtype: dict[str, str | int | float]
        """
        return {
            "name": self.name,
            "number": self.number,
            "symbol": self.symbol,
            "atomic_mass": self.atomic_mass,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | int | float]) -> Self:
        """
        Convert from ``dict`` data

        :param data: Dict data
        :type data: dict[str, str | int | float]
        :rtype: ChemistryElement
        """
        return cls(
            name=data["name"],  # type: ignore
            number=int(data["number"]),
            symbol=data["symbol"],  # type: ignore
            atomic_mass=float(data["atomic_mass"]),
        )


class Text2Chemistry(BaseClass):
    def __init__(self) -> None:
        self.data_location = DataList.CHEMISTRY

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def _load_chemistry_data(self) -> list[ChemistryElement]:
        """
        Load chemistry pickle data
        """
        data: list[dict] = DataLoader(self.data_location).load()
        return [ChemistryElement.from_dict(x) for x in data]

    @property
    def unvailable_characters(self) -> set[str]:
        """
        Characters that can not be converted (unvailable chemistry symbol)

        :rtype: set[str]
        """
        base = set(string.ascii_lowercase)
        available = set(
            "".join(map(lambda x: x.symbol.lower(), self._load_chemistry_data()))
        )
        # logger.debug(base)
        # logger.debug(available)
        return base.difference(available)

    def convert(self, text: str) -> list[list[ChemistryElement]] | list:
        """
        Convert text to chemistry symbol

        :param text: desired text
        :type text: str
        :returns: Converted text (empty list when failed to convert)
        :rtype: list
        """
        # Check if `text` is a word (without digits)
        is_word_pattern = r"^[a-zA-Z]+$"
        if re.search(is_word_pattern, text) is None:
            logger.error("Convert Failed. Word Only!")
            raise ValueError("Convert Failed. Word Only!")
        for x in self.unvailable_characters:
            if text.find(x) != -1:
                logger.debug(
                    f"{text} contains unvailable characters: {self.unvailable_characters}"
                )
                # raise ValueError(f"Text contains {self.unvailable_character}")
                return []

        # Setup
        text_lower = text.lower()
        data = self._load_chemistry_data()

        # List possible elements
        possible_elements: list[ChemistryElement] = []
        for i, letter in enumerate(text_lower):
            for element in data:
                if element.symbol.lower().startswith(
                    letter
                ):  # Check for `element.symbol` starts with `letter`
                    # logger.debug(f"{letter} {element}")
                    if element.symbol.lower().startswith(
                        text_lower[i : i + len(element.symbol)]
                    ):  # Check for `element.symbol` with len > 1 starts with `letter` of len(element.symbol)
                        possible_elements.append(element)
                    # Break when reach last letter in text
                    if letter == text_lower[-1]:
                        break
        logger.debug(possible_elements)
        if len(possible_elements) < 1:  # No possible elements
            return []

        # temp = []
        # for i in range(min_combination_range, len(text_lower)+1):
        #     comb = combinations(possible_elements, i)
        #     temp.append(comb)
        # possible_combinations = chain(*temp)
        max_symbol_len = max(
            map(lambda x: len(x.symbol), possible_elements)
        )  # Max len of `element.symbol`
        min_combination_range = math.ceil(len(text_lower) / max_symbol_len)
        logger.debug(f"Combination range: [{min_combination_range}, {len(text_lower)}]")
        possible_combinations = chain(
            *(
                combinations(possible_elements, i)
                for i in range(min_combination_range, len(text_lower) + 1)
            )
        )
        # logger.debug(list(possible_combinations))

        output = []
        for comb in possible_combinations:
            merged = "".join(map(lambda x: x.symbol, comb))
            if text_lower == merged.lower():
                output.append(list(comb))
                logger.debug(f"Found: {merged}")

        return output

    @staticmethod
    @versionadded("4.2.0")
    def beautify_result(
        result: list[list[ChemistryElement]] | list,
    ) -> str:
        """
        Beautify the result from ``Text2Chemistry.convert()``

        Parameters
        ----------
        result : list[list[ChemistryElement]] | list
            Convert ``Text2Chemistry.convert()`` result

        Returns
        -------
        str
            Beautified output
        """
        if len(result) == 0:
            res = "No possible combination"
        else:
            msg = []
            for i, solution in enumerate(result, start=1):
                max_word_len = max([len(x.name) for x in solution])
                msg.append(f"Option {i:02}: {', '.join([x.symbol for x in solution])}")
                for x in solution:
                    msg.append(
                        f"{x.symbol.ljust(2)} ({x.number:02}. {x.name.ljust(max_word_len)} - {round(x.atomic_mass, 2)})"
                    )
                msg.append("---")
            res = "\n".join(msg)
        return res


class Str2Pixel(BaseClass):
    """Convert str into pixel"""

    PIXEL = "\u2588"

    def __init__(
        self,
        str_data: str,
        *,
        pixel_size: int = 2,
        pixel_symbol_overwrite: str | None = None,
    ) -> None:
        """
        Parameters
        ----------
        str_data : str
            Pixel string data (Format: ``<number_of_pixel><color_code>``)
            Example: 50w20b = 50 white pixels and 20 black pixels

        pixel_size : int, optional
            Pixel size, by default ``2``

        pixel_symbol_overwrite : str | None, optional
            Overwrite pixel symbol, by default ``None``
        """
        self.data = str_data
        if pixel_symbol_overwrite is None:
            self.pixel = self.PIXEL * int(set_min(pixel_size, min_value=1))
        else:
            self.pixel = pixel_symbol_overwrite

    def _extract_pixel(self):
        """Split str_data into corresponding int and str"""
        num = re.split("[a-zA-Z]", self.data)  # type: ignore
        num = filter(lambda x: x != "", num)  # type: ignore # Clean "" in list
        num = list(map(int, num))  # type: ignore
        char = re.split("[0-9]", self.data)
        char = filter(lambda x: x != "", char)  # type: ignore
        return [x for y in zip(num, char) for x in y]

    def convert(self, line_break: bool = True) -> str:
        """Convert data into pixel

        Parameters
        ----------
        line_break : bool, optional
            Add ``\\n`` at the end of line, by default ``True``

        Returns
        -------
        str
            Converted colored pixels
        """
        # Extract pixel
        pixel_map = self._extract_pixel()

        # Translation to color
        translate = {
            "w": CLITextColor.WHITE,
            "b": CLITextColor.BLACK,
            "B": CLITextColor.BLUE,
            "g": CLITextColor.GRAY,
            "G": CLITextColor.GREEN,
            "r": CLITextColor.RED,
            "R": CLITextColor.DARK_RED,
            "m": CLITextColor.MAGENTA,
            "y": CLITextColor.YELLOW,
            "E": CLITextColor.RESET,
            "N": "\n",  # New line
        }

        # import colorama
        # translate = {
        #     "w": colorama.Fore.WHITE,
        #     "b": colorama.Fore.BLACK,
        #     "B": colorama.Fore.BLUE,
        #     "g": colorama.Fore.LIGHTBLACK_EX, # Gray
        #     "G": colorama.Fore.GREEN,
        #     "r": colorama.Fore.LIGHTRED_EX,
        #     "R": colorama.Fore.RED, # Dark red
        #     "m": colorama.Fore.MAGENTA,
        #     "y": colorama.Fore.YELLOW,
        #     "E": colorama.Fore.RESET,
        #     "N": "\n", # New line
        # }

        # Output
        out = ""
        for i, x in enumerate(pixel_map):
            if isinstance(x, str):
                temp = self.pixel * pixel_map[i - 1]
                out += f"{translate[x]}{temp}{translate['E']}"
        if line_break:
            return out + "\n"
        else:
            return out
