import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from uuid import uuid4
import json
from transformers import pipeline, logging
import transformers
import torch
import argparse
import ast
from langchain_core.documents import Document
import os
import shutil
import numpy as np
from huggingface_hub import login
from message_bases import message_base_for_prompt,  generation_base_0, generation_base_1 #base prompts extracted from message_bases.py
transformers.logging.set_verbosity_error()
# insert hugging face access token here.
# Make sure to get access to meta-llama/Llama-3.2-3B-Instruct on HuggingFace at https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
login(token="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")

documents_per_field = {}
all_resumes = []
idx = 0

parser = argparse.ArgumentParser(description="Main pipeline")
parser.add_argument("dataset_path", type=str, help="Path to the folder containing processed resume text")

parser.add_argument("output_folder", type=str, help="Path to output folder.")
args = parser.parse_args()

dataset_path = args.dataset_path
output_folder = args.output_folder

def add_vector(field, text, index, split_threshold):
  text_split = text.split(" ")
  idx =0
  while (True):
    if (idx > len(text_split)):
      break

    text_temp = " ".join(text_split[idx: min(len(text_split), idx+split_threshold)])
    # print(text_temp)
    documents_per_field[str(field)].append(Document(
                  page_content=str(text_temp),
                  metadata={"id": index, "field": field},
              ))
    idx += split_threshold

def make_document(field, text, index, split_threshold):
  if (type(text) == str):
    # print(text)
    add_vector(field, text, index, split_threshold)

  if (type(text) == dict):
    for field_temp in text:
      make_document(field, text[field_temp],index, split_threshold)

  if (type(text) == list):
    for temp in text:
      make_document(field, temp,index, split_threshold)

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()

def rank_documents(all_scores_per_doc):
    max_length = max(len(row) for row in all_scores_per_doc)
    padded_scores = np.array([row + [0] * (max_length - len(row)) for row in all_scores_per_doc])

    flattened_scores = padded_scores.flatten()
    softmaxed_scores = softmax(flattened_scores)

    reshaped_scores = softmaxed_scores.reshape(len(all_scores_per_doc), -1)
    sum_per_doc = reshaped_scores.sum(axis=1)
    ranked_indices = np.argsort(sum_per_doc)[::-1]

    return [(index, sum_per_doc[index]) for index in ranked_indices]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

logging.set_verbosity_error()
model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cuda",
)
terminators = [
    pipe.tokenizer.eos_token_id,
    pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

split_threshold_per_field = {
    "name": 1000,
    "summary": 50,
    "education": 10,
    "experience": 10,
    "skills": 10,
    "certifications": 4,
    "platforms": 10,
    "interests": 1000,
    "contact_info": 1000,
    "projects": 15,
    "languages": 1000,
}

query_threshold_per_field = {
    "name": 0.5,
    "summary": 0.5,
    "education": 0.5,
    "experience": 0.5,
    "skills": 0.5,
    "certifications": 0.5,
    "platforms": 0.5,
    "interests": 0.5,
    "contact_info": 0.5,
    "projects": 0.5,
    "languages": 0.5,
}


print("Creating Vector Store")

for resume_folder in os.listdir(dataset_path)[:100]:
  resume_folder_path = os.path.join(dataset_path, resume_folder)
  for file in os.listdir(resume_folder_path):
    file_path = os.path.join(resume_folder_path,file)
    if (file_path.endswith("json")):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            all_resumes.append(data)
            for i in data:
              if (str(i) not in documents_per_field.keys()):
                documents_per_field[str(i)] = []
              make_document(str(i), data[i], idx, split_threshold_per_field[str(i)])
            idx += 1

vector_stores_per_field = {}
for field in documents_per_field:
  index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
  vector_store = FAISS(
      embedding_function=embeddings,
      index=index,
      docstore=InMemoryDocstore(),
      index_to_docstore_id={},
  )
  uuids = [str(uuid4()) for _ in range(len(documents_per_field[field]))]
  vector_store.add_documents(documents=documents_per_field[field], ids=uuids)
  vector_stores_per_field[field] = vector_store

prompt_build_up = ""
print("Finished Creating Vector Store")
iteration_idx = 0

while (True):
  iteration_idx += 1
  prompt = input("User > ")
  if (prompt == "exit"):
    break
  prompt_build_up += prompt

  # === Structure Prompt ===
  complete_prompt = message_base_for_prompt + [{"role": "system", "content": prompt_build_up}]
  terminators = [
      pipe.tokenizer.eos_token_id,
      pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
  ]


  prompt_dict = None

  with torch.no_grad():
      outputs = pipe(
          complete_prompt,
          max_new_tokens=3000,
          eos_token_id=terminators,
          do_sample=True,
          temperature=0.1,
          top_p=0.9,
      )
      response = outputs[0]["generated_text"][-1]["content"]
      prompt_dict = ast.literal_eval(response)


  # === Filter Resumes ===
  possible_values = [True] * idx
  all_scores_per_doc = [0] * idx
  for i in range(idx):
    all_scores_per_doc[i]= []

  for field in prompt_dict:
    if (prompt_dict[field] == None):
      continue
    if (type(prompt_dict[field]) != list):
      prompt_dict[field] = [prompt_dict[field]]

    for query in prompt_dict[field]:
      results = vector_stores_per_field[field].similarity_search_with_relevance_scores(
          query,
          k=idx,
      )

      scores = [score for _, score in results]
      score_threshold = query_threshold_per_field[field] = 0.5

      filtered_results = [
          (doc, adjusted_score)
          for (doc, _), adjusted_score in zip(results, scores)
          if adjusted_score > score_threshold
      ]
      count = len(filtered_results)

      passes = [False] * idx
      for doc, normalized_score in filtered_results:
        passes[(doc.metadata)['id']] = True
        all_scores_per_doc[(doc.metadata)['id']].append(float(normalized_score))
      for val in range(len(passes)):
        if passes[val] == False:
          possible_values[val] = False


  # === Ranking Resumes ===
  valid_resumes = []
  all_scores_per_doc_filtered = []
  for i in range(len(possible_values)):
    if (possible_values[i] == True):
      all_scores_per_doc_filtered.append(all_scores_per_doc[i])
      valid_resumes.append([all_scores_per_doc[i] ,i])


  ranked_documents = rank_documents(all_scores_per_doc_filtered)

  all_resumes_text = ""

  for i in range(2):
    all_resumes_text += ("Candidate " + str(i)+":\n")
    all_resumes_text += str(all_resumes[ranked_documents[i][0]])
    all_resumes_text += "\n"


  full_resumes_text = "prompt: " + prompt +"\n\n"
  for i in range(len(ranked_documents)):
    full_resumes_text += ("Candidate " + str(i)+":\n")
    full_resumes_text += str(all_resumes[ranked_documents[i][0]])
    full_resumes_text += "\n\n"


  #create a txt file with the contents being full_resumes_text and save it into /content/outputfolder
  file_path = os.path.join(output_folder, f"full_resumes{iteration_idx}.txt")

  # Write the contents to the file
  with open(file_path, "w") as file:
      file.write(full_resumes_text)

  # === Response from model ===
  complete_prompt_generator = generation_base_0 + [{"role": "generator in a RAG pipeline", "content": "this was the prompt given: '" + prompt + "'"}]
  complete_prompt_generator = complete_prompt_generator + generation_base_1
  complete_prompt_generator = complete_prompt_generator + [{"role": "generator in a RAG pipeline", "content": "these are the filtered resumes: " + all_resumes_text}]

  terminators = [
      pipe.tokenizer.eos_token_id,
      pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
  ]

  print("Bot >", end=" ")
  with torch.no_grad():
      outputs = pipe(
          complete_prompt_generator,
          max_new_tokens=500,
          eos_token_id=terminators,
          do_sample=True,
          temperature=0.9,
          top_p=0.9,
      )
      response = outputs[0]["generated_text"][-1]["content"]
      print(response)
      print(f"All the resumes have been saved to: full_resumes{iteration_idx}.txt")