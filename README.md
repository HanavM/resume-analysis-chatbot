This is the Resume Analysis Chatbot

Order to run programs:
1. preprocess.py
2. extract_metadata.py
3. create_output_folder.py
4. main_pipeline.py (main program) 

preprocess.py

To run preprocess.py, run: 
	python3 preprocess.py /path/to/resume/folder
preprocess.py will return:
	All resumes have been preprocessed and saved at: /path/to/preprocessed/resume/folder"
Save that path: /path/to/preprocessed/resume/folder (processed resume dataset path). 

extract_metadata.py

To run extract_metadata.py, run: 
	python3 extract_metadata.py /path/to/preprocessed/resume/folder
extract_metadata.py will return:
	Extracted Metadata at path: /path/to/preprocessed/resume/folder
Save that path: /path/to/preprocessed/resume/folder (processed resume dataset path). 

To run create_output_folder.py, run: 
	python3 create_output_folder.py /path/to/preprocessed/resume/folder
create_output_folder.py will return:
	Folder created successfully at: /path/to/output/folder
Save that path: /path/to/output/folder (output folder path).

main_pipeline.py

To run main_pipeline.py, run: 
	python3 main_pipeline.py /path/to/preprocessed/resume/folder /path/to/output/folder
