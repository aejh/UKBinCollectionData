#!/usr/bin/env python3
"""Get UK bin collection data.
"""
import importlib
import os
import sys
from glob import glob
from typing import List
from pathlib import Path

from get_bin_data import AbstractGetBinDataClass

# We use this method to dynamically import the council processor
SRC_PATH = os.path.join("councils")
module_path = os.path.realpath(os.path.join(os.path.dirname(__file__), SRC_PATH))
sys.path.append(module_path)

# Example using pathlib, used in list_councils()
councils = Path(__file__).parent / "councils"


def list_councils() -> List[str]:
    """List the names of the councils for which a collection service exists."""
    return [c.stem for c in councils.glob("*.py") if not c.name.startswith("_")]


def client_code(get_bin_data_class: AbstractGetBinDataClass, address_url: str) -> None:
    """
    The client code calls the template method to execute the algorithm. Client
    code does not have to know the concrete class of an object it works with,
    as long as it works with objects through the interface of their base class.
    """

    get_bin_data_class.template_method(address_url)


if __name__ == "__main__":
    from argparse import ArgumentParser, RawDescriptionHelpFormatter

    parser = ArgumentParser(
        # This pulls the description from this file's docstring
        description=__doc__.lstrip(),
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "council",
        help=f"The name of the council. One of: {', '.join(list_councils())}",
    )
    parser.add_argument(
        "url",
        help="The data URL",
    )
    args = parser.parse_args()

    council_module = importlib.import_module(args.council)
    client_code(council_module.CouncilClass(), args.url)
