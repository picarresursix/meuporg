#!/usr/bin/env python

import os
import re
from item import *
from file_types import *


def main_file():
    """Goes up the directory tree until finding a folder containing a
    "meup.org" or "meuporg.md" file and then returns the full path to
    the said file.

    """
    while (len(os.getcwd().split(os.path.sep)) > 2):
        folder_content = os.listdir(os.path.curdir)
        for file_format in FILE_NAME.keys():
            if FILE_NAME[file_format] in folder_content:
                return os.path.join(os.getcwd(),FILE_NAME[file_format])
        os.chdir(os.path.pardir)
    return ""


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
    f = open(path,'r')
    for line in f.readlines():
        line = line.rstrip()
        if not recording:
            if (re.match(ITEM_LINE_REGEX,line) != None):
                location = path
                it = Item(line,location,line_index)
                recording = True
        else:
            if (re.match(ITEM_LINE_REGEX,line) != None):
                result.append(it)
                location = path
                it = Item(line,location,line_index)
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
            path = os.path.join(dirname,f)
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
    print main_file()
    for it in parse_directory(
            include=["org","el","md"],
            exclude=["readme"],
            include_backup_files=False,
            include_hidden_files=False):
        print(it.format_entry("!{name}!  {description} ({location}:{line_index})"))
