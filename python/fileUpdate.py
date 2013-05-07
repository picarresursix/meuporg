#!/usr/bin/env python
# AUTHOR: Leo Perrin <leoperrin@picarresursix.fr>
# Time-stamp: <2013-05-07 15:28:59 leo>

import os
import re

import itemDb
import fileFormat
import meupUtils



class MainFile():
    """An interface to read an write to the main meuporg file."""
    
# !SECTION! Initialization
# ========================

    def __init__(self):
        """Initializes the path at which the file is by seraching for a
        meup.org (org), meuporg.wiki (vimiwiki) or a meuporg.md (markdown)
        file.

        To do so, we go up the directory tree until we find a folder
        containing such a file and then set self.path to the full path
        to the said file.
    
        If a directory whose full path contains less than two "/" is
        encountered, we stop because we went to deep (used to prevent
        infinite loop).
    
        If nothing was found, self.path is set to the empty string.

        """
        self.path = ""
        found = False
        while (len(os.getcwd().split(os.path.sep)) > 2) and not found:
            folder_content = os.listdir(os.path.curdir)
            for style in fileFormat.Factory.get_format_list():
                if style.get_main_file_name() in folder_content:
                    self.path = os.path.join(
                        os.getcwd(),
                        style.get_main_file_name()
                    )
                    found = True
            os.chdir(os.path.pardir)
        if self.path != "":
            self.init_configuration()

            
    def init_configuration(self):
        """Reads the configuration of the files to include and exclude from
        the main file.

        """
        with open(self.path, 'r') as f:
            self.include = []
            self.exclude = []
            self.include_backup_files = False
            self.include_hidden_files = False
            for line in f.readlines():
                line = line.rstrip()
                if re.search("!INCLUDE!", line) != None:
                    content = "".join(line.split("!")[2:])
                    self.include = re.split(" *", content)[1:]

                elif re.search("!EXCLUDE!", line) != None:
                    content = "".join(line.split("!")[2:])
                    self.exclude = re.split(" *", content)[1:]
                    
                elif re.search("!INCLUDE_BACKUP_FILES!", line) != None:
                    content = "".join(line.split("!")[2:]).strip()
                    self.include_backup_files = (content == "YES")

                elif re.search("!INCLUDE_HIDDEN_FILES!", line) != None:
                    content = "".join(line.split("!")[2:]).strip()
                    self.include_hidden_files = (content == "YES")

        print self.include
        print self.exclude

# !SECTION! Update the main file
# ==============================

    def update(self,
               include=[],
               exclude=[],
               include_hidden_files=False,
               include_backup_files=False):
        """Updates the main file."""

        # !SUBSECTION! Opening old main file and cd-ing to its directory
        path_to_old_file = self.path
        print("updating {}".format(path_to_old_file))
        if (path_to_old_file == ""):
            print("Could not find a main file. Aborting.")
            exit(1)

        dir_old_file, file_name = os.path.split(path_to_old_file)
        os.chdir(dir_old_file)
    
        # !SUBSECTION! Find the file format from the file name
        for potential_style in fileFormat.Factory.get_format_list():
            if (potential_style.get_main_file_name() == file_name):
                style = potential_style

        # !SUBSECTION! Setting up the variables controlling file inclusion
        self.include += include
        self.exclude += exclude
        self.include_backup_files = (self.include_backup_files
                                     or include_backup_files)
        self.include_hidden_files = (self.include_hidden_files
                                     or include_hidden_files)
        print self.include
        print self.exclude
        
        # !SUBSECTION! Getting items
        meupUtils.parse_directory(
            path=".",
            include=self.include,
            exclude=self.exclude,
            include_backup_files=self.include_backup_files,
            include_hidden_files=self.include_hidden_files)
        item_db = itemDb.MeuporgItemDB(meupUtils.MeuporgItem.__item_list__)

        # !SUBSECTION! Setting up variables
        with open(file_name, 'r') as f_old:
            new_content = ""
            depth = 0
            recording = True
            local_criteria = []
        
            # !SUBSECTION! Updating the content
            line_list = f_old.readlines()
            for i in range(0, len(line_list)):
                line = line_list[i].rstrip()
                print_items = ""

                # !SUBSECTION! Dealing with headers
                if style.line_to_header(line) != False:
                    old_depth = depth
                    depth, heading = style.line_to_header(line)
                    if (old_depth > depth):
                        recording = True
                        for j in range(0, old_depth-depth+1):
                            local_criteria.pop()
                    elif (old_depth == depth):
                        local_criteria.pop()

                    # !SUBSSUBSECTION! Dealing with possible items insertion
                    content = re.findall("[A-Za-z_0-9\-]+", heading)
                    if content[0] == "Items":
                        if len(content) == 1:
                            print_items = "name"
                        else:
                            print_items = content[1]

                    # !SUBSSUBSECTION! Dealing with Criteria
                    if (i+1 < len(line_list)
                        and re.search("!Criteria!", line_list[i+1])) != None:
                        clause_repr = re.findall("\(.*\)", line_list[i+1])[0]
                        local_criteria.append(itemDb.Criteria(clause_repr))
                    else:
                        local_criteria.append(itemDb.AlwaysTrue())

                # !SUBSECTION! Checking if items should be printed after this line
                elif re.search("!Items!", line) != None:
                    print_items = re.findall("[^! ][a-z]+[^! ]", line)[1]

                # !SUBSECTION! Putting what we just read back in the file
                new_content += line + "\n"

                # !SUBSECTION! Dealing with the possible printing of items
                if print_items == "name":
                    new_content += fileFormat.output(
                        item_db.select_and_sort_by_name(itemDb.And(local_criteria)),
                        depth+1,
                        style.get_name(),
                        print_name=False,
                        path="")
                elif print_items == "directories":
                    new_content += fileFormat.output(
                        item_db.select_and_sort_by_directories(itemDb.And(local_criteria)),
                        depth+1,
                        style.get_name(),
                        print_name=True,
                        path = ".")
                elif print_items == "linear":
                    new_content += fileFormat.output(
                        item_db.select(itemDb.And(local_criteria)),
                        depth+1,
                        style.get_name(),
                        print_name=True,
                        path="")
                print_items = ""

                # !CONTINUE! 

        #  writing the new file
        print new_content
        with open(self.path, 'w') as f_new:
            f_new.write(new_content)
            print "[DONE]"



if __name__ == "__main__":
    m = MainFile()
    m.update()
