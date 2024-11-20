import os
from datetime import datetime
from pathlib import Path
from baml_client.partial_types import ModuleCatalog, ModuleList, StudyProgrammOverview
import pdfplumber
import re
import sys
import requests
from requests.auth import HTTPBasicAuth
import json
from tqdm import tqdm

sys.path.append(os.path.abspath("./baml_client"))

import baml_client as client
from baml_client import reset_baml_env_vars
import dotenv

dotenv.load_dotenv()
reset_baml_env_vars(dict(os.environ))


def process_pdf(splits, splits_modules, doc_path, doc_name):
    """
    Processes a PDF document by splitting it into sections based on specified split points,
    and assigns a suffix to each section based on whether it pertains to modules, additional information, or other additional information.
    Args:
        splits (list of int): A list of page numbers where the PDF should be split.
                              These are one-indexed and will be converted to zero-indexed.
        splits_modules (list of int): A list indicating whether each split section is about modules (1),
                                      additional information (0), or other additional information (2).
        doc_path (str): The file path to the PDF document to be processed.
        doc_name (str): A postfix used for the folder that the documents are saved to.
    Returns:
        None: The function writes the extracted text to files in an output folder,
              and then moves these files to a timestamped folder.
    """

    # Convert to zero-indexed split points for pdfplumber
    splits = [s - 1 for s in splits]
    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)

    # Process the PDF
    with pdfplumber.open(doc_path) as pdf:
        prev = 0
        for i, current in enumerate(splits[1:], start=1):
            # Extract text from specified pages
            text = "".join([pdf.pages[j].extract_text() for j in range(prev, current)])

            # Determine the suffix based on splits_modules for the current section
            if splits_modules[i - 1] == 1:
                suffix = "_modules"
            elif splits_modules[i - 1] == 0:
                suffix = "_additional_overview"
            elif splits_modules[i - 1] == 2:
                suffix = "_additional_other"
            else:
                raise ValueError(
                    f"Invalid value in splits_modules: {splits_modules[i - 1]}"
                )

            output_file = output_folder / f"split_{i}{suffix}.txt"

            # Write extracted text to file
            with open(output_file, "w", encoding="utf-8") as text_file:
                text_file.write(text)

            prev = current

        # Process last split until the end of the document
        text = "".join(
            [pdf.pages[j].extract_text() for j in range(prev, len(pdf.pages))]
        )
        if splits_modules[-1] == 1:
            suffix = "_modules"
        elif splits_modules[-1] == 0:
            suffix = "_additional"
        elif splits_modules[-1] == 2:
            suffix = "_additional_other"
        else:
            raise ValueError(f"Invalid value in splits_modules: {splits_modules[-1]}")

        output_file = output_folder / f"split_{len(splits)}{suffix}.txt"

        with open(output_file, "w", encoding="utf-8") as text_file:
            text_file.write(text)

    # Move split files to timestamped folder
    timestamped_folder = output_folder / datetime.now().strftime("%Y%m%d_%H%M%S")
    postfix = f"_{doc_name}"
    timestamped_folder = output_folder / (
        datetime.now().strftime("%Y%m%d_%H%M%S") + postfix
    )
    timestamped_folder.mkdir(exist_ok=True)

    for file in output_folder.glob("split_*.txt"):
        file.rename(timestamped_folder / file.name)

    return timestamped_folder


def merge_additional_files(source_folder, merged_file_name="merged_additional.txt"):
    """
    Merges all files in the specified folder that match the pattern "split_*_additional_other.txt" and "split_*_additional_overview.txt" into separate files.
    Args:
        source_folder (str or Path): The folder containing the files to be merged.
        merged_file_name (str, optional): The base name of the output merged files. Defaults to "merged_additional.txt".
    Returns:
        None
    The function performs the following steps:
    1. Sets up the paths for the source folder and the merged files.
    2. Defines regex patterns to extract numbers from filenames like "split_1_additional_other.txt".
    3. Retrieves and sorts the files based on the extracted number.
    4. Opens the merged files in write mode.
    5. Reads the content of each file and writes it to the corresponding merged file,
       adding optional spacing between the contents of each file.
    6. Prints a message indicating that all files have been merged.
    """

    # Set up paths
    source_folder = Path(source_folder)
    merged_additional_other_path = source_folder / f"merged_additional_other.txt"
    merged_additional_overview_path = source_folder / f"merged_additional_overview.txt"

    # Patterns to extract the number from filenames
    additional_other_pattern = re.compile(r"split_(\d+)_additional_other\.txt")
    additional_overview_pattern = re.compile(r"split_(\d+)_additional_overview\.txt")

    # Get and sort files based on the extracted number
    additional_other_files = sorted(
        (file for file in source_folder.glob("split_*_additional_other.txt")),
        key=lambda f: int(additional_other_pattern.search(f.name).group(1)),
    )
    additional_overview_files = sorted(
        (file for file in source_folder.glob("split_*_additional_overview.txt")),
        key=lambda f: int(additional_overview_pattern.search(f.name).group(1)),
    )

    # Function to merge files
    def merge_files(files, output_path):
        with open(output_path, "w", encoding="utf-8") as merged_file:
            for file in files:
                with open(file, "r", encoding="utf-8") as f:
                    merged_file.write(f.read())
                    merged_file.write(
                        "\n\n"
                    )  # Optional: add spacing between contents of each file

    # Merge files
    merge_files(additional_other_files, merged_additional_other_path)
    merge_files(additional_overview_files, merged_additional_overview_path)

    print(
        f"All '_additional_other' files have been merged into {merged_additional_other_path}"
    )
    print(
        f"All '_additional_overview' files have been merged into {merged_additional_overview_path}"
    )


def process_catalog_overview(folder_path):
    """
    Extracts the catalog overview with BAML from a text file and saves it as a JSON file.
    Args:
        folder_path (str): The path to the folder containing the input text file.
    """

    input_path = os.path.join(folder_path, "merged_additional_overview.txt")
    output_path = os.path.join(folder_path, "catalog_overview.json")

    with open(input_path, "r") as file:
        text = file.read()

    catalog = client.b.ExtractStudyProgrammOverview(text)

    catalog_json = catalog.model_dump_json()

    with open(output_path, "w") as json_file:
        json_file.write(catalog_json)


def process_module_list(input_path):
    """
    Extracts a list of modules with BAML from a text file and saves it as a JSON file.
    Args:
        input_path (str): The path to the input text file.
    """
    input_filename = os.path.basename(input_path)
    output_filename = f"{input_filename.split('.')[0]}_list.json"
    output_path = os.path.join(os.path.dirname(input_path), output_filename)

    with open(input_path, "r") as file:
        text = file.read()
        if not text:
            print(f"No text found in {input_path}")
            return

    try:
        module_list = client.b.ExtractModulesList(text)
    except Exception as e:
        print(f"Error extracting module list from {input_path}: {e}")
        return

    catalog_json = module_list.model_dump_json()

    with open(output_path, "w") as json_file:
        json_file.write(catalog_json)


def parse_module_catalog(path) -> ModuleList:
    with open(path, "r") as json_file:
        catalog_json = json_file.read()

        return ModuleList.model_validate_json(catalog_json)


def parse_overview(path) -> StudyProgrammOverview:
    with open(path, "r") as json_file:
        catalog_json = json_file.read()

        return StudyProgrammOverview.model_validate_json(catalog_json)


def merge_json_files(folder):
    merged_data = {"modules": []}

    for file in os.listdir(folder):
        if file.endswith("_list.json"):
            file_path = os.path.join(folder, file)
            with open(file_path, "r") as f:
                data = json.load(f)
                merged_data["modules"].extend(data.get("modules", []))

    output_file = os.path.join(folder, "merged_modules.json")
    with open(output_file, "w") as f:
        json.dump(merged_data, f, indent=4)

    print(f"Merged JSON file created at: {output_file}")


def process_module_files(folder):
    files = [f for f in os.listdir(folder) if f.endswith("_modules.txt")]
    print(files)
    for filename in tqdm(files, desc="Processing module files"):
        file_path = os.path.join(folder, filename)
        print(f"Now processing file: {file_path}")
        try:
            process_module_list(file_path)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")


def fix_module_file(file_path):
    folder = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    fixed_filename = f"{filename.split('.')[0]}_fix.txt"
    fixed_file_path = os.path.join(folder, fixed_filename)

    # Read the content of the original file and write it to the new file
    with open(file_path, "r", encoding="utf-8") as original_file:
        content = original_file.read()
        with open(fixed_file_path, "w", encoding="utf-8") as fixed_file:
            fixed_file.write(content)

    # Process the new fixed file
    try:
        process_module_list(fixed_file_path)
    except Exception as e:
        print(f"Error processing file {fixed_file_path}: {e}")


def format_module_name(name: str) -> str:
    return " ".join(
        (
            word.capitalize() if word else word
        )  # Capitalize first letter, handle empty strings
        for word in name.replace("_", " ").split(" ")
    )


def format_degree_name(name: str) -> str:
    return " ".join(
        (
            word.capitalize() if word else word
        )  # Capitalize first letter, handle empty strings
        for word in name.split("_")
    )


def dict_to_lists(d):
    """
    Converts a dictionary into two lists: one for keys and one for values.
    Args:
        d (dict): The dictionary to be converted.
    Returns:
        tuple: A tuple containing two lists - the first list contains the keys, and the second list contains the values.
    """
    keys = list(d.keys())
    values = list(d.values())
    return keys, values
