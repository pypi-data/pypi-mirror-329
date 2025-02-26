import functools
import logging
import os

import yaml
import pathlib

from datetime import datetime

from singleton_decorator import singleton
from typing import List, Optional, Union

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
            raise ValueError("Must provide a configuration file")

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

                if "alt_names" in term:
                    self.lookup[term["name"]]["alt_names"] = term["alt_names"]

                if "def" in term:
                    self.lookup[term["name"]]["def"] = term["def"]

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

    @functools.lru_cache(maxsize=constants.LRU_CACHE_MAXSIZE)
    def is_valid(self, term: str, val: Union[str, int, float, bool]) -> bool:
        """Method to check if the value for the specified term is valid.

        Args:
            term (str): The term to check
            val (Union[str, int, float, bool]): The value to check

        Returns:
            bool: True if the value is valid, False otherwise
        """
        return self.is_value_valid(term, val)

    @functools.lru_cache(maxsize=constants.LRU_CACHE_MAXSIZE)
    def is_value_valid(self, term: str, val: Union[str, int, float, bool]) -> bool:
        """Method to check if the value for the specified term is valid.

        Args:
            term (str): The term to check
            val (Union[str, int, float, bool]): The value to check

        Returns:
            bool: True if the value is valid, False otherwise
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

    @functools.lru_cache(maxsize=constants.LRU_CACHE_MAXSIZE)
    def is_term_valid(self, term: str) -> bool:
        """Method to check whether the term exists in the controlled vocabulary.

        Args:
            term (str): The term to check

        Returns:
            bool: Whether the term exists in the controlled vocabulary
        """
        if term not in self.lookup:
            logging.error(f"Term '{term}' not found in lookup")
            return False
        return True

    @functools.lru_cache(maxsize=constants.LRU_CACHE_MAXSIZE)
    def get_alt_names(self, term: str) -> List[str]:
        """Retrieve the alternative names for the specified term.

        Args:
            term (str): The term to check

        Returns:
            List[str]: The alternative names for the term
        """
        if term not in self.lookup:
            logging.error(f"Term '{term}' not found in lookup")
            return False
        if "alt_names" in self.lookup[term]:
            return self.lookup[term]["alt_names"]
        return []

    @functools.lru_cache(maxsize=constants.LRU_CACHE_MAXSIZE)
    def get_definition(self, term: str) -> Optional[str]:
        """Retrieve the definition for the specified term.

        Args:
            term (str): The term to check

        Returns:
            Optional[str]: The definition for the term
        """
        if term not in self.lookup:
            logging.error(f"Term '{term}' not found in lookup")
            return False

        if "def" in self.lookup[term]:
            return self.lookup[term]["def"]

        return None
