import logging
import os

import yaml
import pathlib

from datetime import datetime

from singleton_decorator import singleton
from typing import Union

from controlled_vocabulary_utils import constants
from controlled_vocabulary_utils.file_utils import check_infile_status


@singleton
class Manager:
    """Class for managing the controlled vocabulary utilities."""

    def __init__(self, **kwargs):
        """Constructor for class Manager"""
        self.config_file = kwargs.get("config_file", None)
        self.verbose = kwargs.get("outdir", constants.DEFAULT_VERBOSE)

        if self.config_file is None:
            raise ValueError(f"Must provide a configuration file")

        check_infile_status(self.config_file)

        logging.info(
            f"Will attempt to load contents of config file '{self.config_file}'"
        )
        self.config = yaml.safe_load(pathlib.Path(self.config_file).read_text())

        self.lookup = {}
        self._load_lookup()

        logging.info(f"Instantiated Manager in {os.path.abspath(__file__)}")

    def _load_lookup(self) -> None:

        ctr = 0

        for term in self.config["terms"]:

            ctr += 1

            logging.info(f"Processing term '{term['name']}'")

            if term["name"] not in self.lookup:

                self.lookup[term["name"]] = {}

                has_rule = False
                if "accepted_values" in term:
                    self.lookup[term["name"]]["accepted_values"] = term[
                        "accepted_values"
                    ]
                    has_rule = True

                if "regex" in term:
                    self.lookup[term["name"]]["regex"] = term["regex"]
                    has_rule = True

                if not has_rule:
                    self.lookup[term["name"]] = None

        logging.info(f"Loaded {ctr} terms into lookup")

    def is_valid(self, term: str, val: Union[str, int, float, bool]) -> bool:
        """Method to check if the value for the specified term is valid.

        Args:
            term (str): The term to check
            val (Union[str, int, float, bool]): The value to check

        """
        if term not in self.lookup:
            logging.error(f"Term '{term}' not found in lookup")
            return False

        if "accepted_values" in self.lookup[term]:
            if val not in self.lookup[term]["accepted_values"]:
                logging.error(
                    f"Value '{val}' not found in accepted values for term '{term}'"
                )
                return False

        if "regex" in self.lookup[term]:
            if not self.lookup[term]["regex"].match(val):
                logging.error(f"Value '{val}' does not match regex for term '{term}'")
                return False

        return True
