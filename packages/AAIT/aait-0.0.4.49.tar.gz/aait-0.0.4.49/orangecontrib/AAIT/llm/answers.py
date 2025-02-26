import copy
import os
import GPUtil

from gpt4all import GPT4All
from Orange.data import Domain, StringVariable, Table


if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.llm import prompt_management
else:
    from orangecontrib.AAIT.llm import prompt_management



def check_gpu(model_path, argself):
    """
    Checks if the GPU has enough VRAM to load a model.

    Args:
        model_path (str): Path to the model file.
        argself (OWWidget): OWQueryLLM object.

    Returns:
        bool: True if the model can be loaded on the GPU, False otherwise.
    """
    if model_path is None:
        argself.use_gpu = False
        return
    if not model_path.endswith(".gguf"):
        argself.use_gpu = False
        argself.error("Model is not compatible. It must be a .gguf format.")
        return
    # Calculate the model size in MB with a 1500 MB buffer
    model_size = os.path.getsize(model_path) / (1024 ** 3) * 1000
    model_size += 1500
    # If there is no GPU, set use_gpu to False
    if len(GPUtil.getGPUs()) == 0:
        argself.use_gpu = False
        argself.information("Running on CPU. No GPU detected.")
        return
    # Else
    else:
        # Get the available space on the first GPU
        gpu = GPUtil.getGPUs()[0]
        free_vram = gpu.memoryFree
    # If there is not enough space on GPU
    if free_vram < model_size:
        # Set use_gpu to False
        argself.use_gpu = False
        argself.warning(f"Running on CPU. GPU seems to be too small for this model (available: {free_vram} || required: {model_size}).")
        return
    # If there is enough space on GPU
    else:
        try:
            # Import the Llama library
            from llama_cpp import Llama
            # Load the model and test it
            model = Llama(model_path, n_ctx=4096, n_gpu_layers=-1)
            answer = model("What if ?", max_tokens=20)
            # If it works, set use_gpu to True
            argself.use_gpu = True
            argself.information("Running on GPU.")
            return
        # If importing Llama and reading the model doesn't work
        except Exception as e:
            # Set use_gpu to False
            argself.use_gpu = False
            argself.warning(f"GPU cannot be used. (detail: {e})")
            return



def generate_answers(table, model_path, use_gpu=False, progress_callback=None, argself=None):
    """
    open a model base on llama/gpy4all api
    return input datatable + answer column
    """
    if table is None:
        return

    # Copy of input data
    data = copy.deepcopy(table)
    attr_dom = list(data.domain.attributes)
    metas_dom = list(data.domain.metas)
    class_dom = list(data.domain.class_vars)

    # Load model
    if os.path.exists(model_path):
        model = load_model(model_path, use_gpu=use_gpu, n_gpu_layers=-1)
    else:
        print(f"Model could not be found: {model_path} does not exist")
        return

    # Generate answers on column named "prompt"
    try:
        rows = []
        for i, row in enumerate(data):
            features = list(data[i])
            metas = list(data.metas[i])
            prompt = prompt_management.apply_prompt_template(model_path, str(row["prompt"]))
            answer = run_query(prompt, model=model, use_gpu=use_gpu, stream=True, argself=argself)
            metas += [answer]
            rows.append(features + metas)
            if progress_callback is not None:
                progress_value = float(100 * (i + 1) / len(data))
                progress_callback(progress_value)
    except ValueError as e:
        print("An error occurred when trying to generate an answer:", e)
        return
    #model.close()

    # Generate new Domain to add to data
    answer_dom = [StringVariable("Answer")]

    # Create and return table
    domain = Domain(attributes=attr_dom, metas=metas_dom + answer_dom, class_vars=class_dom)
    out_data = Table.from_list(domain=domain, rows=rows)
    return out_data


def load_model(path, use_gpu=False, n_gpu_layers=0):
    """
    if llamacpp is installed run llama else run gpt4all api
    """
    if use_gpu:
        from llama_cpp import Llama
        model = Llama(path,
                      n_ctx=4096,
                      n_gpu_layers=n_gpu_layers)
    else:
        model = GPT4All(model_path=path,
                        model_name=path,
                        n_ctx=4096,
                        allow_download=False, verbose=True)
    return model


def query_cpu(prompt, model, max_tokens=4096, temperature=0, top_p=0.95, top_k=40, repeat_penalty=1.1, stream=False, argself=None):
    """
    do not use : memory leak
    """
    if not stream:
        output = model.generate(prompt,
                                max_tokens=max_tokens,
                                temp=temperature,
                                top_p=top_p,
                                top_k=top_k,
                                repeat_penalty=repeat_penalty)
    else:
        output = ""
        for token in model.generate(prompt,
                                    max_tokens=max_tokens,
                                    temp=temperature,
                                    top_p=top_p,
                                    top_k=top_k,
                                    repeat_penalty=repeat_penalty,
                                    streaming=True):
            output += token
            if argself is not None:
                if argself.stop:
                    break
    return output.strip()


def query_gpu(prompt, model, max_tokens=4096, temperature=0, top_p=0.95, top_k=40, repeat_penalty=1.1, stream=False, argself=None):
    """
    do not use : memory leak
    """
    if not stream:
        output = model(prompt)
                       # max_tokens=max_tokens,
                       # temperature=temperature,
                       # top_p=top_p,
                       # top_k=top_k,
                       # repeat_penalty=repeat_penalty)["choices"][0]["text"]
    else:
        output = ""
        for token in model(prompt,
                           max_tokens=max_tokens,
                           temperature=temperature,
                           top_p=top_p,
                           top_k=top_k,
                           repeat_penalty=repeat_penalty,
                           stream=True):
            output += token["choices"][0]["text"]
            if argself is not None:
                if argself.stop:
                    break
    return output.strip()


def run_query(prompt, model, use_gpu=False, max_tokens=4096, temperature=0, top_p=0.95, top_k=40, repeat_penalty=1.1, stream=False, argself=None):
    """
    DO NOT USE : MEMORY LEAK
    """
    if use_gpu:
        return query_gpu(prompt, model, max_tokens, temperature, top_p, top_k, repeat_penalty, stream, argself=argself)
    else:
        return query_cpu(prompt, model, max_tokens, temperature, top_p, top_k, repeat_penalty, stream, argself=argself)
