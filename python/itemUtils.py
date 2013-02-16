#!/usr/bin/env python

"""Provides MeuporgItem, a class to store meuporg items easily as well
as utilities to use them easily and to extract them from files.

"""

from collections import defaultdict
import os
import re



# !SECTION! The MeuporgItem class

class MeuporgItem:
    """Stores data corresponding to a given item:
       * location
       * name
       * description
    """

    # This static dictionnary is indexed by the files complete paths
    # and has lists of lists as its entries. It contains all the items
    # whose matches .*SECTION.
    project_structure = defaultdict(list)

    # An item is a string matching the following regex. Recall that an
    # item is made of uppercased letters, underscores and numbers (and
    # nothing else) enclosed between exclamation marks.
    item_regex = "!([A-Z_0-9]+)!"

    # A list containing all the types of items encountered during
    # execution. Useful to loop through the item nowns.
    item_names = []
    
    # If an item is within the middle of the code, i.e. not at the
    # beginning of its own line, it is consider "in-code". In this
    # case, it has the following string as its description.
    no_desc = "link"


    def __init__(self, line, location, line_index):
        """Creates a new instance and sets all of its arguments from
        the content of a line containing an item and appends the name
        of the item to item_names (if it was not already in).

        A line containing an item must contain self.item_regex. If it
        does, what is before the item is dropped and all that is after
        is used to initialise the description. However, if there is an
        alpha-numeric character before the item, the item is
        considered to be in-code so its description is set to
        NO_DESC.

        """
        self.location = location
        self.line_index = line_index
        self.name = re.findall(self.__class__.item_regex, line)[0]
        if self.name not in self.__class__.item_names:
            self.__class__.item_names.append(self.name)
        content = re.split(self.__class__.item_regex + "\W*", line)
        if re.match(("^\W*$"), content[0]) != None:
            self.description = ''.join(content[2:])
        else:
            self.description = self.__class__.no_desc

        if re.match(".*SECTION", self.name) != None:
            self.__class__.project_structure[self.location].append(self)


    def add_to_description(self, partial_desc):
        """Appends a partial description to the description
        attribute if the current description is not NO_DESC.

        We add a space to prevent two words from being concatenated.

        """
        if self.description != self.__class__.no_desc:
            self.description += " " + partial_desc



# !SECTION! Criteria to sort items

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
    


# !SECTION! Parse files and directories


def parse_file(path):
    """Returns a list containing all the items in the file at path.

    The way this function reads data is simple. The lines of the file
    are read one after another. If a line contains an item, i.e. an
    uppercased string of arbitrary length enclosed between '!', we
    initialise a new item. Then, we continue appending the next lines
    to the said description until the lines stop starting with a
    non-alpha-numeric character followed by a '!'.

    """

    recording = False
    line_index = 1
    result = []
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            if not recording:
                if (re.search(MeuporgItem.item_regex, line) != None):
                    location = path
                    it = MeuporgItem(line, location, line_index)
                    recording = True
            else:
                if (re.search(MeuporgItem.item_regex, line) != None):
                    result.append(it)
                    location = path
                    it = MeuporgItem(line, location, line_index)
                elif (re.match('\W*! *', line) != None):
                    it.add_to_description(re.split("\W*! *", line)[1])
                else:
                    result.append(it)
                    recording = False
            line_index += 1
    return result



def parse_directory(path=".",
                    include=[],
                    exclude=[],
                    include_backup_files=False,
                    include_hidden_files=False):
    """Parses a whole directory, looking for items in each file.

    Backup files, i.e. '#files#' and 'files~' as well as hidden files
    '.files' are not taken into account unless respectively
    include_backup_files and include_hidden_files are set to True.

    """

    result = []
    for dirname, dirnames, filenames in os.walk(path):
        for name in filenames:
            path = os.path.join(dirname, name)
            if (include != []):
                to_do = False
                for pattern in include:
                    if re.search(pattern, path):
                        to_do = True
            else:
                to_do = True
            for pattern in exclude:
                if re.search(pattern, path):
                    to_do = False
            if to_do:
                if not (
                        (not include_backup_files and (re.search("/.*[~#]", path) != None))
                        or
                        (not include_hidden_files and (re.search("/\.[^/]+", path) != None))
                ):
                    result += parse_file(path)
    return result


        
# !SECTION! Test suite


if (__name__ == "__main__"):

    # !SUBSECTION! Testing the MeuporgItem class

    BASIC_FORMAT = "!{0.name}!  {0.description} ({0.location}:{0.line_index})"
    print BASIC_FORMAT.format(MeuporgItem(
        "    // * !TODO! :! * blabla! And bla too!",
        "./here.txt",
        12
    ))
    print BASIC_FORMAT.format(MeuporgItem(
        "blabla bla !FIXREF! blabla! blabla",
        "./here/wait/no/actually/there.bla",
        1234
    ))
    print(MeuporgItem.item_names)


    # !SUBSECTION! Testing the Criteria class

    ITEM_LIST = [
        MeuporgItem("!TODO! blabla", "./bla/blu.cpp", 12),
        MeuporgItem("!IDEA! blabla", "./bla/blu/thing.java.cpp", 12),
        MeuporgItem("!TODO! blabla", "./class.hpp", 12)
    ]
    for item in ITEM_LIST:
        crit = Criteria(item)
        print(crit.possible_matches)
        print("matches TODO: {}".format(crit.match("TODO")))


    # !SUBSECTION! Testing the parsing functions
    
    index = 1
    for it in parse_directory(
            path="..",
            include=["org", "el", "md"],
            exclude=["readme"],
            include_backup_files=False,
            include_hidden_files=False):
        print("{item_number}. !{0.name}!  {0.description} ({0.location}:{0.line_index})".format(it, item_number=index))
        index += 1

