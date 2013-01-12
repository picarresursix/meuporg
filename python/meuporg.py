#!/usr/bin/env python


from ast import literal_eval
import sys
import os
import getopt
import re

from item import *
from parse import *
from view import *
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


def read_header(line):
    """Returns the depth and the name of a header.

    For instance, read_header("** Bla") returns [2, "Bla"].
    """
    content = line.split(" ")
    depth   = len(content[0])
    header  = content[1]
    return [depth, header]
    

def update_meuporg_file(include=[],
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
    dir_old_file = os.path.split(path_to_old_file)[0]
    file_name = os.path.split(path_to_old_file)[1]
    os.chdir(dir_old_file)
    f_old = open(file_name,'r')

    # find the file format from the file name
    for f in FILE_NAME.keys():
        if (FILE_NAME[f] == file_name):
            file_format = f
    indent_mark = INDENT_MARK[file_format]


    # updating the content
    new_content = ""
    heading = "."
    depth = 2
    recording = True
    for line in f_old.readlines():
        line = line.rstrip()
        if (re.match("^" + indent_mark + "* Items$",line) != None):
            depth, void_header = read_header(line)
            if (depth == 1):
                # case where the "Items" header is a top-level
                heading = "."

            local_include = include
            local_include.append(".*" + heading + ".*")
            items = parse_directory(path=".",
                    include=local_include,
                    exclude=exclude,
                    include_backup_files=include_backup_files,
                    include_hidden_files=include_hidden_files)
            new_content += line + "\n" + output(extract_name(items),depth+1,file_format)

            # not parsing the same files twice
            exclude.append(".*" + heading + ".*")

            # stopping copying the file (to remove the items previously stored)
            recording = False
        elif (re.match("^"+ indent_mark + "* \w*$",line) != None):
                old_depth = depth
                depth, heading = read_header(line)
                if (depth < old_depth):
                    recording = True

        if recording:
            new_content += line + "\n"
    f_old.close()
    f_new = open(file_name,'w')
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

          -f --main-file=: Returns the path to the main file of the
           directory (if any).

          -l (unordered): lists the locations of all the tags in the
          files in the current folder and its subdirectories in no
          particular order.

          -n (number): gives a list of the tag types in alphabetical
          order and their number of occurrences.

          -o --org: outputs the list of item in org-mode markup format.

          -m --markdown: outputs the list of item in markdown format.

          -u (update): updates the meup.org file in the current
           directory.

          -t (template) <format>: <format> has to be either "md" or
           "org". Creates a new meuporg main file in the said
           format.

          """)

if (__name__ == "__main__"):
    if (len(sys.argv) == 1):
        print_help()
    else:
        optlist , args = getopt.gnu_getopt(
            sys.argv,
            "i:e:fmunhlot:",
            ["help", "include=", "exclude=","main-file=","org","markdown"]
        )
        include = []
        exclude = []
        include_backup_files = False
        include_hidden_files = False

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
            

            # printing the path to the main file
            elif (option == "-f" or option == "--main-file"):
                print main_file()


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
                print(output(extract_name(tags),2,"org"))

            # outputing the items using markdown markup
            elif (option == "-m"):
                tags = parse_directory(include=include,
                                       exclude=exclude,
                                       include_backup_files=include_backup_files,
                                       include_hidden_files=include_hidden_files)
                print(output(extract_name(tags),2,"md"))
                

            # updating the meup.org file
            elif (option == "-u"):
                update_meuporg_file(include=include,
                                    exclude=exclude,
                                    include_backup_files=include_backup_files,
                                    include_hidden_files=include_hidden_files)
