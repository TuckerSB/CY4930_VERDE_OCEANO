import argparse
import numpy
import os
from os import listdir
from PIL import Image
import shutil

# Sample run command: python3 .\randfile.py -p .\temp\
# All images are assumed square

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
    Generate a list of file names that exist in the given directory path with a given extension.
    Input:
        path - The directory path.
        extension - The file extension.
        number - The number of file names to get.
    Output:
        A number long list of file names including path and extension.
    Raise:
        ValueError - If there are not the desired number of existing files in the path with the extension.
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
    return files_of_type[:number]

def get_unused_file_names(path, extension, number=1, name_num_min=10000, name_num_max=99999):
    """
    Generate a list of numeric file names not currently in use at a given path with a given extension.
    Input:
        path - The directory path for the file.
        extension - The extension specifying file type.
        number - The number of file names to get. Defaults to 1.
        name_num_min - The minimum number the name will be. Defaults to 10000.
        name_num_max - The maximum number the name will be. Defaults to 99999.
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

def get_copy_file_names(extension, names):
    """
    Generate a list of unused copy-of-file names.
    Input:
        extension - The extension specifying file type.
        names - The names of files including paths to find copy names for.
    Output:
        Returns a list of copy names for each given name.
    """
    copy_names = []
    for name in names:
        i = 1
        copy_name = name[:len(name) - len(extension) - 1] + "_C-" + str(i) + name[len(name) - len(extension) - 1:]
        while os.path.exists(copy_name):
            i = i + 1
            copy_name = name[:len(name) - len(extension) - 1] + "_C-" + str(i) + name[len(name) - len(extension) - 1:]
        copy_names.append(copy_name)
    return copy_names

def _write_files(args, names, write_open_method = "w"):
    """
    Write files with given names using a given method and specified arguments.
    Input:
        args - The specified arguments.
        names - The file names to write to.
        write_open_method - The writing method specified for opening. Expects a, w, x, or s. Option s is non-standard and shrinks the file
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
            # If overwrite, only overwrite first characters
            if write_open_method == "w":
                f = open(name, "r")
                old_data = list(f.read())
                # If old data is larger than new data overwrite, otherwise just continue with new data
                if len(old_data) > args["size"]:
                    for i in range(args["size"]):
                        old_data[i] = data[i]
                    data = old_data
            # If shrink, only shrink to first number characters at most
            elif write_open_method == "s":
                f = open(name, "r")
                old_data = list(f.read())
                data = old_data[:args["size"]] if args["size"] < len(old_data) else old_data
                write_open_method = "w"
            # Write file
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
            elif write_open_method == "s":
                # Open existing image
                image = Image.open(name)
                # Convert image to array
                old_data = numpy.array(image)
                # Shrink to at most number by number pixels
                if len(old_data) > args["size"]:
                    data = []
                    for i in range(args["size"]):
                        data.append(old_data[i][:args["size"]])
                    data = numpy.asarray(data)
                else:
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
    Creates files based on the command line arguments.
    Input:
        args - The command line arguments.
    Output:
        Creates files.
        Returns nothing.
    """
    # Get new file names
    names = get_unused_file_names(args["path"], args["extension"], number=args["number"])
    # Write with x to ensure new file
    _write_files(args, names, write_open_method="x")
    return

def overwrite_files(args):
    """
    Overwrites files based on the command line arguments.
    Only overwrites part and keeps rest if overwrite size is less than existing file size.
    Input:
        args - The command line arguments.
    Output:
        Overwrites files.
        Returns nothing.
    """
    # Get existing file names
    names = get_used_file_names(args["path"], args["extension"], number=args["number"])
    # Write with w to overwrite
    _write_files(args, names, write_open_method="w")
    return

def append_files(args):
    """
    Appends to files based on the command line arguments.
    Input:
        args - The command line arguments.
    Output:
        Appends to files.
        Returns nothing.
    """
    # Get existing file names
    names = get_used_file_names(args["path"], args["extension"], number=args["number"])
    # Write with a to append
    _write_files(args, names, write_open_method="a")
    return

def copy_files(args):
    """
    Copies files based on the command line arguments.
    Input:
        args - The command line arguments.
    Output:
        Copies files.
        Returns nothing.
    """
    # Get existing file names
    names = get_used_file_names(args["path"], args["extension"], number=args["number"])
    # Get copy file names
    copy_names = get_copy_file_names(args["extension"], names)
    # Copy the files
    for i in range(args["number"]):
        shutil.copyfile( names[i], copy_names[i])
    return

def delete_files(args):
    """
    Deletes files based on the command line arguments after prompting user for confirmation.
    Input:
        args - The command line arguments.
    Output:
        Deletes files.
        Returns nothing.
    """
    # Get existing file names
    names = get_used_file_names(args["path"], args["extension"], number=args["number"])
    # Generate warning
    warning = "Deleting these files,\n"
    for name in names:
        warning = warning + name + "\n"
    warning = warning + "are you sure?(y/n)"
    # Confirm delete
    sure = " "
    while sure not in "yYnN":
        sure = input(warning)
    # Delete files if sure, otherwise print cancelled
    if sure in "yY":
        for name in names:
            os.remove(name)
    else:
        print("Cancelled delete")
    return

def shrink_files(args):
    """
    Shrinks files based on the command line arguments to no greater than the specified size.
    Input:
        args - The command line arguments.
    Output:
        Shrinks files.
        Returns nothing.
    """
    # Get existing file names
    names = get_used_file_names(args["path"], args["extension"], number=args["number"])
    # Write with s to shrink
    _write_files(args, names, write_open_method="s")
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
    elif args["mode"] == "copy":
        copy_files(args)
    elif args["mode"] == "delete":
        delete_files(args)
    elif args["mode"] == "shrink":
        shrink_files(args)
    else:
        raise Exception("Unimplemented mode specified")
    return

if __name__ == '__main__':
    main()