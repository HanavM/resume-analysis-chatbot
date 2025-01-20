import shutil
import os
import PyPDF2
import argparse


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

#insert dataset of resume path here
parser = argparse.ArgumentParser(description="Process a folder of PDFs and extract text.")
parser.add_argument("resume_folder", type=str, help="Path to the folder containing PDF resumes")
args = parser.parse_args()

dataset_path_og = args.resume_folder  # Use the path from the argument

new_folder_name = "resume_dataset_processed"
dataset_path_new = os.path.join(os.path.dirname(dataset_path_og), new_folder_name)

os.makedirs(dataset_path_new, exist_ok=True)

for file in os.listdir(dataset_path_og):
  file_path = os.path.join(dataset_path_og, file)
  if (file_path.endswith("pdf")):
    try:
      folder_path_new = os.path.join(dataset_path_new,file.strip(".pdf"))
      os.makedirs(folder_path_new, exist_ok=True)
      file_path_new = os.path.join(folder_path_new, file)
      shutil.copy2(file_path, file_path_new)
      extracted_text = extract_text_from_pdf(file_path_new)
      txt_file_path = os.path.join(folder_path_new, "text_extracted.txt")
      with open(txt_file_path, "w", encoding="utf-8") as txt_file:
          txt_file.write(extracted_text)
    except:
      pass

print("All resumes have been preprocessed and saved at:", dataset_path_new)