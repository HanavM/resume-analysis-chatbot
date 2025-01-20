import os
import argparse

parser = argparse.ArgumentParser(description="Process extracted resume text and generate metadata.")
parser.add_argument("dataset_path", type=str, help="Path to the folder containing processed resume text")
args = parser.parse_args()

dataset_path = args.dataset_path

directory_path = 
output_folder_path = "/".join(directory_path.split("/")[:-1]) + "/outputfolder"

# print(output_folder_path)

try:
    os.makedirs(output_folder_path, exist_ok=True)
    print(f"Folder created successfully at: {output_folder_path}")
except Exception as e:
    print(f"An error occurred while creating the folder: {e}")