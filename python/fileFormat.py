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
import meupUtils


# !SECTION! The classes supporting the different file formats
# ===========================================================


#   !SUBSECTION! Org-mode files
#   ---------------------------


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


    def get_link(self, description, location):
        """Returns an org-mode link with the given description poiting to the
        given location.

        """
        if len(description) == 0:
            description = "link"
        return "[[{}][{}]]".format(location, description)


    def item_to_string(self, item, print_path=True, print_name=True):
        """Returns the string containing the data in the item
        corresponding to this format.

        """
        name = item.name
        desc_with_link = self.get_link(
            item.description,
            "file:{0.file_name}::{0.line_index}".format(item))
        location = "({0.file_name}::{0.line_index})".format(item)
        if print_name and print_path:
            return name + ": " + desc_with_link + " " + location
        elif print_name:
            return name + ": " + desc_with_link
        elif print_path:
            return desc_with_link + " " + location
        else:
            return desc_with_link
            
        

    def list_to_string(self,
                       item_list,
                       indentation="",
                       print_path=True,
                       print_name=True):
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
                self.item_to_string(item,
                                    print_path=print_path,
                                    print_name=print_name)
                )
            index += 1
        return result
        


#   !SUBSECTION! Vimwiki files
#   --------------------------


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
        

    def get_link(self, description, location):
        """Returns vimwiki link with the given description poiting to the
        given location.

        """
        if len(description) == 0:
            description = "link"
        return "[file://{}|{}]".format(location, description)


    def item_to_string(self, item, print_path=True, print_name=True):
        """Returns the string containing the data in the item
        corresponding to this format.

        """
        name = item.name
        desc_with_link = self.get_link(
            item.description,
            "{0.file_name}::{0.line_index}".format(item))
        location = "({0.file_name}:{0.line_index})".format(item)
        if print_name and print_path:
            return name + ": " + desc_with_link + " " + location
        elif print_name:
            return name + ": " + desc_with_link
        elif print_path:
            return desc_with_link + " " + location
        else:
            return desc_with_link
        

    def list_to_string(self,
                       item_list,
                       indentation="",
                       print_name=False,
                       print_path=False):
        """Returns a string containing the data in each of the item in
        the item list indented at the correct level.

        """
        result = ""
        for item in item_list:
            result += "{}# {}\n".format(
                indentation,
                self.item_to_string(item,
                                    print_path=print_path,
                                    print_name=print_name)
                )
        return result
        



#   !SUBSECTION! Markdown format
#   ----------------------------

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
        # !trailing "#" extracted as part of the title.
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


    def get_link(self, description, location):
        """Returns a markdown link with the given description poiting to the
        given location.

        """
        if len(description) == 0:
            description = "link"
        return "[{}]({})".format(description, location)


    def item_to_string(self, item, print_name=True, print_path=True):
        """Returns the string containing the data in the item
        corresponding to this format.

        """
        name = item.name
        desc_with_link = self.get_link(
            item.description,
            "{0.file_name}:{0.line_index}".format(item)) 
        location = "({0.file_name}:{0.line_index})".format(item)
        if print_name and print_path:
            return name + ": " + desc_with_link + " " + location
        elif print_name:
            return name + ": " + desc_with_link
        elif print_path:
            return desc_with_link + " " + location
        else:
            return desc_with_link
        
        return "".format(item)
        

    def list_to_string(self,
                       item_list,
                       indentation="",
                       print_name=False,
                       print_path=False):
        """Returns a string containing the data in each of the item in
        the item list indented at the correct level.

        """
        result = ""
        index = 1
        for item in item_list:
            result += "{}{}. {}\n".format(
                indentation,
                index,
                self.item_to_string(item, 
                                    print_path=print_path,
                                    print_name=print_name)
                )
            index += 1
        return result
        



# !SECTION! Functions using this formats
# ======================================

#   !SUBSECTION! Factory building file formats
#   ------------------------------------------


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


#   !SUBSECTION! output function
#   ----------------------------


def output(items, depth, output_format, print_name=True, path=""):
    """Outputs a representation of the items given in the format
    wanted, which must be in fileFormat.Factory.valid_types.

    Uses keys of a dictionnary as headings and output lists as
    lists. The indentation of the list and the level of the head node
    is given by the depth argument.

    """
    style = Factory.get_format(output_format)
    result = ""
    if isinstance(items, list):
        if (len(items) == 0):
            result = ""
        else:
            result += style.list_to_string(items,
                                           " " * depth,
                                           print_name=print_name,
                                           print_path=(path == ""))
    else:
        for key in sorted(items.keys()):
            if (path == ""):
                heading = style.header_to_string(depth, key)
                partial_output = output(items[key],
                                        depth+1,
                                        output_format,
                                        print_name=print_name,
                                        path="")
            else:
                heading = style.header_to_string(
                    depth,
                    key + " " + style.get_link("=>", path+"/"+key) + " ")
                partial_output = output(items[key],
                                        depth+1,
                                        output_format,
                                        print_name=print_name,
                                        path=path + "/" + key)
            result += "{}\n{}".format(heading, partial_output)
    return result



# !SECTION! Test suite
# ====================


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

    item_list = [
        meupUtils.MeuporgItem("!TODO! blibla", "/path/to/file1", 300, [], False),
        meupUtils.MeuporgItem("!IDEA! blublo", "/path/to/file1", 310, [], False)
    ]
    for file_format in file_format_list:
        print(file_format.list_to_string(
            item_list,
            indentation="  ",
            print_name=True,
            print_path=False))


    item_dict = {
        "path": {
            "to": {
                "file1": [
                    meupUtils.MeuporgItem("!TODO! blibla", "/path/to/file1", 300, [], False),
                    meupUtils.MeuporgItem("!IDEA! blublo", "/path/to/file1", 310, [], False)
                ],
                "file2": [
                    meupUtils.MeuporgItem("!TODO! blibla", "/path/to/file2", 300, [], False),
                    meupUtils.MeuporgItem("!IDEA! blublo", "/path/to/file2", 310, [], False)
                ]},
            "and":  {
                "file1": [
                    meupUtils.MeuporgItem("!TODO! blibla", "/path/to/file1", 300, [], False),
                    meupUtils.MeuporgItem("!IDEA! blublo", "/path/to/file1", 310, [], False)
                ],
                "file2": [
                    meupUtils.MeuporgItem("!TODO! blibla", "/path/to/file2", 300, [], False),
                    meupUtils.MeuporgItem("!IDEA! blublo", "/path/to/file2", 310, [], False)
                ]}
        }
    }
    for file_format in file_format_list:
        style = file_format.get_name()
        print("\n--- {} ---\n{}".format(
            style,
            output(item_dict, 1, style, print_name=True, path="")))
