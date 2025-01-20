This is the Resume Analysis Chatbot

Order to run programs:
1. preprocess.py
2. extract_metadata.py
3. create_output_folder.py
4. main_pipeline.py (main program) 

preprocess.py

	To run preprocess.py, run: "python3 preprocess.py /path/to/resume/folder"
	Once preprocess.py terminates, a path will outputted that specifies where the processed resume dataset is.
	Save that path (processed resume dataset path). 

extract_metadata.py

To run extract_metadata.py, run: "python3 extract_metadata.py /path/to/preprocessed/resume/folder"
/path/to/preprocessed/resume/folder is the path saved from preprocess.py
Once this terminates, the same path will be outputted. 
Save that path (processed resume dataset path).

create_output_folder.py

To run create_output_folder.py, run: "python3 create_output_folder.py /path/to/preprocessed/resume/folder"
/path/to/preprocessed/resume/folder is the path saved from extract_metadata.py
Once this terminates, an output folder path will be outputted. 
Save that path (output folder path).

main_pipeline.py

To run create_output_folder.py, run: "python3 main_pipeline.py /path/to/preprocessed/resume/folder /path/to/output/folder"
/path/to/preprocessed/resume/folder is the path saved from extract_metadata.py
/path/to/output/folder is the path saved from create_output_folder.py
