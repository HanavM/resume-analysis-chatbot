import os

directory_path = "/content/drive"
output_folder_path = "/".join(directory_path.split("/")[:-1]) + "/outputfolder"

# print(output_folder_path)

try:
    os.makedirs(output_folder_path, exist_ok=True)
    print(f"Folder created successfully at: {output_folder_path}")
except Exception as e:
    print(f"An error occurred while creating the folder: {e}")