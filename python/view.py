#!/usr/bin/env python

# The functions in this file pretty print a list of items in different
# ways. They are grouped in two groups.
#
# First, the functions sorting the list of items into dictionnaries
# with different sets of keys.
#
# Then, the functions outputing the result in different format.

from file_types import *



def extract_name(item_list):
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
                for i in range(0,depth):
                    result += INDENT_MARK[output_format].replace("\\","")
                result += " {}\n{}".format(
                    str(key),
                    output(items[key],depth+1,output_format)
                )
        elif isinstance(items,list):
            indent = ""
            for i in range(0,depth):
                indent += " "
            index = 1
            for item in items:
                result += "{}{}. {}\n".format(
                    indent,
                    index,
                    item.format_entry(ENTRY_FORMAT[output_format])
                )
                index += 1
    return result
            


if (__name__ == "__main__"):
     # !TODO! Write tests for the views.
    items = [
        Item("    // * !TODO! :! * blabla! And bla too!","./here.txt",1),
        Item("blabla bla !FIXREF! blabla! blabla","./here/wait/no/actually/there.bla",123456)
        ]
    print("Bla.")
