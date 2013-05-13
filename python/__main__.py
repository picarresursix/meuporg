#!/usr/bin/env python
# Time-stamp: <2013-05-13 12:24:25 leo>

"""Contains the main program of meuporg, i.e. parses the cli arguments
and calls the correct functions.

"""

import shutil
import os
import argparse


import fileFormat 
import fileUpdate
import itemDb
import itemUtils


# !SECTION! Constants and trivial routines

TEMPLATE_DIR = os.path.join(os.path.expanduser("~"), ".meuporg/templates")


def get_template(format_name):
    """Copy the file in BASE_DIR having the correct extension in the
    current directory.

    """
    if format_name not in fileFormat.Factory.valid_formats:
        raise Exception("Unkown file format")
    else:
        style = fileFormat.Factory.get_format(format_name)
        shutil.copy(
            os.path.join(TEMPLATE_DIR, style.get_main_file_name()),
            os.path.join(os.path.curdir, style.get_main_file_name())
        )
        print("{} file created.".format(style.get_main_file_name()))


def parse_and_print(path=".",
                    style_name="org",
                    include=[],
                    exclude=[],
                    include_backup_files=False,
                    include_hidden_files=False):
    """Parses what is at path (it can be a file or a directory) and
    outputs the items found using the format given, sorting them by
    name.

    """
    if (os.path.isdir(path)):
        tags = itemUtils.parse_directory(include=include,
                                         exclude=exclude,
                                         include_backup_files=include_backup_files,
                                         include_hidden_files=include_hidden_files,
                                         path=path)
    else:
        tags = itemUtils.parse_file(path)
        print(FileFormat.output(meuporgCore.sort_by_name(tags), 2, style_name))



# !SECTION! Main function

if (__name__ == "__main__"):

    # !SUBSECTION! Declaring the CLI arguments

    ARGUMENT_PARSER = argparse.ArgumentParser(
        version = "0.9",
        description = (
            "Parse files/directories to find items and either print them"
            " or use them to update a file where information is"
            " centralised."
        ),
        epilog =
        "Meuporg is intended to help you manage your projects. If you"
        " have any suggestions or find a bug, send a mail at leoperrin"
        " at picarresursix dot fr. I'll see what I can do."
    )

    ARGUMENT_PARSER.add_argument(
        "-b",
        help = (
            "(Backup file): include backup files (file~ and #file#);"
            " default behaviour is not to. "
        ),
        action = 'store_true', dest='include_backup_files',
        default = False
    )

    ARGUMENT_PARSER.add_argument(
        "-d",
        help = (
            "(Dot file): include hidden files and folders (starting with"
            " '.'), default behaviour is not to."
        ),
        action = 'store_true', dest='include_hidden_files',
        default = False
    )

    ARGUMENT_PARSER.add_argument(
        "-f",
        help = (
            "(main File): Returns the path to the main file of the"
            " directory (if any)."
        ),
        action = 'store_true', dest='show_main_file',
        default = False
    )

    ARGUMENT_PARSER.add_argument(
        "-e",
        help = (
            "(Exclude): Decides which file pattern(s) to exclude from the"
            " search. Repeat to specify several regex to exclude. Default"
            " behaviour is to exclude no file (but the backup and hidden"
            " ones)."
        ),
        action = 'append', dest='to_exclude',
        default = []
    )

    ARGUMENT_PARSER.add_argument(
        "-i",
        help = (
            "(Include): Decides which file pattern(s) to include in the"
            " search. Repeat to specify several regex to include. Default"
            " behaviour is to include every file (but the backup and hidden"
            " ones)."
        ),
        action = 'append', dest='to_include',
        default = []
    )

    ARGUMENT_PARSER.add_argument(
        "-t",
        help = (
            "(Template) <format>: <format> has to be either 'md',"
            " 'vimwiki' or 'org'. Creates a new meuporg main file in the"
            " said format."
        ),
        action = 'store', dest='template_style',
        default = ""
    )

    ARGUMENT_PARSER.add_argument(
        "-o",
        help = (
            "(Org): outputs the list of items in the given path or"
            " folder in org-mode format."
        ),
        action = 'store', dest='parse_and_show_org',
        default = ""
    )

    ARGUMENT_PARSER.add_argument(
        "-m",
        help = (
            "(Md): outputs the list of items in the given path or"
            " folder in markdown."
        ),
        action = 'store', dest='parse_and_show_md',
        default = ""
    )
    ARGUMENT_PARSER.add_argument(
        "-w",
        help = (
            "(vimWiki): outputs the list of items in the given path or"
            " folder in vimwiki format."
        ),
        action = 'store', dest='parse_and_show_vimwiki',
        default = ""
    )
    ARGUMENT_PARSER.add_argument(
        "-u",
        help = (
            "(Update): Updates the main file ruling this directory (it"
            " might be in the parent directories)."
        ),
        action = 'store_true', dest='update',
        default = False
    )
    
    
    # !SUBSECTION! Acting depending on the CLI arguments
    
    ARGS = ARGUMENT_PARSER.parse_args()
    meuporg = fileUpdate.MainFile()
    if ARGS.show_main_file:
        print meuporg.path
    elif ARGS.template_style != "":
        get_template(ARGS.template_style)
    elif ARGS.parse_and_show_org != "":
        parse_and_print(
            path=ARGS.parse_and_show_org,
            include=ARGS.to_include,
            exclude=ARGS.to_exclude,
            include_backup_files=ARGS.include_backup_files,
            include_hidden_files=ARGS.include_hidden_files,
            style_name="org")

    elif ARGS.parse_and_show_md != "":
        parse_and_print(
            path=ARGS.parse_and_show_md,
            include=ARGS.to_include,
            exclude=ARGS.to_exclude,
            include_backup_files=ARGS.include_backup_files,
            include_hidden_files=ARGS.include_hidden_files,
            style_name="md")

    elif ARGS.parse_and_show_vimwiki != "":
        parse_and_print(
            path=ARGS.parse_and_show_vimwiki,
            include=ARGS.to_include,
            exclude=ARGS.to_exclude,
            include_backup_files=ARGS.include_backup_files,
            include_hidden_files=ARGS.include_hidden_files,
            style_name="vimwiki")

    elif ARGS.update:
        meuporg.update(include=ARGS.to_include,
                 exclude=ARGS.to_exclude,
                 include_backup_files=ARGS.include_backup_files,
                 include_hidden_files=ARGS.include_hidden_files)

    else:
        ARGUMENT_PARSER.print_help()
        # itemUtils.parse_directory(".")
        # print output(item.MeuporgItem.project_structure,2,"org")
