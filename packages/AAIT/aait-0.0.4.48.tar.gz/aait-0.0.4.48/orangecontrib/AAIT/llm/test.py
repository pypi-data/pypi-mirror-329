# import os
# import torch
# import json
# import functions_Finetuning
# from datasets import concatenate_datasets, Dataset
# from transformers import TrainingArguments, Trainer
#
# # Check GPU usage
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")
#
#
# # Model to finetune
# model_name = r"C:\Users\lucas\aait_store\Models\NLP\Chocolatine-3B-Instruct"
# model, tokenizer = functions_Finetuning.load_model_with_lora(model_name)
#
#
# # Generate datasets for training and evaluation
# # Load text data from a TXT file
# txt_path = r"C:\Users\lucas\Desktop\BDD_Helico\manuel_volFamaKiss.txt"
#
# def load_text_dataset(txt_path):
#     """
#     Loads and returns a dataset from a text file.
#     """
#     with open(txt_path, 'r', encoding='utf-8') as file:
#         text = file.read()
#     return Dataset.from_dict({"text": [text]})
#
# # Tokenize the dataset
# def tokenize_function(examples):
#     """
#     Tokenizes the dataset and splits it into blocks of the specified size.
#     """
#     block_size = 512  # Adjust this depending on your GPU memory
#     tokenized_output = tokenizer(
#         examples["text"],
#         truncation=True,
#         max_length=block_size,
#         return_overflowing_tokens=True,
#         return_length=True,
#     )
#
#     # Map tokens to input_ids and labels for CLM
#     input_ids = tokenized_output["input_ids"]
#     return {"input_ids": input_ids, "labels": input_ids}
#
# # Load and process the dataset
# raw_dataset = load_text_dataset(txt_path)
# tokenized_dataset = raw_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
#
# # Split into train and eval datasets
# split_datasets = tokenized_dataset.train_test_split(test_size=0, seed=42)
# tokenized_train_dataset = split_datasets["train"]
# tokenized_eval_dataset = split_datasets["test"]
#
# # Training Arguments with Epochs
# training_args = TrainingArguments(
#     output_dir="./results",
#     per_device_train_batch_size=1,
#     gradient_accumulation_steps=8,
#     num_train_epochs=100,  # Adjust epochs here
#     learning_rate=5e-5,
#     fp16=True,
#     logging_dir="./logs",
#     save_total_limit=1,
#     logging_steps=10,
#     #evaluation_strategy="epoch",         # Evaluate the model at the end of each epoch
#     #metric_for_best_model="eval_loss"
# )
#
# # Trainer
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_train_dataset,
#     #eval_dataset=tokenized_eval_dataset,
#     tokenizer=tokenizer,
# )
#
#
# # Test function to evaluate before and after fine-tuning
# def test_model(model, tokenizer, test_queries):
#     for query in test_queries:
#         prompt = f"{query}"
#         input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
#         output = model.generate(input_ids, max_length=100, temperature=0, top_p=0)
#         response = tokenizer.decode(output[0], skip_special_tokens=True)
#         response = response.replace(query, "")
#         # response = response.split(r"\n")[0]
#         print(f"Query: {query}")
#         print(f"Response: {response}\n")
#         print("#############")
#
#
# # Test model before fine-tuning
# print("Testing model before fine-tuning:")
# test_queries = [
#     "Le poids à vide maximal de l'hélicoptère KISS 209 MF est",
#     "### Question: Quel est le poids maximal à vide de l'hélicoptère KISS 209 MF ?\n### Réponse:"
# ]
# test_model(model, tokenizer, test_queries)
#
# # Fine-tune the model
# print("Starting training...")
# trainer.train()
# print("Training completed!")
# # Test model after fine-tuning
# print("Testing model after fine-tuning:")
# test_model(model, tokenizer, test_queries)


from chonkie import WordChunker
from sentence_transformers import SentenceTransformer

tokenizer = r"C:\Users\lucas\aait_store\Models\NLP\all-mpnet-base-v2"
model = SentenceTransformer(tokenizer)
# Initialize the chunker
chunker = WordChunker(
    tokenizer=model.tokenizer,
    chunk_size=10,  # maximum tokens per chunk
    chunk_overlap=3  # overlap between chunks
)

# Chunk a single piece of text
chunks = chunker.chunk("Woah! Chonkie, the chunking library is so cool! I love the tiny hippo hehe.")
for chunk in chunks:
    print(f"Chunk: {chunk.text}", type(chunk.text))
    print(f"Tokens: {chunk.token_count}")