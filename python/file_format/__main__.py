#!/usr/bin/env python


from factory import factory

if __name__ == "__main__":
    """A basic test of the classes in this module. The idea is to have
    every file_format to print data and manually check if it seems
    correct.

    """

    file_format_list = [factory.get_format(name) for name in factory.valid_formats]
    for file_format in file_format_list:
        print("\n" + "-"*60 + "\n")
        print("name: {}".format(file_format.get_name()))
        print("main file: {}".format(file_format.get_main_file_name()))
        print("sample headers:")
        for depth in range(1,4):
            header_string = file_format.header_to_string(depth,"depth "+str(depth))
            print(header_string)
            print(file_format.line_to_header(header_string))
