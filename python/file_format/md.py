#!/usr/bin/env python

import re


class md_file:
    """Provides function to read headers and print headers and lists
    to a file using the markdown format.

    """
    def get_name(self):
        """Returns the name of the format."""
        return "md"

    def get_main_file_name(self):
        """Returns the name of the main file associated with this
        format.

        """
        return "meuporg.md"


    def line_to_header(self,line):
        """Returns False if the line does not correspond to a header
        and a list containing [depth, title] otherwise.

        """
        if (re.match("^#+ .+",line) == None):
            return False
        else:
            content = line.split(" ")
            depth = len(content[0])
            if (re.match(".*#+",content[1]) == None):
                title = line[depth:].strip()
            else:
                title = line[depth:len(line)-depth].strip()
            return [depth, title]
            

    def header_to_string(self,depth,title):
        """Returns a string containing a header with the given title
        and depth.

        """
        return "#"*depth + " " + title + " " + "#"*depth
        

    def item_to_string(self,item):
        """Returns the string containing the data in the item
        corresponding to this format.

        """
        return "[{0.description}]({0.location}:{0.line_index})".format(item)
        

    def list_to_string(self,items, indentation):
        """Returns a string containing the data in each of the item in
        the item list items indented at the correct level.

        """
        result = ""
        index = 1
        for item in items:
            result += "{}{}. {}\n".format(
                indentation,
                index,
                item_to_string(item)
                )
            index += 1
        return result
        
