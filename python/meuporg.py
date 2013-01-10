#!/usr/bin/env python


from ast import literal_eval
import sys
import getopt
import re

from item import *
from parse import *
from view import *


def read_header(line):
    """Returns the depth and the name of a header.

    For instance, read_header("** Bla") returns [2, "Bla"].
    """
    content = line.split(" ")
    depth   = len(content[0])
    header  = content[1]
    return [depth, header]
    

def update_meuporg_file(path=".",
                    include=[],
                    exclude=[],
                    include_backup_files=False,
                    include_hidden_files=False):
    """Parses the file at path and updates all the "Items" nodes in
    it.

    The name of the header containing the "Items" sub-header is used
    to modify the "include only" array of pattern: ".*<header name>.*"
    is added to it. Then, the parse_directory is called on "." and its
    output org-formatted is placed just below the Item sub-header, at
    the correct depth.

    """
    f_old = open(path,'r')
    new_content = ""
    heading = "."
    depth = 2
    recording = True
    for line in f_old.readlines():
        line = line.rstrip()
        if (re.match("^\** Items$",line) != None):
            depth, void_header = read_header(line)
            if (depth == 1):
                # case where the "Items" header is a top-level
                heading = "."

            print "Item: " + str(depth) + " " + heading
            local_include = include
            local_include.append(".*" + heading + ".*")
            items = parse_directory(path=".",
                    include=local_include,
                    exclude=exclude,
                    include_backup_files=include_backup_files,
                    include_hidden_files=include_hidden_files)
            new_content += line + "\n" + org_output(extract_name(items),depth+1)

            # not parsing the same files twice
            exclude.append(".*" + heading + ".*")

            # stopping copying the file (to remove the items previously stored)
            recording = False
        elif (re.match("^\** \w*$",line) != None):
                old_depth = depth
                depth, heading = read_header(line)
                if (depth < old_depth):
                    recording = True
                print "new heading: " + heading + ", depth: " + str(depth)
        if recording:
            new_content += line + "\n"
    f_old.close()
    f_new = open(path,'w')
    f_new.write(new_content)
    f_new.close()


def print_help():
    """Displays the help of the script."""
    print("""Usage: meuporg OPTIONS

OPTION can be the following.
          -h (help):prints this help and exits.

          -i --include=: Decides which file pattern(s) to include in
          the search.

          -e --exclude=: Decides which file and path pattern(s) to
          exclude from the search.

          -m --module-depth=: Sorts the items depending on the folders
          they are in up to the given depth.

          -l (unordered): lists the locations of all the tags in the
          files in the current folder and its subdirectories in no
          particular order.

          -n (number): gives a list of the tag types in alphabetical
          order and their number of occurrences.

          -o (org-mode): outputs the list of item in org-mode markup
           format.

          -u (update): updates the meup.org file in the current
           directory.

          """)

if (__name__ == "__main__"):
    if (len(sys.argv) == 1):
        print_help()
    else:
        optlist , args = getopt.gnu_getopt(sys.argv,"i:e:m:unhlo",["help", "include=", "exclude="])
        include = []
        exclude = []
        include_backup_files = False
        include_hidden_files = False
        module_depth = 0

        # for option, argument in optlist:
        for option, argument in optlist:
            # printing help
            if (option == "-h" or option == "--help"):
                print_help()
                exit()


            # deciding which files to include
            elif (option == "-i" or option == "--include"):
                include = argument.split(" ")


            # deciding which files to exclude
            elif (option == "-e" or option == "--exclude"):
                exclude = argument.split(" ")


            # deciding whether items should be grouped by modules
            elif (option == "-m"):
                module_depth = int(argument)
            
    
            # listing the tags in no particular order
            elif (option == "-l"):
                tags = parse_directory(include=include,
                                       exclude=exclude,
                                       include_backup_files=include_backup_files,
                                       include_hidden_files=include_hidden_files)
                for item in tags:
                    print( "!{}! ({})".format(item.name, item.location) )
                exit()


            # giving the number of each item type                
            elif (option == "-n"):
                tags = parse_directory(include=include,
                                       exclude=exclude,
                                       include_backup_files=include_backup_files,
                                       include_hidden_files=include_hidden_files)
                numbers = {}
                for item in tags:
                    if item.name not in numbers.keys():
                        numbers[item.name] = 1
                    else:
                        numbers[item.name] += 1
                for item_name in sorted(numbers.keys()):
                    print( "{}: {}".format(item_name, numbers[item_name]))
                exit()


            # outputing the items using org-mode markup
            elif (option == "-o"):
                tags = parse_directory(include=include,
                                       exclude=exclude,
                                       include_backup_files=include_backup_files,
                                       include_hidden_files=include_hidden_files)
                if (module_depth == 0):
                    print(org_output(extract_name(tags),2))
                else:
                    print(org_output(extract_module(tags),2))

            # updating the meup.org file
            elif (option == "-u"):
                update_meuporg_file("./meup.org")
