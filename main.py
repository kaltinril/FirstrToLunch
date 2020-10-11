# This program is written without optimizations for easier understanding.
# Loops are used instead of mapping, list comprehension, or lambda
# Loops should be "fast enough" for us for this example

# Load file: Load a file and return the commands
def loadfile(filename):
    # Open the file and read all lines into a list
    command_file = open(filename, "r")
    command_list_input = command_file.readlines()

    # Convert all commands to lowercase, remove leading and trailing white space, and then add to command_list
    command_list = []
    for command in command_list_input:
        command_list.append(command.lower().strip())

    print(command_list)
    command_file.close()

    return command_list


def main():
    command_list = loadfile("commands.txt")


if __name__ == "__main__":
    main()
