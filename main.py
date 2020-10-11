# This program is written without optimizations for easier understanding.
# Loops are used instead of mapping, list comprehension, or lambda
# Loops should be "fast enough" for us for this example

command_file = open(r"commands.txt","r")
command_list_input = command_file.readlines()

command_list = []
# Convert all commands to lowercase, remove leading and trailing white space, and then add to command_list
for command in command_list_input:
    command_list.append(command.lower().strip())

print(command_list)

command_file.close()
