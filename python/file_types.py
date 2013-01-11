#!/usr/bin/env python

# The different constant which are file_type dependant.

VALID_TYPE = ["org", "md"]

# How entries should be formatted depending on the format. Variables
# are:
# * {location}: relative path to the file
# * {line_index}: number of the line where the item is
# * {description}: the description of the item
# * {name}: the name of the item, e.g. "TODO"
ENTRY_FORMAT = {
    "org": "[[file:{location}::{line_index}][{description}]] ({location}::{line_index})",
    "md":"[{description}]({location}:{line_index})"
}

# The correspondance between file type and main file name.
FILE_NAME = {
    "org": "meup.org",
    "md" : "meuporg.md"
}

# the following is used in regexp (from the re package), so escape
# special characters!
INDENT_MARK = {
    "org": "\*",
    "md" : "#"
}
