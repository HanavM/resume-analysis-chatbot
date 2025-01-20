from huggingface_hub import login
import os
import torch
from transformers import pipeline
import json
import argspace
from message_bases import message_base_for_processing #base prompt extracted from message_bases.py

parser = argparse.ArgumentParser(description="Process extracted resume text and generate metadata.")
parser.add_argument("dataset_path", type=str, help="Path to the folder containing processed resume text")
args = parser.parse_args()

dataset_path = args.dataset_path

# insert hugging face access token here.
# Make sure to get access to meta-llama/Llama-3.2-3B-Instruct on HuggingFace at https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
login(token="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")

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

print("Finished downloading model.")

count = 0
for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        ends_with = file.split(".")[-1]
        if ends_with != "txt":
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except:
            print("Failed when getting text from .txt file")
            continue

        complete_prompt = message_base_for_processing + [{"role": "system", "content": text}]

        try:
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

          # Convert to JSON and save
          output_path = os.path.join(folder_path, "output_metadata_3.json")
          metadata_dict = json.loads(response)
          with open(output_path, "w") as file:
              json.dump(metadata_dict, file, indent=4)
          print("JSON saved successfully to:",output_path)

        except Exception as e:
            print("Failed when processing with LLaMA model:", str(e))

        count += 1


print("Finished converting:", count, " resumes")
