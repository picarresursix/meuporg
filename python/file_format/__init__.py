#!/usr/bin/env python

from org import org_file
from md import md_file
from vimwiki import vimwiki_file


def formats():
    """Returns a list of the file formats supported by meuporg."""
    return [org_file(), md_file(), vimwiki_file()]


if __name__ == "__main__":
    # basic test of the classes in this module
    
    for file_format in formats():
        print "name: {}".format(file_format.get_name())
        print "main file: {}".format(file_format.get_main_file_name())
        print "sample headers:\n{}\n{}\n{}".format(
            file_format.header_to_string(1,"depth 1"),
            file_format.header_to_string(2,"depth 2"),
            file_format.header_to_string(3,"depth 2"),
        )
