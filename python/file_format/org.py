#!/usr/bin/env python

import re


class org_file:
    """Provides function to read headers and print headers and lists
    to a file using the org format.

    """
    def get_name(self):
        """Returns the name of the format."""
        return "org"


    def get_main_file_name(self):
        """Returns the name of the main file associated with this
        format.

        """
        return "meup.org"


    def line_to_header(self,line):
        """Returns False if the line does not correspond to a header
        and a list containing [depth, title] otherwise.

        """
        if (re.match("^\*+ .+$",line) == None):
            return False
        else:
            content = line.split(" ")
            depth = len(content[0])
            title = line[depth:].strip()
            return [depth, title]
            

    def header_to_string(self,depth,title):
        """Returns a string containing a header with the given title
        and depth.

        """
        return "*"*depth + " " + title
        

    def item_to_string(self,item):
        """Returns the string containing the data in the item
        corresponding to this format.

        """
        return "[[file:{location}::{line_index}][{description}]] ({location}::{line_index})".format(
            item.location,
            item.line_index,
            item.description
        )
        

    def list_to_string(self,items, indentation):
        """Returns a string containing the data in each of the item in
        the item list items indented at the correct level.

        For org-mode the indentation is taken care of by the "indent"
        STARTUP option, so we don't use the parameter here.

        """
        result = ""
        index = 1
        for item in items:
            result += "{}. {}\n".format(
                index,
                item_to_string(item)
                )
            index += 1
        return result
        
