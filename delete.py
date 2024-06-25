import os

# Specify the directory where the files are located
names = [
    "cristobal",
    "david",
    "diego",
    "gabriel",
    "isidora",
    "javier",
    "magdalena",
    "porte",
]

for name in names:
    folder_path = f"data/{name}/screenshots"
    # Loop through each file in the directory
    for filename in os.listdir(folder_path):
        # Check if the file is a PNG and starts with "screenshot"
        if filename.startswith("screenshot") and filename.endswith(".png"):
            # Create the full path to the file
            file_path = os.path.join(folder_path, filename)
            # Delete the file
            os.remove(file_path)
            print(f"Deleted {file_path}")

    # Print completion message
    print("Finished deleting all matching PNG files.")
