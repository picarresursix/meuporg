#!/usr/bin/env python
# Time-stamp: <2013-02-16 23:05:10 leo>

from collections import defaultdict
import os
import re

import itemUtils
import fileFormat


# !SECTION! Dealing with a list of items

def sort_by_name(item_list):
    """Returns a dictionnary where the keys are the item names and
    the entries are list of the items having this name.

    """
    result = defaultdict(list)
    for item in flatten_to_list(item_list):
        result[item.name] += [item]
    return result


def flatten_to_list(items):
    """"Destroys" the sorting of some items by taking all the items in
    a dictionnary and putting them in a "flat" list. If the list
    contains a list, the content of this list is added to the main
    one.

    If given a list of items, does not modify it.

    """
    if isinstance(items, list):
        result = []
        for elmt in items:
            if isinstance(elmt, list) or isinstance(elmt, dict):
                result += flatten_to_list(elmt)
            else:
                result.append(elmt)
        return result
    elif isinstance(items, dict):
        result = []
        for key in items.keys():
            result += flatten_to_list(items[key])
        return result
        
    

def pop_item_by_patterns(items,  pattern_list):
    """Goes through the items in the list and builds a new list
    containing all items matching (in the sense of the Criteria class)
    all the patterns. These items are removed from the list passed in
    parameter.

    """
    if isinstance(items, dict):
        result = {}
        for key in items.keys():
            result[key] = pop_item_by_patterns(items[key],  pattern_list)
    elif isinstance(items, list):
        result = []
        for i in reversed(range(0, len(items))):
            keep_it = True
            item = items[i]
            for pattern in pattern_list:
                if not Criteria(item).match(pattern):
                    keep_it = False
            if keep_it:
                result.append(item)
                items.pop(i)
    return result
        
    

def output(items, depth, output_format):
    """Outputs a representation of the items given in the format
    wanted, which must be in fileFormat.Factory.valid_types.

    Uses keys of a dictionnary as headings and output lists as
    lists. The indentation of the list and the level of the head node
    is given by the depth argument.

    """
    style = fileFormat.Factory.get_format(output_format)
    result = ""
    if isinstance(items, dict):
        for key in sorted(items.keys()):
            partial_output = output(items[key], depth+1, output_format)
            if (partial_output != ""):
                heading = style.header_to_string(depth, key)
                result += "{}\n{}".format(
                    heading,
                    partial_output
                )
    elif isinstance(items, list):
        if (len(items) == 0):
            result = ""
        else:
            indent = ""
            for i in range(0, depth):
                indent += " "
            result += style.list_to_string(reversed(items), indent)
    return result



# !SECTION! Interacting with the main file

#   !SUBSECTION! Find the main file

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
        for style in fileFormat.Factory.get_format_list():
            if style.get_main_file_name() in folder_content:
                return os.path.join(
                    os.getcwd(),
                    style.get_main_file_name()
                )
        os.chdir(os.path.pardir)
    return ""


#   !SUBSECTION! Extract data from the main file

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


#   !SUBSECTION! Updating the main file    

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
    for potential_style in fileFormat.Factory.get_format_list():
        if (potential_style.get_main_file_name() == file_name):
            style = potential_style

    # reading old file a first time to get configuration
    include, exclude, include_backup_files, include_hidden_files = get_configuration(file_name)
    
    # getting items
    items = itemUtils.parse_directory(path=".",
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



# !SECTION! Test suite

if __name__ == "__main__":

    # !SUBSECTION! Testing the interaction with item lists

    item_list = {
        "bla": [
            MeuporgItem("    // * !TODO! :! * blabla! And bla too!", "./here.txt", 1),
            MeuporgItem("blabla bla !FIXREF! blabla! blabla", "./here/wait/no/actually/there.bla", 123456)
        ],
        "blo": {
            "blu" :
            [
                MeuporgItem("    // * !IDEA! :! * blabla! And bla too!", "./here.txt", 1),
                MeuporgItem("blabla bla !IDEA! blabla! blabla", "./here/wait/no/actually/there.bla", 123456)
            ],
            "bly" :
            [
                MeuporgItem("    // * !TODO! :! * blabla! And bla too!", "./here.txt", 1),
                MeuporgItem("blabla bla !FIXREF! blabla! blabla", "./here/wait/no/actually/there.bla", 123456)
            ]
        }
    }
    print(output(item_list, 1, "org"))
    print(output(item_list, 1, "md"))
    print(output(item_list, 1, "vimwiki"))
    fixref = pop_item_by_patterns(item_list, ["FIXREF"])
    print("FIXREF:\n{}".format(output(fixref, 1, "org")))
    todo = pop_item_by_patterns(item_list, ["TODO"])
    print("TODO:\n{}".format(output(todo, 1, "org")))
    remainer = sort_by_name(item_list)
    print("REMAINER:\n{}".format(output(remainer, 1, "org")))


    # !SUBSECTION! Testing the interaction with the main file

    print heading_to_patterns("blabla abla")
    print heading_to_patterns("blabla (bla,bla,bli)")
    print heading_to_patterns("blabla abla (bcka,.*nckj,vn[/n],nckn+)")
    print heading_to_patterns("blabla abla ()")
    
