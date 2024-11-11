from baml_client.sync_client import b
from baml_client.types import ModuleCataloge

from baml_client import reset_baml_env_vars
import os
import dotenv

dotenv.load_dotenv()
reset_baml_env_vars(dict(os.environ))
# print(dict(os.environ))


def run_baml(input: str) -> ModuleCataloge:
    # BAML's internal parser guarantees ExtractResume
    # to be always return a Resume type
    response = b.ExtractModuleCatalog(input)
    return response


def run_baml_stream(input: str) -> ModuleCataloge:
    stream = b.stream.ExtractModuleCatalog(input)
    for msg in stream:
        print(msg)  # This will be a PartialResume type

    # This will be a Resume type
    final = stream.get_final_response()

    return final


with open("./baml_tests/mmds_newest_unstructured.txt", "r") as file:
    text = file.read()
    # if len(text) > 10000:
    #     text = text[:10000]

catalog = run_baml(text)

print("\n\n============")
for i in range(len(catalog.studyAreas)):
    print(catalog.studyAreas[i].name)
    print(len(catalog.studyAreas[i].modules))
