#!/usr/bin/env python
# Time-stamp: <2013-01-13 17:01:44 leo>

from ast import literal_eval
import shutil
import os
import sys
import getopt


from item import *
from parse import *
from view import *
from file_types import *
from update import *


TEMPLATE_DIR=os.path.join(os.path.expanduser("~"),".meuporg/templates")


def get_template(file_format):
    """Copy the file in BASE_DIR having the correct extension in the
    current directory.

    """
    if file_format not in FILE_NAME.keys():
        print("Unkown file format")
        exit(1)
    shutil.copy(
        os.path.join(TEMPLATE_DIR,FILE_NAME[file_format]),
        os.path.join(os.path.curdir,FILE_NAME[file_format])
    )
    print("{} file created.".format(FILE_NAME[file_format]))


def print_help():
    """Displays the help of the script."""
    print("""Usage: meuporg OPTIONS

OPTION can be the following.

          -b (backup file): include backup files (file~ and #file#)
          
          -d (dot file): include hidden file (.file)

          -e --exclude=: Decides which file and path pattern(s) to
          exclude from the search.

          -f --main-file=: Returns the path to the main file of the
           directory (if any).

          -h (help):prints this help and exits.

          -i --include=: Decides which file pattern(s) to include in
          the search.

          -l (unordered): lists the locations of all the tags in the
          files in the current folder and its subdirectories in no
          particular order.

          -m --markdown: outputs the list of item in markdown format.

          -n (number): gives a list of the tag types in alphabetical
          order and their number of occurrences.

          -o --org: outputs the list of item in org-mode markup format.

          -t (template) <format>: <format> has to be either "md" or
           "org". Creates a new meuporg main file in the said
           format.

          -u (update): updates the meup.org file in the current
           directory.

          """)

if (__name__ == "__main__"):
    if (len(sys.argv) == 1):
        print_help()
    else:
        optlist , args = getopt.gnu_getopt(
            sys.argv,
            "bde:fhi:lmnot:u",
            ["help", "include=", "exclude=","main-file=","org","markdown"]
        )
        include = []
        exclude = []
        include_backup_files = False
        include_hidden_files = False

        # for option, argument in optlist:
        for option, argument in optlist:

            # include backup
            if (option == "-b"):
                include_backup_files = True

            # include hidden files
            if (option == "-d"):
                include_hidden_files = True

            # deciding which files to exclude
            elif (option == "-e" or option == "--exclude"):
                exclude = argument.split(" ")
            
            # printing the path to the main file
            elif (option == "-f" or option == "--main-file"):
                print main_file()

            # printing help
            elif (option == "-h" or option == "--help"):
                print_help()
                exit()


            # deciding which files to include
            elif (option == "-i" or option == "--include"):
                include = argument.split(" ")

            # listing the tags in no particular order
            elif (option == "-l"):
                tags = parse_directory(include=include,
                                       exclude=exclude,
                                       include_backup_files=include_backup_files,
                                       include_hidden_files=include_hidden_files)
                for item in tags:
                    print( "!{}! ({})".format(item.name, item.location) )
                exit()

            # outputing the items using markdown markup
            elif (option == "-m"):
                tags = parse_directory(include=include,
                                       exclude=exclude,
                                       include_backup_files=include_backup_files,
                                       include_hidden_files=include_hidden_files)
                print(output(sort_by_name(tags),2,"md"))

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
                print(output(sort_by_name(tags),2,"org"))                

            # updating the meup.org file
            elif (option == "-u"):
                update_main_file(include=include,
                                 exclude=exclude,
                                 include_backup_files=include_backup_files,
                                 include_hidden_files=include_hidden_files)

            # fetching template
            elif (option == "-t"):
                get_template(argument)
