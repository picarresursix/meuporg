#!/usr/bin/env python
# AUTHOR: Leo Perrin <leoperrin@picarresursix.fr>
# Time-stamp: <2013-05-03 16:43:48 leo>

"""Provides utilities to easily build complex conditions an item must
validate. in order to trigger some action.

For instance, 

"""

import re
import meupUtils

class Attribute:
    """Provide a method to check that a given attribute of a meuporg item
    matches one of the regex's of the list of regex' specified at
    construction.

    """

    def __init__(self, attribute, possible_matches):
        """Initializes all the attribute of this instance."""
        if (attribute == "name"
            or attribute == "file_name"
            or attribute == "description"
            or attribute == "section"):
            self.attribute = attribute
        else:
            raise ValueError("Unkown attribute \"" + self.attribute + "\"")
        self.possible_matches = possible_matches
        

    def __str__(self):
        res = "(" + self.attribute
        for regex in self.possible_matches:
            res += " " + regex
        return res + ")"


    def match(self, it):
        """Returns True if and only if the meuporgItem it's field <attribute>
        matches one of the regex's in <possible_values>."""

        if (self.attribute == "name"
            or self.attribute == "file_name"
            or self.attribute == "description"):
            # case of text fields
            if self.attribute == "name":
                field = it.name
            elif self.attribute == "file_name":
                field = it.file_name
            elif self.attribute == "description":
                field = it.description
            for regex in self.possible_matches:
                if re.search(regex, field) != None:
                    return True
            return False
        elif self.attribute == "section":
            # case of list fields
            for regex in self.possible_matches:
                for field in it.sections:
                    if re.search(regex, field) != None:
                        return True
            return False


class Not:
    """Returns the opposite of a criteria."""

    def __init__(self, criteria):
        self.criteria = criteria
        
    def __str__(self):
        return "(not" + str(self.criteria) + ")"

    def match(self, it):
        return not self.criteria.match(it)


class And:
    """Allows to check if the conjunction of two criteria holds for an
    item.

    """

    def __init__(self, criterias):
        self.criterias = criterias

    def __str__(self):
        res = "(and"
        for crit in self.criterias:
            res += " " + str(crit)
        return res + ")"

    def match(self, it):
        for crit in self.criterias:
            if not crit.match(it):
                return False
        return True


class Or:
    """Allows to check if the disjunction of two criteria holds for an
    item.

    """

    def __init__(self, criterias):
        self.criterias = criterias

    def __str__(self):
        res = "(or"
        for crit in self.criterias:
            res += " " + str(crit)
        return res + ")"

    def match(self, it):
        for crit in self.criterias:
            if crit.match(it):
                return True
        return False



class Criteria:
    """Builds a complex criteria an item can match from its string
    representation.

    The string representation of a criteria is LISP-like in the
    following sense. Say you want to encode that only items with name
    "TODO" or "IDEA" and file_name containing "module" should be
    kept. You would write:

    (and (name TODO IDEA) (file_name module))

    """

    def __init__(self, representation):
        """The representation must start with '(' and end with ')'."""
        representation = re.sub(" *\) *", ")", representation)
        representation = re.sub(" *\( *", "(", representation)
        representation = representation[1:len(representation) - 1]
        keyword = re.split("[ \(]",representation)[0]
        representation = representation[len(keyword):]

        if keyword == "and" or keyword == "or" or keyword == "not":
            depth = 0
            sub_criterias = []
            sub_repr = ""
            for char in representation:
                sub_repr += char
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                    if depth < 0:
                        raise ValueError("Mismatched parenthesis in ("
                                         + keyword + representation + ")")
                    if depth == 0:
                        sub_criterias.append(Criteria(sub_repr[:]))
                        sub_repr = ""
            if depth != 0:
                raise ValueError("Mismatched parenthesis in ("
                                 + keyword + representation + ")")
            if keyword == "and":
                self.criteria = And(sub_criterias)
            elif keyword == "or":
                self.criteria = Or(sub_criterias)
            elif keyword == "not":
                if len(sub_criterias) > 1:
                    raise ValueError("'Not' can only have one parameter.")
                else:
                    self.criteria = Not(sub_criterias[0])
        else:
            possible_matches = [regex for regex in re.split(" +",representation)
                                if len(regex) > 0]
            self.criteria = Attribute(keyword, possible_matches)


    def __str__(self):
        return str(self.criteria)


    def match(self, string):
        return self.criteria.match(string)



if __name__ == "__main__":
    meupUtils.parse_directory(
        path = "..",
        include = ["org", "el", "md"],
        exclude = ["readme"],
        include_backup_files = False,
        include_hidden_files = False)
    crit = Criteria("(and (file_name el py) (or (name TODO) (not (name IDEA))))")
    print crit
    print Or([
        And([
            Attribute("file_name", ["el"]),
            Attribute("name", ["TODO"])
        ]),
        Not(Or([
            Attribute("description", ["test", "explication"]),
            Attribute("section", ["test", "explication"])
        ]))
        ])
    index = 1
    for it in meupUtils.MeuporgItem.__item_list__:
        if crit.match(it):
            print("{item_number}. !{0.name}!  {0.description} "
                  "(line {0.line_index} in "
                  "{0.file_name}".format(it, item_number = index))
        index += 1

