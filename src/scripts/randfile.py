import argparse
import numpy
import os.path

# Sample run command: python3 .\randfile.py -p .\temp\
# TODO ADD EXCEPTIONS TO FUNCTION DOCS
# TODO ADD JPG AND PNG CREATION
# TODO ADD FIND EXISTING FILES FUNCTION


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

def get_unused_file_names(path, extension, number=1, name_num_min=10000, name_num_max=99999):
    """
    Generate a list of numeric file names not currently in use at a given path with a given extension.
    Input:
        path - The directory path for the file.
        extension - The extension spcifying file type.
        number - The number of file names to get. Defaults to 1.
        name_num_min - The minimum number the name will be. Defaults to 10000.
        name_num_max - The maximum number the name will be. Defaults to 99999.
    Output:
        The list of full file paths. Any path includes the given directory path, the generated file name, and the file extension.
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

def create_file(args):
    """
    Creates files using the specified arguments.
    Input:
        args - The specified arguments.
    Ouput:
        Creates files.
        Returns nothing.
    """
    # Get file names
    names = get_unused_file_names(args["path"], args["extension"], number=args["number"])
    # Generate data and write files depending on extension
    for name in names:
        if args["extension"] == "txt":
            data = rand_chars(args["size"])
            # Write new file
            f = open(name, "x")
            for character in data:
                f.write(character)
        else:
            raise Exception("Unimplemented extension specified")
    return

def parse_args():
    """
    Parses the command line arguments.
    Output:
        The dictionary of parsed arguments.
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
    TODO
    """
    # Parse arguments
    args = parse_args()
    # Handle file action
    if args["mode"] == "create":
        create_file(args)
    else:
        raise Exception("Unimplemented mode specified")
    return

if __name__ == '__main__':
    main()