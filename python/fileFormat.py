#!/usr/bin/env python

"""Provides classes and methods to read and write the supported
formats in a standard way.

The different format supported are org (org-mode), vimwiki and
markdown. For each format, a class provides functions to read data
from a file in this format and to write headings and lists to it.

A "Factory" is provided to retrieve the different file formats from
their string representation.

"""

import re


# !SECTION! The classes supporting the different file formats.


# !SUBSECTION! Org-mode files

class OrgFile:
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


    def line_to_header(self, line):
        """Returns False if the line does not correspond to a header
        and a list containing [depth, title] otherwise.

        """
        if (re.match("^\*+ .+$", line) == None):
            return False
        else:
            content = line.split(" ")
            depth = len(content[0])
            title = line[depth:].strip()
            return [depth, title]
            

    def header_to_string(self, depth, title):
        """Returns a string containing a header with the given title
        and depth.

        """
        return "*"*depth + " " + title
        

    def item_to_string(self, item):
        """Returns the string containing the data in the item
        corresponding to this format.

        """
        return "[[file:{0.location}::{0.line_index}][{0.description}]] ({0.location}::{0.line_index})".format(item)
        

    def list_to_string(self, item_list, indentation):
        """Returns a string containing the data in each of the item in
        the item list indented at the correct level.

        For org-mode the indentation is taken care of by the "indent"
        STARTUP option, so we don't use the parameter here.

        """
        result = ""
        index = 1
        for item in item_list:
            result += "{}. {}\n".format(
                index,
                self.item_to_string(item)
                )
            index += 1
        return result
        


# !SUBSECTION! Vimwiki files


class VimwikiFile:
    """Provides function to read headers and print headers and lists
    to a file using the vimwiki format.

    """
    def get_name(self):
        """Returns the name of the format."""
        return "vimwiki"


    def get_main_file_name(self):
        """Returns the name of the main file associated with this
        format.

        """
        return "meuporg.wiki"

    def line_to_header(self, line):
        """Returns False if the line does not correspond to a header
        and a list containing [depth, title] otherwise.

        """
        if (re.match("^=+ .+ =+$", line) == None):
            return False
        else:
            content = line.split(" ")
            depth = len(content[0])
            title = line[depth:len(line)-depth].strip()
            return [depth, title]
            

    def header_to_string(self, depth, title):
        """Returns a string containing a header with the given title
        and depth.

        """
        return "="*depth + " " + title + " " + "="*depth
        

    def item_to_string(self, item):
        """Returns the string containing the data in the item
        corresponding to this format.

        """
        return "[file://{0.location}:{0.line_index}|{0.description}] ({0.location}:{0.line_index})".format(item)
        

    def list_to_string(self, item_list, indentation):
        """Returns a string containing the data in each of the item in
        the item list indented at the correct level.

        """
        result = ""
        for item in item_list:
            result += "{}# {}\n".format(
                indentation,
                self.item_to_string(item)
                )
        return result
        


# !SUBSECTION! Markdown format


class MdFile:
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


    def line_to_header(self, line):
        """Returns False if the line does not correspond to a header
        and a list containing [depth, title] otherwise.

        """
        # !REALTODO! There is a problem with md: the headings have the
        # !trailing "#" are extracted as part of the title.
        if (re.match("^#+ .+", line) == None):
            return False
        else:
            content = line.split(" ")
            depth = len(content[0])
            if (re.match(".*#+", content[1]) == None):
                title = line[depth:].strip()
            else:
                title = line[depth:len(line)-depth].strip()
            return [depth,  title]
            

    def header_to_string(self, depth, title):
        """Returns a string containing a header with the given title
        and depth.

        """
        return "#"*depth + " " + title + " " + "#"*depth
        

    def item_to_string(self, item):
        """Returns the string containing the data in the item
        corresponding to this format.

        """
        return "[{0.description}]({0.location}:{0.line_index})".format(item)
        

    def list_to_string(self, item_list, indentation):
        """Returns a string containing the data in each of the item in
        the item list indented at the correct level.

        """
        result = ""
        index = 1
        for item in item_list:
            result += "{}{}. {}\n".format(
                indentation,
                index,
                self.item_to_string(item)
                )
            index += 1
        return result
        


# !SUBSECTION! Factory building file formats


class Factory:
    """A Factory to get file_format objects from strings representing
    their names.

    """

    """A list containing the string representation of all the file
    formats supported by meuporg.

    """
    valid_formats = ["org", "md", "vimwiki"]
    

    @staticmethod
    def get_format(name):
        """Returns a file_format instance of the correct type
        depending on the name given.
        
        If no such file_format exits, raises an exception.

        """
        if name == "org":
            return OrgFile()
        elif name == "md":
            return MdFile()
        elif name == "vimwiki":
            return VimwikiFile()
        else:
            raise Exception("Unkown file format \"" + name + "\"")

    @staticmethod
    def get_format_list():
        """Returns a list of all the file_format objects available."""
        return [Factory.get_format(name) for name in Factory.valid_formats]



# !SECTION! Test suite


if __name__ == "__main__":
    """A basic test of the classes in this module. The idea is to have
    every file_format to print data and manually check if it seems
    correct.

    """

    file_format_list = [Factory.get_format(name) for name in Factory.valid_formats]
    for file_format in file_format_list:
        print("\n" + "-"*60 + "\n")
        print("name: {}".format(file_format.get_name()))
        print("main file: {}".format(file_format.get_main_file_name()))
        print("sample headers:")
        for depth in range(1, 4):
            header_string = file_format.header_to_string(depth, "depth "+str(depth))
            print(header_string)
            print(file_format.line_to_header(header_string))
