#!/usr/bin/env python

from collections import defaultdict

import file_format
from criteria import Criteria
from item import MeuporgItem


def sort_by_name(item_list):
    """Returns a dictionnary where the keys are the item names and
    the entries are list of the items having this name.

    """
    result = defaultdict(list)
    for item in flatten_to_list(item_list):
        result[item.name] += [item]
    return result


def flatten_to_list(items):
    """"Destroys" the sorting of some items by taking all the items in
    a dictionnary and putting them in a "flat" list. If the list
    contains a list, the content of this list is added to the main
    one.

    If given a list of items, does not modify it.

    """
    if isinstance(items, list):
        result = []
        for elmt in items:
            if isinstance(elmt, list) or isinstance(elmt, dict):
                result += flatten_to_list(elmt)
            else:
                result.append(elmt)
        return result
    elif isinstance(items, dict):
        result = []
        for key in items.keys():
            result += flatten_to_list(items[key])
        return result
        
    

def pop_item_by_patterns(items,  pattern_list):
    """Goes through the items in the list and builds a new list
    containing all items matching (in the sense of the Criteria class)
    all the patterns. These items are removed from the list passed in
    parameter.

    """
    if isinstance(items, dict):
        result = {}
        for key in items.keys():
            result[key] = pop_item_by_patterns(items[key],  pattern_list)
    elif isinstance(items, list):
        result = []
        for i in reversed(range(0, len(items))):
            keep_it = True
            item = items[i]
            for pattern in pattern_list:
                if not Criteria(item).match(pattern):
                    keep_it = False
            if keep_it:
                result.append(item)
                items.pop(i)
    return result
        
    

def output(items, depth, output_format):
    """Outputs a representation of the items given in the format
    wanted, which must be in file_format.Factory.valid_types.

    Uses keys of a dictionnary as headings and output lists as
    lists. The indentation of the list and the level of the head node
    is given by the depth argument.

    """
    style = file_format.Factory.get_format(output_format)
    result = ""
    if isinstance(items, dict):
        for key in sorted(items.keys()):
            partial_output = output(items[key], depth+1, output_format)
            if (partial_output != ""):
                heading = style.header_to_string(depth, key)
                result += "{}\n{}".format(
                    heading,
                    partial_output
                )
    elif isinstance(items, list):
        if (len(items) == 0):
            result = ""
        else:
            indent = ""
            for i in range(0, depth):
                indent += " "
            result += style.list_to_string(reversed(items), indent)
    return result
            


if (__name__ == "__main__"):
    item_list = {
        "bla": [
            MeuporgItem("    // * !TODO! :! * blabla! And bla too!", "./here.txt", 1),
            MeuporgItem("blabla bla !FIXREF! blabla! blabla", "./here/wait/no/actually/there.bla", 123456)
        ],
        "blo": {
            "blu" :
            [
                MeuporgItem("    // * !IDEA! :! * blabla! And bla too!", "./here.txt", 1),
                MeuporgItem("blabla bla !IDEA! blabla! blabla", "./here/wait/no/actually/there.bla", 123456)
            ],
            "bly" :
            [
                MeuporgItem("    // * !TODO! :! * blabla! And bla too!", "./here.txt", 1),
                MeuporgItem("blabla bla !FIXREF! blabla! blabla", "./here/wait/no/actually/there.bla", 123456)
            ]
        }
    }
    print(output(item_list, 1, "org"))
    print(output(item_list, 1, "md"))
    print(output(item_list, 1, "vimwiki"))
    fixref = pop_item_by_patterns(item_list, ["FIXREF"])
    print("FIXREF:\n{}".format(output(fixref, 1, "org")))
    todo = pop_item_by_patterns(item_list, ["TODO"])
    print("TODO:\n{}".format(output(todo, 1, "org")))
    remainer = sort_by_name(item_list)
    print("REMAINER:\n{}".format(output(remainer, 1, "org")))
