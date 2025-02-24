"""Functions set for pollenflug.

Functions:
    loadconfig(config_location): loads the config file, returns default values if not available.
    print_help(): prints a standard help dialog.
    def print_calendar(data, eng): loops through data received from request and prints.
"""

import sys
import os

# For dict/r.json type hinting
from typing import Dict

# Parser for INI config files and homedir
import configparser
from pathlib import Path

# local
from .consts import ENG_LIST
from .color import Color


def loadconfig(config_location: str) -> (int, bool, bool):
    """Loads the config file, returns default values if not available.

    Input Arguments: absolute directory of the config file.
    Returns: postal code, language flag and debug option.
    """

    # Test if the file given exists. If not, return default vals.
    if not Path(config_location).exists():
        return 20095, True, False

    # Load config file
    config = configparser.ConfigParser()
    config.read(config_location)

    # Check config file for postal code, and set appropriately
    try:
        plz = int(config["DEFAULT"]["plz"])
    except (TypeError, KeyError):
        # plz not defined in config file, use default
        plz = 20095
    except ValueError:
        print(Color.format_color("Error") + ": invalid postal code in config!")
        sys.exit(os.EX_CONFIG)

    # Check config file for debug flag, and set appropriately
    try:
        debug_str = config["DEFAULT"]["debug"].lower()
        if debug_str in ("true", "1"):
            debug = True
        elif debug_str in ("false", "0", ""):
            debug = False
        else:
            print(Color.format_color("Error") + ": invalid debug flag in config!")
            sys.exit(os.EX_CONFIG)
    except KeyError:
        # Don't fail on undefined
        debug = False

    # Check config file for english flag, and set if given.
    try:
        eng = config["DEFAULT"]["en"].lower()
        if eng in ("true", "1"):
            use_eng = True
        elif eng in ("false", "0", ""):
            use_eng = False
        else:
            print(Color.format_color("Error") + ": invalid language flag in config!")
            sys.exit(os.EX_CONFIG)
    except KeyError:
        # Don't fail on undefined
        use_eng = False

    return plz, use_eng, debug


def print_help() -> None:
    """Print help menu with argument, usage, copyright and Github.

    Input Arguments: None
    Returns: None
    """
    print(
        """Usage: pollenflug.py [options]

    -h,--help               Print this help menu
    -d,--date=YYYY-MM-DD    Set start date of pollen calendar
    -p,--plz=iiiii          Set postal code/plz
    -e,--english            Print plant names in English
    -v,--verbose            Print verbose


By default, date is set to today and plz to Hamburg.
Data is fetched from Hexal's Pollenflugkalendar.

pollenflug  Copyright (C) 2022  Bader Zaidan
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions; read LICENSE for details.

For bug reports and feature requests, see:
https://github.com/BaderSZ/pollenflug"""
    )


def print_calendar(data: Dict, eng: bool = False) -> None:
    """Print calendar as a table with appropriate spacing.

    Input Arguments: `data: dict` from URL request., language flag.
    Returns: None.
    """
    # Print top Bar:
    print("Date", end="\t\t")
    if eng:
        for string in ENG_LIST:
            print(string[:6], end="\t")
    else:
        for string in data["content"]["pollen"]:
            print(string[:6], end="\t")
    print()  # Newline

    # Loop, print for every date
    for string in data["content"]["values"]:
        cdate = string
        print(cdate, end="\t")
        for val in data["content"]["values"][cdate]:
            print(Color.format_color(val, Color(val)), end="\t")
        print()  # Newline
