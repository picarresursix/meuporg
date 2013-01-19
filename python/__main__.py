#!/usr/bin/env python
# Time-stamp: <2013-01-20 00:01:34 leo>

import shutil
import os
import sys
import argparse


import file_format 
from parse import parse_file, parse_directory
from view import *
from update import update_main_file, main_file


TEMPLATE_DIR=os.path.join(os.path.expanduser("~"),".meuporg/templates")


def get_template(format_name):
    """Copy the file in BASE_DIR having the correct extension in the
    current directory.

    """
    if format_name not in file_format.factory.valid_formats:
        raise Exception("Unkown file format")
    style = file_format.factory.get_format(format_name)
    shutil.copy(
        os.path.join(TEMPLATE_DIR,style.get_main_file_name()),
        os.path.join(os.path.curdir,style.get_main_file_name())
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
        tags = parse_directory(include=include,
                               exclude=exclude,
                               include_backup_files=include_backup_files,
                               include_hidden_files=include_hidden_files,
                               path=path)
    else:
        tags = parse_file(path)
    print(output(sort_by_name(tags),2,style_name))


if (__name__ == "__main__"):
    argument_parser = argparse.ArgumentParser(
        version = "0.9",
        description = (
        "Parse files/directories to find items and either print them"
        " or use them to update a file where information is"
        " centralised."
        ),
        epilog =
        "Meuporg is intended to help you manage your projects. If you"
        " have any suggestions or find a bug, send a mail at leoperrin"
        " at picarresurix dot fr. I'll see what I can do."
        )

    argument_parser.add_argument(
        "-b",
        help = (
        "(Backup file): include backup files (file~ and #file#);"
        " default behaviour is not to. "
        ),
        action = 'store_true', dest='include_backup_files',
        default = False
    )

    argument_parser.add_argument(
        "-d",
        help = (
        "(Dot file): include hidden files and folders (starting with"
        " '.'), default behaviour is not to."
        ),
        action = 'store_true', dest='include_hidden_files',
        default = False
    )

    argument_parser.add_argument(
        "-f",
        help = (
        "(main File): Returns the path to the main file of the"
        " directory (if any)."
        ),
        action = 'store_true', dest='show_main_file',
        default = False
    )

    argument_parser.add_argument(
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

    argument_parser.add_argument(
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

    argument_parser.add_argument(
        "-t",
        help = (
        "(Template) <format>: <format> has to be either 'md',"
        " 'vimwiki' or 'org'. Creates a new meuporg main file in the"
        " said format."
        ),
        action = 'store', dest='template_style',
        default = ""
    )

    argument_parser.add_argument(
        "-o",
        help = (
        "(Org): outputs the list of items in the given path or"
        " folder in org-mode format."
        ),
        action = 'store', dest='parse_and_show_org',
        default = ""
    )

    argument_parser.add_argument(
        "-m",
        help = (
        "(Md): outputs the list of items in the given path or"
        " folder in markdown."
        ),
        action = 'store', dest='parse_and_show_md',
        default = ""
    )
    argument_parser.add_argument(
        "-w",
        help = (
        "(vimWiki): outputs the list of items in the given path or"
        " folder in vimwiki format."
        ),
        action = 'store', dest='parse_and_show_vimwiki',
        default = ""
    )
    argument_parser.add_argument(
        "-u",
        help = (
        "(Update): Updates the main file ruling this directory (it"
        " might be in the parent directories)."
        ),
        action = 'store_true', dest='update',
        default = False
    )
    
    
    args = argument_parser.parse_args()
    if args.show_main_file:
        print main_file()
    elif args.template_style != "":
        get_template(args.template_style)
    elif args.parse_and_show_org != "":
        parse_and_print(
            path=args.parse_and_show_org,
            include=args.to_include,
            exclude=args.to_exclude,
            include_backup_files=args.include_backup_files,
            include_hidden_files=args.include_hidden_files,
            style_name="org")

    elif args.parse_and_show_md != "":
        parse_and_print(
            path=args.parse_and_show_md,
            include=args.to_include,
            exclude=args.to_exclude,
            include_backup_files=args.include_backup_files,
            include_hidden_files=args.include_hidden_files,
            style_name="md")

    elif args.parse_and_show_vimwiki != "":
        parse_and_print(
            path=args.parse_and_show_vimwiki,
            include=args.to_include,
            exclude=args.to_exclude,
            include_backup_files=args.include_backup_files,
            include_hidden_files=args.include_hidden_files,
            style_name="vimwiki")

    elif args.update:
        update_main_file(include=args.to_include,
                         exclude=args.to_exclude,
                         include_backup_files=args.include_backup_files,
                         include_hidden_files=args.include_hidden_files)

    else:
        argument_parser.print_help()
