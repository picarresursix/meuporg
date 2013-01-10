#!/usr/bin/env python


from ast import literal_eval
import sys
import getopt

from item import *
from parse import *
from view import *


def update_meuporg_file(path):
    """Parses the file at path and updates all the Item nodes"""


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

          -u (unordered): lists the locations of all the tags in the
          files in the current folder and its subdirectories in no
          particular order.

          -n (number): gives a list of the tag types in alphabetical
          order and their number of occurrences.

          -o (org-mode): outputs the list of item in org-mode markup
           format.

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
            elif (option == "-u"):
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
