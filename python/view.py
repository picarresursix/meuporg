#!/usr/bin/env python

# The functions in this file pretty print a list of items in different
# ways. They are grouped in two groups.
#
# First, the functions sorting the list of items into dictionnaries
# with different sets of keys.
#
# Then, the functions outputing the result in different format.



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
    

def org_output(items, depth):
    """Outputs an org representation of the items given.

    Uses keys of a dictionnary as org-headings and output lists as
    numbered org-lists. The indentation of the list and the level of
    the head node is given by the depth argument.

    """
    result = ""
    if isinstance(items,dict):
        for key in sorted(items.keys()):
            for i in range(0,depth):
                result += "*"
            result += " {}\n{}".format(
                str(key),
                org_output(items[key], depth+1)
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
                item.to_entry()
            )
            index += 1
    return result
            


if (__name__ == "__main__"):
     # !TODO! Write it!
     # !TODO! document it!
    print("Bla.")
