#!/usr/bin/env python


from org import OrgFile
from md import MdFile
from vimwiki import VimwikiFile

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
