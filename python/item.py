#!/usr/bin/env python

"""Provides MeuporgItem, a class to store meuporg items easily."""


import re


class MeuporgItem:
    """Stores data corresponding to a given item:
       * location
       * name
       * description
    """

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


    def add_to_description(self, partial_desc):
        """Appends a partial description to the description
        attribute if the current description is not NO_DESC.

        We add a space to prevent two words from being concatenated.

        """
        if self.description != self.__class__.no_desc:
            self.description += " " + partial_desc
        



if (__name__ == "__main__"):
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
