#!/usr/bin/env python

# The functions in this file pretty print a list of items in different
# ways. They are grouped in two groups.
#
# First, the functions sorting the list of items into dictionnaries
# with different sets of keys.
#
# Then, the functions outputing the result in different format.

from file_types import *
from item import *
import re


def sort_by_name(item_list):
    """Turns a list into a dictionnary where items are sorted by their
    names.

    """
    result = {}
    for item in item_list:
        if item.name in result.keys():
            result[item.name].append(item)
        else:
            result[item.name] = [item]
    return result


def pop_item_by_location(items, patterns):
    """Goes through the items in the list and builds a new list
    containing all items whose locations matches all the
    patterns. These items are removed from the list passed in
    parameter.

    """

    result = []
    for i in reversed(range(0,len(items))):
        keep_it = True
        for pattern in patterns:
            if (re.match(pattern,items[i].location) == None):
                keep_it = False
        if keep_it:
            result.append(items[i])
            items.pop(i)
    return result
        
    

def output(items, depth, output_format):
    """Outputs a representation of the items given in the format
    wanted, which must be in VALID_TYPE.

    Uses keys of a dictionnary as org-headings and output lists as
    numbered org-lists. The indentation of the list and the level of
    the head node is given by the depth argument.

    """
    if output_format not in VALID_TYPE:
        # !TODO! Switch to a proper exception in the output function.
        print("Unkown file format")
        exit(1)
    else:
        result = ""
        if isinstance(items,dict):
            for key in sorted(items.keys()):
                partial_output = output(items[key],depth+1,output_format)
                if (partial_output != ""):
                    heading = " " + key + " "
                    for i in range(0,depth):
                        heading = HEADING_TEMPLATE[output_format].format(heading)
                    result += "{}\n{}".format(
                        heading,
                        partial_output
                    )
        elif isinstance(items,list):
            if (len(items) == 0):
                result = ""
            else:
                indent = ""
                for i in range(0,depth):
                    indent += " "
                index = 1
                for item in reversed(items):
                    result += "{}{}. {}\n".format(
                        indent,
                        index,
                        item.format_entry(ENTRY_FORMAT[output_format])
                    )
                    index += 1
    return result
            


if (__name__ == "__main__"):
     # !TODO! Write tests for the views.
    items = {
        "bla": [
            Item("    // * !TODO! :! * blabla! And bla too!","./here.txt",1),
            Item("blabla bla !FIXREF! blabla! blabla","./here/wait/no/actually/there.bla",123456)
        ],
        "blo": {
            "blu" :
            [
                Item("    // * !IDEA! :! * blabla! And bla too!","./here.txt",1),
                Item("blabla bla !IDEA! blabla! blabla","./here/wait/no/actually/there.bla",123456)
            ],
            "bly" :
            [
                Item("    // * !TODO! :! * blabla! And bla too!","./here.txt",1),
                Item("blabla bla !FIXREF! blabla! blabla","./here/wait/no/actually/there.bla",123456)
            ]
        }
    }
    print(output(items, 1, "org"))
    print(output(items, 1, "md"))
    print(output(items, 1, "wiki"))
