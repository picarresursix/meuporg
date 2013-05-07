#!/usr/bin/env python
# AUTHOR: Leo Perrin <leoperrin@picarresursix.fr>
# Time-stamp: <2013-05-07 15:07:33 leo>

"""Provides utilities to easily select some items and build complex
conditions an item must validate in order to trigger some action.

"""

import re
import meupUtils
from collections import defaultdict


# !SECTION! Boolean management
# ============================


#  !SUBSECTION! Attribute class
#  ----------------------------

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
        if isinstance(possible_matches, str):
            self.possible_matches = [possible_matches]
        else:
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



#  !SUBSECTION! Not class
#  ----------------------------


class Not:
    """Returns the opposite of a criteria."""

    def __init__(self, criteria):
        self.criteria = criteria
        
    def __str__(self):
        return "(not" + str(self.criteria) + ")"

    def match(self, it):
        return not self.criteria.match(it)


#  !SUBSECTION! AlwaysTrue class
#  ----------------------------


class AlwaysTrue:
    """Always returns True."""

    def __str__(self):
        return "True"

    def match(self, it):
        return True



#  !SUBSECTION! AlwaysFalse class
#  ----------------------------


class AlwaysFalse:
    """Always returns False."""
        
    def __str__(self):
        return "False"

    def match(self, it):
        return False


#  !SUBSECTION! And class
#  ----------------------------


class And:
    """Allows to check if the conjunction of several criteria holds for an
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

    def append(self, criteria):
        self.criterias.append(criteria)

    def pop(self):
        return self.criterias.pop()


#  !SUBSECTION! Or class
#  ---------------------

class Or:
    """Allows to check if the disjunction of several criteria holds for an
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

    def append(self, criteria):
        self.criterias.append(criteria)

    def pop(self):
        return self.criterias.pop()


#  !SUBSECTION! Criteria class
#  ---------------------------


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



# !SECTION! A poor man's database for the items
# =============================================

def tree():
    return defaultdict(tree)


class MeuporgItemDB:
    """Stores items and provides method to obtain items depending on a
    wide range of criteria.

    When items are retrieved from it, they are removed from it.

    """
    
    def __init__(self, item_list):
        """Initializes a new databade from a list of items. """
        self.item_list = item_list


    # !SUBSECTION! Sorting methods
    # ----------------------------

    def sort_by_name(self,item_list):
        """Returns a dictionnary whose keys are the names of the items in the
        list and its values the lists of the items having the
        corresponding name.
        
        """
        result = defaultdict(list)
        for it in item_list:
            result[it.name].append(it)
        return result


    def sort_by_directories(self,item_list):
        """Returns a dictionnary whose keys are the folders and the files used
        in the file_name attribute of the items in the list given as a
        parameter. The nodes corresponding to files contain a list of
        all the items in the file.

        The tree has a depth as low as possible: if your working
        directory is /path/to/dir but all the items in item_list are
        in /path/to/dir/module/submodule, returns a tree starting at
        submodule.

        """

        result = tree()
        for it in item_list:
            pointer = result
            splitted_path = it.file_name.split('/')
            for i in range(0, len(splitted_path) - 1):
                if splitted_path[i] not in pointer.keys():
                    pointer[splitted_path[i]] = tree()
                pointer = pointer[splitted_path[i]]
            file_name = splitted_path[len(splitted_path) - 1]
            if file_name not in pointer.keys():
                pointer[file_name] = [it]
            else:
                pointer[file_name].append(it)
        while (len(result.keys()) == 1
               and not isinstance(result[result.keys()[0]], list)):
            result = result[result.keys()[0]]
        return result
        


    # !SUBSECTION! Obtaining items from the db
    # ----------------------------------------

    def select(self,
               criteria=None,
               name=[],
               file_name=[],
               sections=[],
               description=[]):
        """Returns a list containing all the items which match the criteria
        (if provided) or those whose attributes match at least one
        regex in all of the list provided.

        EXAMPLE: select_and_erase(file_name=["el", "py"], name=["TODO"])

        returns a list of all the items in self.items such that their
        file_name attribute contains "el" or "py" and their name
        contains "TODO".

        If criteria is not None, the other parameters are ignored.

        """
        if criteria == None:
            attribute_list = []
            if len(name) > 0:
                attribute_list.append(Attribute("name", name))
            if len(file_name) > 0:
                attribute_list.append(Attribute("file_name", file_name))
            if len(sections) > 0:
                attribute_list.append(Attribute("sections", sections))
            if len(description) > 0:
                attribute_list.append(Attribute("description", description))
            if len(attribute_list) > 0:
                match = And(attribute_list).match
            else:
                match = lambda x : True # everything matches
        else:
            match = criteria.match

        new_item_list = []
        result = []
        for it in self.item_list:
            if not it.is_heading and match(it):
                result.append(it)
            else:
                new_item_list.append(it)
        self.item_list = new_item_list
        return result


    def select_and_sort_by_name(self,
               criteria=None,
               name=[],
               file_name=[],
               sections=[],
               description=[]):
        item_list = self.select(criteria=criteria,
                                name=name,
                                file_name=file_name,
                                sections=sections,
                                description=description)
        return self.sort_by_name(item_list)


    def select_and_sort_by_directories(self,
               criteria=None,
               name=[],
               file_name=[],
               sections=[],
               description=[]):
        item_list = self.select(criteria=criteria,
                                name=name,
                                file_name=file_name,
                                sections=sections,
                                description=description)
        return self.sort_by_directories(item_list)



# !SECTION! Tests
# ===============


if __name__ == "__main__":
    meupUtils.parse_directory(
        path = "..",
        include = ["org$", "el$", "md$", "py$"],
        exclude = ["readme"],
        include_backup_files = False,
        include_hidden_files = False)
    crit = Criteria("(and (file_name el$ py$ md$))")
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

    db = MeuporgItemDB(meupUtils.MeuporgItem.__item_list__)
    item_dict = db.select_and_sort_by_name()
    for key in item_dict.keys():
        print "-- " + key
        for it in item_dict[key]:
            print "  {} | {}:{}".format(it.name,
                                        it.file_name,
                                        it.line_index)
    
    # index = 1
    # for it in db.select_and_erase(crit):
    #     print("{item_number}. !{0.name}!  {0.description} "
    #           "(line {0.line_index} in "
    #           "{0.file_name}".format(it, item_number = index))
    #     index += 1

    # for it in db.select_and_erase(name=["IDEA"]):
    #     print("{item_number}. !{0.name}!  {0.description} "
    #           "(line {0.line_index} in "
    #           "{0.file_name}".format(it, item_number="@"))

    # for it in db.select_and_erase(file_name=["org$"]):
    #     print("{item_number}. !{0.name}!  {0.description} "
    #           "(line {0.line_index} in "
    #           "{0.file_name}".format(it, item_number="$"))

    # for it in db.select_and_erase():
    #     print("{item_number}. !{0.name}!  {0.description} "
    #           "(line {0.line_index} in "
    #           "{0.file_name}".format(it, item_number="_"))

