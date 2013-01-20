#!/usr/bin/env python

import os
import re
from item import meuporg_item



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
    with open(path,'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            if not recording:
                if (re.search(meuporg_item.item_regex,line) != None):
                    location = path
                    it = meuporg_item(line,location,line_index)
                    recording = True
            else:
                if (re.search(meuporg_item.item_regex,line) != None):
                    result.append(it)
                    location = path
                    it = meuporg_item(line,location,line_index)
                elif (re.match('\W*! *',line) != None):
                    it.add_to_description(re.split("\W*! *",line)[1])
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
            path = os.path.join(dirname,name)
            if (include != []):
                to_do = False
                for pattern in include:
                    if re.search(pattern,path):
                        to_do = True
            else:
                to_do = True
            for pattern in exclude:
                    if re.search(pattern,path):
                        to_do = False
            if to_do:
                if not (
                        (not include_backup_files and (re.search("/.*[~#]",path) != None))
                        or
                        (not include_hidden_files and (re.search("/\.[^/]+",path) != None))
                ):
                    result += parse_file(path)
    return result



if (__name__ == "__main__"):
    index = 1
    for it in parse_directory(
            include=["org","el","md"],
            exclude=["readme"],
            include_backup_files=False,
            include_hidden_files=False):
        print("{item_number}. !{0.name}!  {0.description} ({0.location}:{0.line_index})".format(it,item_number=index))
        index += 1
