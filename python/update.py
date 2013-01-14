#!/usr/bin/env python
# Time-stamp: <2013-01-14 20:57:38 leo>

import os
import re

from item import *
from parse import *
from view import *
from file_types import *


def get_configuration(file_name):
    """Parses the file at file_name and returns a list of variables
    initialised from it.

    """
    print("Reading config from {}".format(file_name))
    f = open(file_name,'r')
    include = []
    exclude = []
    include_backup_files = False
    include_hidden_files = False
    for line in f.readlines():
        line = line.rstrip()
        if (re.match("^\W*INCLUDE: .*$",line) != None):
            content = "".join(line.split(":")[1:])
            include = re.split(" *",content)[1:]

        elif (re.match("^\W*EXCLUDE: .*$",line) != None):
            content = "".join(line.split(":")[1:])
            exclude = re.split(" *",content)[1:]

        elif (re.match("^\W*INCLUDE_BACKUP_FILES: .*$",line) != None):
            content = "".join(line.split(":")[1:]).strip()
            include_backup_files = (content == "YES")

        elif (re.match("^\W*INCLUDE_HIDDEN_FILES: .*$",line) != None):
            content = "".join(line.split(":")[1:]).strip()
            include_hidden_files = (content == "YES")
    f.close()
    return include, exclude, include_backup_files, include_hidden_files


def read_header(line):
    """Returns the depth and the name of a header.

    For instance, read_header("** Bla") returns [2, "Bla"].
    """
    content = line.split(" ")
    depth   = len(content[0])
    header  = content[1]
    return [depth, header]
    

def update_main_file(include=[],
                     exclude=[],
                     include_backup_files=False,
                     include_hidden_files=False
                    ):
    """Parses the main file ruling the directory and updates all the
    "Items" nodes in it.

    If there is no "meup.org" or "meuporg.md" file in the parent
    directories (i.e. if main_file() returns the empty string), exits
    violently.

    The name of the header containing the "Items" sub-header is used
    to modify the "include only" array of pattern: ".*<header name>.*"
    is added to it. Then, the parse_directory is called on "." and its
    output org-formatted is placed just below the Item sub-header, at
    the correct depth.

    """

    # opening old main file and cd-ing to its directory
    path_to_old_file = main_file()
    print("updating {}".format(path_to_old_file))
    if (path_to_old_file == ""):
        print("Could not find a main file. Aborting.")
        exit(1)

    dir_old_file, file_name = os.path.split(path_to_old_file)
    os.chdir(dir_old_file)
    
    # find the file format from the file name
    for f in FILE_NAME.keys():
        if (FILE_NAME[f] == file_name):
            file_format = f
    indent_mark = INDENT_MARK[file_format]

    # reading old file a first time to get configuration
    include, exclude, include_backup_files, include_hidden_files = get_configuration(file_name)
    
    # getting items
    items = parse_directory(path=".",
                            include=include,
                            exclude=exclude,
                            include_backup_files=include_backup_files,
                            include_hidden_files=include_hidden_files)

    # setting up variables
    f_old = open(file_name,'r')
    new_content = ""
    depth = 0
    recording = True
    local_include = []
    

    # updating the content
    for line in f_old.readlines():
        line = line.rstrip()
        if (re.match("^"+ indent_mark + "+ .*$",line) != None):
            old_depth = depth
            depth, heading = read_header(line)
            if (old_depth > depth):
                recording = True
                for i in range(0, old_depth-depth+1):
                    local_include.pop()
            elif (old_depth == depth):
                local_include.pop()

            if (heading != "Items"):
                local_include.append(".*" + heading + ".*")
            else:
                # updating "Items" header
                new_content += line + "\n" + output(
                    sort_by_name(pop_item_by_location(items,local_include)),
                    depth+1,
                    file_format)

                # stopping copying the file (to remove the items previously stored)
                recording = False

                local_include.append("Items") # will be poped in next iteration

        if recording:
            new_content += line + "\n"
    
    # closing old file and writing the new one
    f_old.close()
    f_new = open(file_name,'w')
    f_new.write(new_content)
    f_new.close()
    print "[DONE]"
