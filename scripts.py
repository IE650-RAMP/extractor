import os
from datetime import datetime
from pathlib import Path
from baml_client.partial_types import ModuleCatalog, ModuleList, StudyProgrammOverview
import pdfplumber
from pathlib import Path
import re
import sys
import requests
from requests.auth import HTTPBasicAuth

sys.path.append(os.path.abspath("./baml_client"))

import baml_client as client
from baml_client import reset_baml_env_vars
import dotenv

dotenv.load_dotenv()
reset_baml_env_vars(dict(os.environ))


def process_pdf(splits, splits_modules, doc_path):
    """
    Processes a PDF document by splitting it into sections based on specified split points,
    and assigns a suffix to each section based on whether it pertains to modules or additional information.
    Args:
        splits (list of int): A list of page numbers where the PDF should be split.
                              These are one-indexed and will be converted to zero-indexed.
        splits_modules (list of int): A list indicating whether each split section is about modules (1)
                                      or additional information (0).
        doc_path (str): The file path to the PDF document to be processed.
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
            suffix = "_modules" if splits_modules[i - 1] == 1 else "_additional"
            output_file = output_folder / f"split_{i}{suffix}.txt"

            # Write extracted text to file
            with open(output_file, "w", encoding="utf-8") as text_file:
                text_file.write(text)

            prev = current

        # Process last split until the end of the document
        text = "".join(
            [pdf.pages[j].extract_text() for j in range(prev, len(pdf.pages))]
        )
        suffix = "_modules" if splits_modules[-1] == 1 else "_additional"
        output_file = output_folder / f"split_{len(splits)}{suffix}.txt"

        with open(output_file, "w", encoding="utf-8") as text_file:
            text_file.write(text)

    # Move split files to timestamped folder
    timestamped_folder = output_folder / datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_folder.mkdir(exist_ok=True)

    for file in output_folder.glob("split_*.txt"):
        file.rename(timestamped_folder / file.name)


def merge_additional_files(source_folder, merged_file_name="merged_additional.txt"):
    """
    Merges all files in the specified folder that match the pattern "split_*_additional.txt"
    into a single file.
    Args:
        source_folder (str or Path): The folder containing the files to be merged.
        merged_file_name (str, optional): The name of the output merged file. Defaults to "merged_additional.txt".
    Returns:
        None
    The function performs the following steps:
    1. Sets up the paths for the source folder and the merged file.
    2. Defines a regex pattern to extract numbers from filenames like "split_1_additional.txt".
    3. Retrieves and sorts the files based on the extracted number.
    4. Opens the merged file in write mode.
    5. Reads the content of each '_additional' file and writes it to the merged file,
       adding optional spacing between the contents of each file.
    6. Prints a message indicating that all '_additional' files have been merged.
    """

    # Set up paths
    source_folder = Path(source_folder)
    merged_file_path = source_folder / merged_file_name

    # Pattern to extract the number from filenames like "split_1_additional.txt"
    file_pattern = re.compile(r"split_(\d+)_additional\.txt")

    # Get and sort files based on the extracted number
    additional_files = sorted(
        (file for file in source_folder.glob("split_*_additional.txt")),
        key=lambda f: int(file_pattern.search(f.name).group(1)),
    )

    # Open the merged file in write mode
    with open(merged_file_path, "w", encoding="utf-8") as merged_file:
        for file in additional_files:
            # Read the content of each '_additional' file and write to merged file
            with open(file, "r", encoding="utf-8") as f:
                merged_file.write(f.read())
                merged_file.write(
                    "\n\n"
                )  # Optional: add spacing between contents of each file

    print(f"All '_additional' files have been merged into {merged_file_path}")


def process_catalog_overview(folder_path):
    """
    Extracts the catalog overview with BAML from a text file and saves it as a JSON file.
    Args:
        folder_path (str): The path to the folder containing the input text file.
    """

    input_path = os.path.join(folder_path, "merged_additional.txt")
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

    module_list = client.b.ExtractModulesList(text)

    catalog_json = module_list.model_dump_json()

    with open(output_path, "w") as json_file:
        json_file.write(catalog_json)

def parse_module_catalog(path):
    with open(path, 'r') as json_file:
        catalog_json = json_file.read()

        return ModuleList.model_validate_json(catalog_json)
    
def parse_overview(path):
    with open(path, 'r') as json_file:
        catalog_json = json_file.read()

        return StudyProgrammOverview.model_validate_json(catalog_json)
