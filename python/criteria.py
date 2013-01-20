#!/usr/bin/env python

"""Provides the Criteria class to extract useful info from MeuporgItems"""

import os.path
import re
from item import MeuporgItem

class Criteria:
    """Extracts useful data from an item and provides a method to see
    if an item belongs in a given category, i.e. if it is semantically
    connected with a given string.

    Example: "!TODO! I must do that" at line 33 of file
    ./thing/stuff/bla.class.java is connected with the strings:
    "TODO", "thing", "stuff", "bla.class", ".java".

    """
    

    def __init__(self, meuporg_item):
        """Extract useful data from the item.

        We slice the path to get all the folders' names and the file's
        name, possibly remove the starting ".".

        Example: Criteria(
                   MeuporgItem("!TODO! bla","./thing/stuff/class.hpp")
                 ).possible_matches = ['TODO','thing','stuff','class.hpp']

        """
        path, file_name = list(os.path.split(meuporg_item.location))
        path_strings = path.split(os.path.sep)
        if path_strings[0] == ".":
            path_strings = path_strings[1:]
        self.possible_matches = (
            [meuporg_item.name]
            + path_strings
            + [file_name]
            )


    def match(self, criteria_value):
        """Check if the item studied matches the Criteria_value
        regex.

        """
        for possibility in self.possible_matches:
            if re.search(criteria_value, possibility) != None:
                return True
        return False
    

if __name__ == "__main__":
    # Basic test for the Criteria class
    ITEM_LIST = [
        MeuporgItem("!TODO! blabla", "./bla/blu.cpp", 12),
        MeuporgItem("!IDEA! blabla", "./bla/blu/thing.java.cpp", 12),
        MeuporgItem("!TODO! blabla", "./class.hpp", 12)
    ]
    for item in ITEM_LIST:
        crit = Criteria(item)
        print(crit.possible_matches)
        print("matches TODO: {}".format(crit.match("TODO")))
