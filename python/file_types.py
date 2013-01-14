#!/usr/bin/env python

# The different constant which are file_type dependent.


VALID_TYPE = ["org", "md", "wiki"]

# How entries should be formatted depending on the format. Variables
# are:
# * {item_number}: the index of the item
# * {location}: relative path to the file
# * {line_index}: number of the line where the item is
# * {description}: the description of the item
# * {name}: the name of the item, e.g. "TODO"
ENTRY_FORMAT = {
    "org":  "{item_number}. [[file:{location}::{line_index}][{description}]] ({location}::{line_index})",
    "md":   "{item_number}. [{description}]({location}:{line_index})",
    "wiki": "# [file://{location}:{line_index}|{description}] ({location}:{line_index})"
}

# The correspondance between file type and main file name.
FILE_NAME = {
    "org": "meup.org",
    "md" : "meuporg.md",
    "wiki": "meuporg.wiki"
}

# The following is used in regexp (from the re package), so escape
# special characters!
INDENT_MARK = {
    "org": "\*",
    "md" : "#",
    "wiki":"="
}


# To obtain a heading of depth n, iterate the following construction n
# times.
HEADING_TEMPLATE = {
    "org": "*{}",
    "md": "#{}#",
    "wiki": "={}="
}
