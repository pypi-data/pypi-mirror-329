import saft_data_mgmt
import os

# Print module location
print(f"Package installed at: {os.path.dirname(saft_data_mgmt.__file__)}")

# List all files in the package
for root, dirs, files in os.walk(os.path.dirname(saft_data_mgmt.__file__)):
    print(f"Directory: {root}")
    for file in files:
        print(f"  - {file}")