import os
import subprocess

DB = {}

# Get the path to the "python" directory relative to the current working directory
python_dir = os.path.join(os.getcwd(), "coding", "python")

# Loop through each file in the "python" directory
for filename in os.listdir(python_dir):
    # Check if the file ends with ".py"
    if filename.endswith(".py"):
        # Get the full path to the file
        filepath = os.path.join(python_dir, filename)

        # Read in the contents of the file
        with open(filepath, "r") as f:
            contents = f.read()

        # Run the file and capture the output
        result = subprocess.run(["python", filepath], capture_output=True, text=True)

        # Store the contents and result in the dictionary
        DB[filename] = {"contents": contents, "result": result.stdout}

