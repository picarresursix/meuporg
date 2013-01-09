#!/usr/bin/env python

import os
import re
from item import *


def parse_file(path):
    """Returns a list containing all the items in the file at path.

    The way this function reads data is simple. The lines of the file
    are read one after another. If a line contains an item, i.e. an
    uppercased string of arbitrary length enclosed between '!', we
    initialise a new item:

    """

    recording = False
    line_index = 1
    result = []
    f = open(path,'r')
    for line in f.readlines():
        line = line.rstrip()
        if not recording:
            if (re.match(ITEM_LINE_REGEX,line) != None):
                location = path + "::" + str(line_index)
                it = Item(line,location)
                recording = True
        else:
            if (re.match(ITEM_LINE_REGEX,line) != None):
                result.append(it)
                location = path + "::" + str(line_index)
                it = Item(line,location)
            elif (re.match('\W*! *',line) != None):
                it.add_to_description(re.split("\W*! *",line)[1])
            else:
                result.append(it)
                recording = False
        line_index += 1
        f.close()
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
        for f in filenames:
            if (include != []):
                to_do = False
                for pattern in include:
                    if re.match(pattern,f):
                        to_do = True
            else:
                to_do = True
            for pattern in exclude:
                    if re.match(pattern,path):
                        to_do = False
            if to_do:
                path = os.path.join(dirname,f)
                if not (
                        (not include_backup_files and (re.match("^[^#].*[^~]$",f) == None))
                        or
                        (not include_hidden_files and (re.match("^[^.].*$"    ,f) == None))
                ):
                    result += parse_file(path)
    return result



if (__name__ == "__main__"):
    for it in parse_directory():
        print(it.to_entry())
