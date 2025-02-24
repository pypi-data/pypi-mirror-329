import os
import json
import ntpath

from Orange.data import Table, Domain, StringVariable

import fitz



def process_documents(dirpath):
    if dirpath is None or not os.path.exists(dirpath):
        return None, None
    # get path from user selection
    embeddings = check_for_embeddings(dirpath)
    files_to_process = get_files_to_process(dirpath, embeddings)

    # Set selected path in the saved embeddings
    if embeddings is not None:
        for row in embeddings:
            row["path"] = dirpath

    rows = []
    for file in files_to_process:
        # Get the text content from the file
        content = extract_text_from_pdf(file)
        filename = ntpath.basename(file)
        # Build a row containing dirpath | filename | content
        row = [dirpath, filename, content]
        rows.append(row)

    # Build a table with the constructed rows
    path_var = StringVariable("path")
    name_var = StringVariable("name")
    content_var = StringVariable("content")
    domain = Domain(attributes=[], metas=[path_var, name_var, content_var])
    out_data = Table.from_list(domain=domain, rows=rows)
    return out_data, embeddings


def get_files_to_process(folder_path, table=None):
    """
    Finds all PDF files in a folder (including subfolders) that are not already in the table.
    The comparison is based on "name" (relative path from the main folder) instead of full paths.

    :param folder_path: Path to the folder to scan for documents.
    :param table: Orange Data Table with columns "path", "name", and "content".
    :return: List of paths to files not present in the table (by name, including subfolder structure).
    """
    #TODO
    # Supported file extensions
    supported_extensions = [".pdf"]

    # Read the json containing file sizes
    filepath_sizes = os.path.join(folder_path, "sizes.json")
    if os.path.exists(filepath_sizes):
        with open(filepath_sizes, "r") as json_file:
            sizes = json.load(json_file)
    else:
        sizes = dict()

    # Extract the existing file names from the Orange Data Table
    if table:
        existing_names = set(table[:, "name"].metas.flatten())  # Extract names from the table
    else:
        existing_names = set()

    # Walk through the folder and its subfolders
    new_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Check if the file has a supported extension
            if os.path.splitext(file)[1].lower() in supported_extensions:
                # Compute the relative name (including subfolder structure)
                relative_name = os.path.relpath(os.path.join(root, file), folder_path)
                # Add the file if its relative name is not already in the table
                filepath = os.path.join(root, file)
                if relative_name not in existing_names:
                    new_files.append(filepath)
                    sizes[relative_name] = os.path.getsize(filepath)
                # If the file is in the table, verify if the file has been modified (comparing the size)
                else:
                    new_size = os.path.getsize(filepath)
                    if relative_name not in sizes.keys():
                        sizes[relative_name] = new_size
                    else:
                        old_size = sizes[relative_name]
                        if old_size != new_size:
                            new_files.append(filepath)
                            table = remove_from_table(relative_name, table)
                            sizes[relative_name] = new_size
    with open(filepath_sizes, "w") as json_file:
        json.dump(sizes, json_file, indent=4)
    return new_files


def remove_from_table(filename, table):
    filtered_table = Table.from_list(domain=table.domain,
                                      rows=[row for row in table if row["name"].value != filename])
    return filtered_table


def check_for_embeddings(folder_path):
    """
    Check for an embeddings.pkl file in a given folder. Return its content if it exists.

    Parameters:
        folder_path (str): The path to the folder where embeddings.pkl may exist.

    Returns:
        Table or None: The content of embeddings.pkl.
    """
    filepaths = [os.path.join(folder_path, "embeddings_question.pkl"),
                 os.path.join(folder_path, "embeddings.pkl")]
    for filepath in filepaths:
        if os.path.exists(filepath):
            data = Table.from_file(filepath)
            return data
    else:
        return None


def extract_text_from_pdf(pdf_path):
    """
    Extrait le texte d'un fichier PDF.

    :param pdf_path: Chemin vers le fichier PDF.
    :return: Texte extrait du PDF sous forme de chaîne.
    """
    try:
        # Ouvre le fichier PDF
        pdf_document = fitz.open(pdf_path)
        extracted_text = ""

        # Parcourt toutes les pages et extrait le texte
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            extracted_text += page.get_text()

        pdf_document.close()
        return extracted_text
    except Exception as e:
        print(f"Erreur lors de l'extraction de texte depuis {pdf_path}: {e}")
        return None



def get_pages_of_extract(pdf_path, extract):
    """
    Identify the pages that a given extract belongs to.

    :param pdf_path: The path of the pdf to search in.
    :param extract: The text snippet to locate.
    :return: A list of page numbers the extract spans.
    """
    full_text, page_mapping = load_pdf_with_sparse_mapping(pdf_path)
    # Find the start index of the extract in the full text
    start_index = full_text.find(extract)
    if start_index == -1:
        return []  # Extract not found

    # Determine the end index of the extract
    end_index = start_index + len(extract) - 1

    # Find all pages the extract spans
    pages = []
    for page, (start, end) in page_mapping.items():
        if start <= end_index and end >= start_index:
            pages.append(page)

    if pages == []:
        return [1]
    return pages


def load_pdf_with_sparse_mapping(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    page_mapping = {}  # Sparse mapping: {page_num: (start_index, end_index)}

    for page_num in range(len(doc)):
        page_text = doc[page_num].get_text()
        start_index = len(full_text)
        full_text += page_text
        end_index = len(full_text) - 1
        page_mapping[page_num + 1] = (start_index, end_index)

    doc.close()
    return full_text, page_mapping