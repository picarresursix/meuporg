#!/usr/bin/env python


from org import org_file
from md import md_file
from vimwiki import vimwiki_file

class factory:
    """A factory to get file_format objects from strings representing
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
            return org_file()
        elif name == "md":
            return md_file()
        elif name == "vimwiki":
            return vimwiki_file()
        else:
            raise Exception("Unkown file format \"" + name + "\"")

    @staticmethod
    def get_format_list():
        """Returns a list of all the file_format objects available."""
        return [factory.get_format(name) for name in factory.valid_formats]
