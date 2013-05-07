#!/usr/bin/env python

"""Provides MeuporgItem, a class to store meuporg items easily as well
as utilities to use them easily and to extract them from files.

"""

from collections import defaultdict
import os
import re




# !SECTION! The Context class


class Context:
    """Contains a description of the current context of the state: which
    file are we looking at, which line and which section/subsection/etc.

    """
    

    def __init__(self):
        """Initializes a new empty context."""
        self.updateFile("")


    def updateFile(self, path):
        """Modifies the current_file attribute to path and resets other
        attributes.

        """
        self.current_file    = path
        self.sections_stack  = []
        self.line_index      = 0
        self.new_item        = False
        self.continuing_item = False
        self.finished_item   = False
        self.is_heading      = False


    def update(self, line):
        """Updates the context depending on the line."""

        self.line_index += 1
        self.line = line

        if (re.search(MeuporgItem.__item_regex__, line) != None):
            # case where we have a new item
            if self.new_item or self.continuing_item:
                self.finished_item = True
            self.continuing_item = False
            depth, heading = self.struct_item(line)
            if depth != 0:
                # if it corresponds to a structural indication, we update
                self.is_heading = True
                if depth == len(self.sections_stack):
                    # if the new heading is at the same depth as the
                    # previous one, we remove the previous one
                    self.sections_stack.pop()
                elif depth < len(self.sections_stack):
                    # if it has a smaller depth, we remove all
                    # headings with greater depth.
                    for i in range(0, len(self.sections_stack) - depth + 1):
                        self.sections_stack.pop()
                self.sections_stack.append(heading)
            self.new_item = True

        elif self.new_item and (re.match('\W*! *', line) != None):
            # case where we previously had a new item and the new line
            # starts with '!'
            self.new_item = False
            self.continuing_item = True
            self.finished_item = False
            self.is_heading = False

        elif self.continuing_item and not (re.match('\W*! *', line) != None):
            # case were we had a continued item but don't have it anymore
            self.continuing_item = False
            self.finished_item = True
            self.is_heading = False

        elif self.new_item or self.continuing_item:
            # case where we had an item previously, but not anymore
            self.finished_item = True
            self.new_item = False
            self.continuing_item = False
            self.is_heading = False

        else:
            # case where nothing happens
            self.new_item = False
            self.continuing_item = False
            self.is_heading = False


    # The regex corresponding to short structural items
    __struct_regex_short__ = "!LEV[0-9]+!"

    # The regex corresponding to LaTeX-style structural items
    __struct_regex_latex__ = "!.*SECTION!"
    

    def struct_item(self, line):
        """If this line contains a structural items, returns its depth
        and its heading in a two entries list.

        Structural items are items matching one of the regexes in:
        + __struct_regex_latex__
        + __struct_regex_short__

        """
        if re.search(self.__class__.__struct_regex_short__, line) != None:
            depth = int( re.findall("[0-9]+", line)[0] )
            content = re.split(self.__class__.__struct_regex_short__ + "\W*", line)
            heading = content[1]
        elif re.search(self.__class__.__struct_regex_latex__, line) != None:
            name = re.findall(self.__class__.__struct_regex_latex__, line)[0]
            # name should match (SUB)*SECTION, so we simply compute
            # the number of "sub" directly from the length of it
            depth = (len(name) - 4)/3
            content = re.split("!\W*", line)
            heading = "".join(content[2:])
        else:
            depth = 0
            heading = "name"

        return [depth, heading]



# !SECTION! The MeuporgItem class

class MeuporgItem:
    """Stores data corresponding to a given item:
       * title       : the type of the item (what's between the !'s).
       * description : the text accompanying the item (if any).
       * file_name   : the path to the file it is in.
       * sections    : the list of the imbricated sections it is in.
    """

    # A list of all the items found during this execution
    __item_list__ = []

    # An item is a string matching the following regex. Recall that an
    # item is made of uppercased letters, underscores and numbers (and
    # nothing else) enclosed between exclamation marks.
    __item_regex__ = "!([A-Z_0-9]+)!"

    # A list containing all the types of items encountered during
    # execution. Useful to loop through the item names.
    __item_names__ = []
    
    # If an item is within the middle of the code, i.e. not at the
    # beginning of its own line, it is consider "in-code". In this
    # case, it has the following string as its description.
    __no_desc__ = "link"
    

    def __init__(self, line, file_name, line_index, sections, is_heading):
        """Creates a new instance and sets all of its arguments from
        the content of a line containing an item and appends the name
        of the item to __item_names__ (if it was not already in).

        A line containing an item must contain self.__item_regex__. If it
        does, what is before the item is dropped and all that is after
        is used to initialise the description. However, if there is an
        alpha-numeric character before the item, the item is
        considered to be in-code so its description is set to
        __no_desc__.

        """
        self.file_name  = file_name
        self.line_index = line_index
        self.sections   = sections
        self.is_heading = is_heading
        self.name = re.findall(self.__class__.__item_regex__, line)[0]
        if self.name not in self.__class__.__item_names__:
            self.__class__.__item_names__.append(self.name)
        content = re.split(self.__class__.__item_regex__ + "\W*", line)
        if re.match(("^\W*$"), content[0]) != None: # "incode" case
            self.description = ''.join(content[2:])
        else:
            self.description = self.__class__.__no_desc__

    def add_to_description(self, partial_desc):
        """Appends a partial description to the description
        attribute if the current description is not __no_desc__.

        We add a space to prevent two words from being concatenated.

        """
        if self.description != self.__class__.__no_desc__:
            self.description += " " + partial_desc

    def is_section_heading(self):
        """Returns True if this item corresponds to a section heading, False
        otherwise.

        """
        return self.is_heading


    def push_to_list(self):
        """Appends this item to the static list of items."""
        self.__class__.__item_list__.append(self)


    @staticmethod
    def get_item(context):
        """Returns an item using the information from a Context
        instance.

        Note that we pass a copy of the sections stack, not the list
        itself as it is modified afterwards.

        """
        return MeuporgItem(
            context.line,
            context.current_file,
            context.line_index,
            context.sections_stack[:],
            context.is_heading)



# !SECTION! Parse files and directories


def parse_file(path, context):
    """Updates the list containing all the items with those in the file at
    path, where the context is given by the context parameter.

    The way this function reads data is simple. The lines of the file
    are read one after another. If a line contains an item, i.e. an
    uppercased string of arbitrary length enclosed between '!', we
    initialise a new item. Then, we continue appending the next lines
    to the said description until the lines stop starting with a
    non-alpha-numeric character followed by a '!'.

    """

    context.updateFile(path)
    with open(path, 'r') as f:
        pushed = False
        for line in f.readlines():
            line = line.rstrip()
            context.update(line)
            if context.finished_item and not pushed:
                it.push_to_list()
                pushed = True
            if context.new_item:
                it = MeuporgItem.get_item(context)
                pushed = False
            if context.continuing_item:
                it.add_to_description(re.split("\W*! *", line)[1])


def parse_directory(path = ".",
                    include = [],
                    exclude = [],
                    include_backup_files = False,
                    include_hidden_files = False,
                    context = Context()):
    """Parses a whole directory, looking for items in each file.

    Backup files, i.e. '#files#' and 'files~' as well as hidden files
    '.files' are not taken into account unless respectively
    include_backup_files and include_hidden_files are set to True.

    """

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
                    parse_file(path, context)


        
# !SECTION! Test suite


if (__name__ == "__main__"):

    # !SUBSECTION! Testing the MeuporgItem class

    BASIC_FORMAT = "!{0.name}!  {0.description} ({0.sections}, line {0.line_index} in {0.file_name})"
    print BASIC_FORMAT.format(MeuporgItem(
        "    // * !TODO! :! * blabla! And bla too!",
        "./here.txt",
        12,
        [],
        False
    ))
    print BASIC_FORMAT.format(MeuporgItem(
        "blabla bla !FIXREF! blabla! blabla",
        "./here/wait/no/actually/there.bla",
        1234,
        ["title1", "title2"],
        False
    ))
    print(MeuporgItem.__item_names__)
    


    # !SUBSECTION! Testing the parsing functions
    
    parse_directory(
        path = "..",
        include = ["org", "el", "md"],
        exclude = ["readme"],
        include_backup_files = False,
        include_hidden_files = False)
    index = 1
    for it in MeuporgItem.__item_list__:
        ind = "  " * len(it.sections)
        if it.is_section_heading():
            ind = ind[2:]
        print("{indent}{item_number}. !{0.name}!  {0.description} "
              "({0.sections}, line {0.line_index} in "
              "{0.file_name}".format(it,
                                     item_number = index,
                                     indent = ind))
        index += 1

