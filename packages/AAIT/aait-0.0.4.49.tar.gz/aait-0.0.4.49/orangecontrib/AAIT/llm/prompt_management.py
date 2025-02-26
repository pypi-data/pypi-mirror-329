import os

prompt_templates = {
    "llama":
"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>""",



    "mistral": """<s>[INST] {user_prompt} [/INST]""",



    "solar":
"""### User: {user_prompt}

### Assistant:""",



    "qwencoder":
"""<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{user_prompt}<|im_end|>
<|im_start|>assistant\n""",
}


stop_tokens = {
    "llama": "<|eot_id|>",
    "mistral": "</s>",
    "qwencoder": "<|im_end|>"
}


model_types = {
    "solar-10.7b-instruct-v1.0.Q6_K.gguf": "solar",
    "solar-10.7b-instruct-v1.0-uncensored.Q6_K.gguf": "solar",
    "Mistral-7B-Instruct-v0.3.Q6_K.gguf": "mistral",
    "Qwen2.5.1-Coder-7B-Instruct-Q6_K.gguf": "qwencoder"
}


def apply_prompt_template(model_name, request, system_prompt="", raw_request=False):
    """
    Apply a prompt template based on the given model name and request.

    Parameters:
        model_name (str): The name of the model used to determine its type.
        request (str): The user request or input to embed into the template.
        system_prompt (str, optional): A system-level instruction or context
            to include in the prompt. Defaults to an empty string.
        raw_request (bool, optional): A bool to indicate that all the formating
            has been managed in the request already, so no transformation is applied
            to the request.
    """
    if raw_request:
        return request
    model_name = os.path.basename(model_name)
    # If the definitions exist in the dicts
    try:
        # Get the model type
        model_type = model_types[model_name]
        # Get the template for the model type
        prompt = prompt_templates[model_type]
    except KeyError as e:
        print(f"Model type or prompt template not implemented for your model {model_name}. See prompt_management.py. (detail: {e})")
        return request
    # If the template includes a system prompt, add it
    if "{system_prompt}" in prompt:
        prompt = prompt.replace("{system_prompt}", system_prompt)
    # Otherwise, concatenate the system prompt with the request
    else:
        request = system_prompt + request
    # Place the request in the template
    prompt = prompt.replace("{user_prompt}", request)
    return prompt


def get_stop_token(model_name):
    """
    Get the stop token according to the model name / type.

    Parameters:
        model_name (str): The name of the model used to determine its type.
    """
    # If there is a stop token
    try:
        # Get the model type
        model_type = model_types[model_name]
        # Get the template for the model type
        stop_token = stop_tokens[model_type]
    except KeyError as e:
        print(f"Your model {model_name} has no stop token defined. See prompt_management.py. (detail: {e})")
        return None
    return stop_token


# models = ["solar-10.7b-instruct-v1.0.Q6_K.gguf", "solar-10.7b-instruct-v1.0-uncensored.Q6_K.gguf",
#           "Mistral-7B-Instruct-v0.3.Q6_K.gguf", "Qwen2.5.1-Coder-7B-Instruct-Q6_K.gguf"]
# q = "Quelles sont les planètes du système solaire ?"
#
# for model in models:
#     p = apply_prompt_template(model, q)
#     print(p, "\n\n\n\n")





