#!/usr/bin/env python
# Time-stamp: <2013-01-20 14:54:00 leo>

import os
import re

from item import MeuporgItem
from parse import parse_file, parse_directory
from view import output, flatten_to_list, sort_by_name, pop_item_by_patterns 
import file_format



def main_file():
    """Goes up the directory tree until finding a folder containing a
    "meup.org" or "meuporg.md" file and then returns the full path to
    the said file.

    If a directory whose full path contains less than two "/" is
    encountered, we stop because we went to deep (used to prevent
    infinite loop).

    If nothing was found, returns the empty string.

    """
    while (len(os.getcwd().split(os.path.sep)) > 2):
        folder_content = os.listdir(os.path.curdir)
        for style in file_format.Factory.get_format_list():
            if style.get_main_file_name() in folder_content:
                return os.path.join(
                    os.getcwd(),
                    style.get_main_file_name()
                )
        os.chdir(os.path.pardir)
    return ""


def heading_to_patterns(heading):
    """Extract patterns from a heading.

    If the heading is a space separated list of words, returns a
    list containing these words.

    If the heading contains a bracket enclosed list of comma separated
    words, outputs only this list.

    Examples:
    > print(heading_to_patterns("section title"))
      ["section", "title"]
    > print(heading_to_patterns("section title (pattern1,re.*gex)"))
      ["pattern1", "re.*gex"]

    """
    if re.match(".*\(.*\)\W*$", heading) == None:
        return heading.split(" ")
    else:
        return heading[heading.find('(')+1:heading.find(')')].split(",")
        

    

def get_configuration(file_name):
    """Parses the file at file_name and returns a list of variables
    initialised from it.

    """
    print("Reading config from {}".format(file_name))
    with open(file_name, 'r') as f:
        include = []
        exclude = []
        include_backup_files = False
        include_hidden_files = False
        for line in f.readlines():
            line = line.rstrip()
            if (re.match("^\W*INCLUDE: .*$", line) != None):
                content = "".join(line.split(":")[1:])
                include = re.split(" *", content)[1:]

            elif (re.match("^\W*EXCLUDE: .*$", line) != None):
                content = "".join(line.split(":")[1:])
                exclude = re.split(" *", content)[1:]

            elif (re.match("^\W*INCLUDE_BACKUP_FILES: .*$", line) != None):
                content = "".join(line.split(":")[1:]).strip()
                include_backup_files = (content == "YES")

            elif (re.match("^\W*INCLUDE_HIDDEN_FILES: .*$", line) != None):
                content = "".join(line.split(":")[1:]).strip()
                include_hidden_files = (content == "YES")
    return include, exclude, include_backup_files, include_hidden_files

    

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
    for potential_style in file_format.Factory.get_format_list():
        if (potential_style.get_main_file_name() == file_name):
            style = potential_style

    # reading old file a first time to get configuration
    include, exclude, include_backup_files, include_hidden_files = get_configuration(file_name)
    
    # getting items
    items = parse_directory(path=".",
                            include=include,
                            exclude=exclude,
                            include_backup_files=include_backup_files,
                            include_hidden_files=include_hidden_files)

    # setting up variables
    with open(file_name, 'r') as f_old:
        new_content = ""
        depth = 0
        recording = True
        local_include = []
    

        # updating the content
        for line in f_old.readlines():
            line = line.rstrip()
            if (style.line_to_header(line) != False):
                old_depth = depth
                depth, heading = style.line_to_header(line)
                if (old_depth > depth):
                    recording = True
                    for i in range(0, old_depth-depth+1):
                        local_include.pop()
                elif (old_depth == depth):
                    local_include.pop()

                if (heading != "Items"):
                    local_include += [heading_to_patterns(heading)]
                    
                else:
                    # updating "Items" header. If an item name is in
                    # local_include, we do not sort the items by name.
                    use_sort_by_name = True
                    for pattern in flatten_to_list(local_include):
                        if pattern in MeuporgItem.item_names:
                            use_sort_by_name = False
                    if use_sort_by_name:
                        items_to_print = sort_by_name(pop_item_by_patterns(
                            items,
                            flatten_to_list(local_include)
                        ))
                    else:
                        items_to_print = pop_item_by_patterns(
                            items,
                            flatten_to_list(local_include)
                        )
                    new_content += line + "\n" + output(
                        items_to_print,
                        depth+1,
                        style.get_name())
                    
                    # stopping copying the file (to remove the items previously stored)
                    recording = False

                    local_include.append("Items") # will be poped in next iteration
            if recording:
                new_content += line + "\n"
    
    #  writing the new file
    with open(file_name, 'w') as f_new:
        f_new.write(new_content)
    print "[DONE]"


if __name__ == "__main__":
    print heading_to_patterns("blabla abla")
    print heading_to_patterns("blabla (bla,bla,bli)")
    print heading_to_patterns("blabla abla (bcka,.*nckj,vn[/n],nckn+)")
    print heading_to_patterns("blabla abla ()")
    
