#!/usr/bin/env python

# We import the regex module to recognize the patterns we want
import re

# We also need to use CLI argments and list directories
import os

# An item is a string matching the following regex. Recall that an
# item is made of uppercased letters, underscores and numbers (and
# nothing else) enclosed between exclamation marks.
ITEM_REGEX = "!([A-Z_0-9]+)!"

# A line containing an item must thus match the following regex.
ITEM_LINE_REGEX = "^.*" + ITEM_REGEX + ".*$"


# We want the appearance of the tasks in the file to be easily
# customizable. Thus, we simply insert the relevant data in a string
# using "format". Here the said string:
ENTRY = "[[file:{location}][{description}]] ({location})"

# If an item is within the middle of the code, i.e. not at the
# beginning of its own line, it is consider "in-code". In this case,
# it has the following string as its description.
NO_DESC = "link"



class Item:
    """Stores data corresponding to a given item:
       * location
       * name
       * tasks
       * description
    """
    def __init__(self,line,location):
        """Creates a new instance and sets all of its arguments from
        the content of a line containing an item.

        A line containing an item must match ITEM_LINE_REGEX. If it
        does, what is before the item is dropped and all that is after
        (minus the first non alphanumerical characters) is used to
        initialise the description. However, if there is an
        alpha-numeric character before the item, the item is
        considered to be in-code so its description is set to NO_DESC.

        """
        self.location = location
        self.name = re.findall(ITEM_REGEX,line)[0]
        content = re.split(ITEM_REGEX + "\W*",line)
        if (re.match(("^\W*$"),content[0]) != None):
            self.description = ''.join(content[2:])
        else:
            self.description = NO_DESC


    def add_to_description(self,partial_desc):
        """Appends a partial description to the description
        attribute if the current description is not NO_DESC.

        We add a space to prevent two words from being concatenated.

        """
        if (self.description != NO_DESC):
            self.description += " " + partial_desc
        

    def to_entry(self):
        """Outputs a string corresponding to the entry. """
        return ENTRY.format(
            location    = self.location,
            name        = self.name,
            description = self.description,
        )







if (__name__ == "__main__"):
    print Item("    // * !TODO! :! * blabla! And bla too!","./here.txt:1").to_entry()
    print Item("blabla bla !FIXREF! blabla! blabla","./here/wait/no/actually/there.bla:123456").to_entry()
    
    
