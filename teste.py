import os

# Define the directory and file names
directory = 'ui'  # replace with your directory path
file_name = 'widget_creator_apostas.py'

# Construct the full file path
file_path = os.path.join(directory, file_name)

# Check if the file exists
if os.path.isfile(file_path):
    print(f"The file '{file_name}' exists in the directory '{directory}'.")
else:
    print(f"The file '{file_name}' does not exist in the directory '{directory}'.")