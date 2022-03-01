import argparse
from logging import exception
from tkinter import EXCEPTION
import numpy
import os.path
from os import listdir
from PIL import Image

# Sample run command: python3 .\randfile.py -p .\temp\
# TODO COPY, DELETE, SHRINK
# TODO CARRY EXCEPTIONS UP FUNCTION DOCUMENTS? Single point of truth annoyance. Could say "exceptions of this sub function"

# DATA GENERATION
###################################################################################################
def rand_chars(n):
    """
    Generate a list of n non-special ascii-characters.
    Input:
        n - The number of character to generate.
    Output:
        An n long list of generated characters.
    """
    ascii_numbers = numpy.random.randint(size=n, low=32, high=126)
    characters = []
    for i in range(n):
        characters.append(chr(ascii_numbers[i]))
    return characters

def rand_pixels(cols, rows=1, color=True):
    """
    Returns a rows by cols list of pixels.
    Input:
        rows - The number of rows in the list of generated pixels. Defaults to 1.
        cols - The number columns in the list of generated pixels.
        color - Whether or not 3 values should be generated for rgb or one for grayscale. Defaults to True for rgb.
    Output:
        A rows by cols list of pixels for grayscale, cols * 3 for rgb.
    """
    return numpy.random.randint(255, size=(rows, cols, 3 if color else cols), dtype=numpy.uint8)

# FILE ACTIONS
###################################################################################################
def get_used_file_names(path, extension, number=1):
    """
    TODO
    """
    # Get all files in path
    files = [file for file in listdir(path) if os.path.isfile(path + file)]
    # Filter by extension
    files_of_type = []
    for file in files:
        if file[len(file) - len(extension):] == extension:
            files_of_type.append(path + file)
    if len(files_of_type) < number:
        raise ValueError("Files of the given type in the given path are less than desired number")
    return files_of_type

# TODO COPY NAMES IMPLEMENTATION
def get_unused_file_names(path, extension, number=1, name_num_min=10000, name_num_max=99999, copy=False):
    """
    Generate a list of numeric file names not currently in use at a given path with a given extension.
    Input:
        path - The directory path for the file.
        extension - The extension spcifying file type.
        number - The number of file names to get. Defaults to 1.
        name_num_min - The minimum number the name will be. Defaults to 10000.
        name_num_max - The maximum number the name will be. Defaults to 99999.
        copy - Whether or not the new names are for copied files. Defaults to False.
    Output:
        The list of full file paths. Any path includes the given directory path, the generated file name, and the file extension.
    Raise:
        OverflowError - If there are not enough unique file names with an extension available in a directory between min and max.
    """
    names = []
    name_num = name_num_min
    for i in range(number):
        name = path + str(name_num) + "." + extension
        # Generate file name that does not already exist
        ## Increment if name is taken up to max
        while(os.path.exists(name) and name_num <= name_num_max):
            name_num = name_num + 1
            name = path + str(name_num) + "." + extension
        if name_num == name_num_max + 1:
            raise OverflowError("Could not create number of files of specified type in the specified path")
        # Add name to list
        names.append(name)
        name_num = name_num + 1
    return names

def _write_files(args, names, write_open_method = "w"):
    """
    Write files with given names using a given method and specified arguments.
    Input:
        args - The specified arguments.
        names - The file names to write to.
        write_open_method - The writing method specified for opening. Expects a, w, or x.
    Ouput:
        Writes files.
        Returns nothing.
    Raise:
        Exception - If the extension requested is not implemented.
        Exception - If the write_open_method is not supported.
    """
    # Generate data and write files depending on extension
    for name in names:
        if args["extension"] == "txt":
            # Generate data
            data = rand_chars(args["size"])
            # Only overwrite first characters
            if write_open_method == "w":
                f = open(name, "r")
                old_data = list(f.read())
                # If old data is larger than new data overwrite, otherwise just continue with new data
                if len(old_data) > args["size"]:
                    for i in range(args["size"]):
                        old_data[i] = data[i]
                    data = old_data
            # Write new file
            f = open(name, write_open_method)
            for character in data:
                f.write(character)
            f.close()
        elif args["extension"] == "jpg" or args["extension"] == "png":
            if write_open_method == "a":
                # Open existing image
                image = Image.open(name)
                # Convert image to array
                old_data = numpy.array(image)
                # Generate data to expand old image by size in each dimension
                ## Get pixels for expanded backwards L shape
                ## m by m old extended by n in both dimensions
                ## adds m by n rectangle right and an n by m + n rectangle bottom
                rect_right = rand_pixels(rows=len(old_data), cols=args["size"], color=True)
                rect_bottom = rand_pixels(rows=args["size"], cols=len(old_data) + args["size"], color=True)
                ## Append right rectangle to the ends of rows
                data = []
                for i in range(len(rect_right)):
                    joined_row = numpy.concatenate((old_data[i], rect_right[i]))
                    data.append(joined_row)
                ## Append bottom rectangle unerneath rows
                data.extend(rect_bottom)
                data = numpy.asarray(data)
            elif write_open_method == "w":
                # Open existing image
                image = Image.open(name)
                # Convert image to array
                old_data = numpy.array(image)
                # Generate data to overwrite
                data = rand_pixels(rows=args["size"], cols=args["size"], color=True)
                # If old data is larger than new data overwrite, otherwise just continue with new data
                if len(old_data) > args["size"]:
                    for i in range(args["size"]):
                        for j in range(args["size"]):
                            old_data[i][j] = data[i][j]
                    data = old_data
            elif write_open_method == "x":
                # Generate data
                data = rand_pixels(rows=args["size"], cols=args["size"], color=True)
            else:
                raise Exception("Unexpected write method used")
            # Convert Pixels to image
            image = Image.fromarray(data, mode="RGB")
            # Write new file
            image.save(name)
        else:
            raise Exception("Unimplemented extension specified")
    return

def create_files(args):
    """
    TODO
    """
    # Get new file names
    names = get_unused_file_names(args["path"], args["extension"], number=args["number"])
    # Write with x to ensure new file
    _write_files(args, names, write_open_method="x")
    return

def overwrite_files(args):
    """
    TODO
    """
    # Get existing file names
    names = get_used_file_names(args["path"], args["extension"], number=args["number"])
    # Write with w to overwrite
    _write_files(args, names, write_open_method="w")
    return

def append_files(args):
    """
    TODO
    """
    # Get existing file names
    names = get_used_file_names(args["path"], args["extension"], number=args["number"])
    # Write with a to append
    _write_files(args, names, write_open_method="a")
    return

# MAIN
###################################################################################################
def parse_args():
    """
    Parses the command line arguments.
    Output:
        The dictionary of parsed arguments.
    Raise:
        ValueError - If the path given is not a valid directory.
        ValueError - If the number of files given is not >= 1.
        ValueError - If the sie given is not >= 1.
    """
    # Define argument options
    ## Actions that need new data
    new_data_modes = [
        "create",
        "append",
        "overwrite"
    ]
    ## Actions that do not need new data
    no_new_data_modes = [
        "copy",
        "delete",
        "shrink"
    ]
    mode_choices = new_data_modes + no_new_data_modes
    # File types
    ## Files containing text data
    text_file_types = [
        "txt"
    ]
    ## Files containing image data
    image_file_types = [
        "jpg",
        "png"
    ]
    file_type_choices = text_file_types + image_file_types

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="The path to act on files. Should not be an important folder", required=True)
    parser.add_argument("-e", "--extension", type=str, default=file_type_choices[0], choices=file_type_choices, help="The file type extension")
    parser.add_argument("-m", "--mode", type=str, default=mode_choices[0], choices=mode_choices, help="The mode of interaction with the files")
    parser.add_argument("-n", "--number", type=int, default=1, help="The number of files to make")
    parser.add_argument("-s", "--size", type=int, default=100, help="The dimension in units appropriate for the file type")
    args = vars(parser.parse_args())
    # Check for valid arguments
    if not os.path.isdir(args["path"]):
        raise ValueError("Invalid path. Must be a directory")
    elif args["number"] < 1:
        raise ValueError("Number of files must be >= 1")
    elif args["size"] < 1:
        raise ValueError("Size must be >= 1")
    return args

def main():
    """
    Performs the correct file action based on the command line arguments.
    Raise:
        Exception - If the mode requested is not implemented.
    """
    # Parse arguments
    args = parse_args()
    # Handle file action
    if args["mode"] == "create":
        create_files(args)
    elif args["mode"] == "overwrite":
        overwrite_files(args)
    elif args["mode"] == "append":
        append_files(args)
    else:
        raise Exception("Unimplemented mode specified")
    return

if __name__ == '__main__':
    main()