###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

file_map = {
    
    "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n\nclient<llm> CustomGPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> CustomGPT4oMini {\n  provider openai\n  retry_policy Exponential\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> CustomSonnet {\n  provider anthropic\n  options {\n    model \"claude-3-5-sonnet-20241022\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\n\nclient<llm> CustomHaiku {\n  provider anthropic\n  retry_policy Constant\n  options {\n    model \"claude-3-haiku-20240307\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/round-robin\nclient<llm> CustomFast {\n  provider round-robin\n  options {\n    // This will alternate between the two clients\n    strategy [CustomGPT4oMini, CustomHaiku]\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/fallback\nclient<llm> OpenaiFallback {\n  provider fallback\n  options {\n    // This will try the clients in order until one succeeds\n    strategy [CustomGPT4oMini, CustomGPT4oMini]\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/retry\nretry_policy Constant {\n  max_retries 3\n  // Strategy is optional\n  strategy {\n    type constant_delay\n    delay_ms 200\n  }\n}\n\nretry_policy Exponential {\n  max_retries 2\n  // Strategy is optional\n  strategy {\n    type exponential_backoff\n    delay_ms 300\n    mutliplier 1.5\n    max_delay_ms 10000\n  }\n}",
    "generators.baml": "// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\", \"rest/openapi\"\n    output_type \"python/pydantic\"\n\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../\"\n\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.67.0\"\n\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    default_client_mode sync\n}\n",
    "module_catalog.baml": "enum Semester {\n  FFS @description(\"Fall/Spring semester\")\n  HWS @description(\"Winter semester\")\n}\n\nenum AssessmentForm {\n  WRITTEN @description(\"Assessment is a written exam\")\n  ORAL @description(\"Assessment is an oral exam\")\n  ASSIGNEMNT @description(\"Assessment is an assignemnt\")\n  REPORT @description(\"Assessment is a written report\")\n  PRESENTATION @description(\"Assessment is a presentation\")\n  PRACTICAL @description(\"Assessment includes practical examination components\")\n}\n\nenum Degree {\n    BACHELOR_OF_ARTS @description(\"Bachelor of Arts\")\n    BACHELOR_OF_SCIENCE @description(\"Bachelor of Science\")\n    BACHELOR_OF_EDUCATION @description(\"Bachelor of Education\")\n    BACHELOR_OF_LAWS @description(\"Bachelor of Laws\")\n    MASTER_OF_SCIENCE @description(\"Master of Science\")\n    MASTER_OF_ARTS @description(\"Master of Arts\")\n    MASTER_OF_COMPARATIVE_BUSINESS_LAW @description(\"Master of Comparative Business Law\")\n    MASTER_OF_LAWS @description(\"Master of Laws\")\n    MASTER_OF_EDUCATION @description(\"Master of Education\")\n}\n\nclass ModuleCatalog {\n  studyProgram StudyProgram @description(\"The study program, this module cataloge is about.\")\n  studyAreas StudyArea[] @description(\"A list of the study areas in this module cataloge\")\n}\n\nclass StudyProgram {\n  name string @description(\"The name of the study program, e.g., 'MMDS'\")\n  hasDegree Degree[] @description(\"Degrees associated with this study program\")\n} // could directly include study program name and degre in ModuleCatalog\n\nclass StudyArea {\n  name string @description(\"The name of the study area, e.g., 'Data Science Fundamentals'\")\n  requiredEcts int[] @description(\"The number of ects that has to be completed in this study area. Either exact number or lower and upper bound of a range.\")\n  modules Module[] @description(\"A list of all modules in this study area\")\n}\n\n// ----\n\nclass StudyProgrammOverview {\n  name string @description(\"The name of the study program, e.g., 'MMDS'\")\n  hasDegree Degree[] @description(\"Degrees associated with this study program\")\n  studyArea StudyAreaOverview[] @description(\"The different areas of study within the study program\")\n\n}\n\nclass StudyAreaOverview {\n  name string @description(\"The name of the study area, e.g., 'Data Science Fundamentals'\")\n  requiredEcts int[] @description(\"The number of ects that has to be completed in this study area. Either exact number or lower and upper bound of a range.\")\n  modules ModuleOverview[] @description(\"A list of all modules (with their name and id) in this study area\")\n}\n\nclass ModuleOverview {\n  name string @description(\"The name of the module e.g. machine_learning (in snake case)\")\n  id string @description(\"The ID of the module typically a letter-number combination e.g. IE_100 (in snake case)\")\n}\n\nclass ModuleList {\n  modules Module[] \n}\n\nclass Module {\n  name string @description(\"The name of the module (in snake case)\")\n  id string @description(\"The ID of the module typically a letter-number combination e.g. IE_100 (in snake case)\")\n  ects int @description(\"The number of ECTS points for the module\")\n  workloadInPerson int @description(\"The in-person workload hours for the module\")\n  workloadSelfStudy int @description(\"The self-study workload hours for the module\")\n  offeredIn Semester[] @description(\"The semester when the module is offered\")\n  recommendedSemester int[] @description(\"Recommended semesters to take this module\")\n  recommendedLiterature string[] @description(\"List of recommended literature for the module\")\n  \n  hasLecturer Person[] @description(\"The persons that gives the lecture for this module\")\n  hasPersonInCharge Person[] @description(\"The person that is in charge of the module\")\n  \n  assessmentForms AssessmentForm[] @description(\"The forms of assesment for this moudle\")\n  examinationDistribution string? @description(\"Distribution method for examinations in this module (e.g. 80/20, 100)\")\n  examinationDuration int? @description(\"Duration of the examination in minutes\")\n  \n  requiredPrerequisiteModules string[] @description(\"A list of module IDs (typically a letter-number combination such as IE_100) that are a explicitly stated as required prerequisite for this module\")\n  optionalPrerequisiteModules string[] @description(\"A list of module IDs (typically a letter-number combination such as IE_100) that are a optional additional prerequisite for this module\")\n  additionalPrerequisite string? @description(\"Any additional prerequisites for the module\")\n  furtherModules string[] @description(\"A list of module names that are recommended subsequent modules\")\n  // isFollowupOfModule string[] @description(\"List of modules that this module follows up on\")\n  // isMandatoryPrerequisiteOf string[] @description(\"List of modules that require this module as a mandatory prerequisite\")\n  // isRecommendedPrerequisiteOf string[] @description(\"List of modules for which this module is a recommended prerequisite\")\n  \n  // isPartOfStudyArea StudyArea[] @description(\"List of study areas this module is a part of\")\n}\n\nclass Person {\n  name string @description(\"The name of a person without their title. If no name is given use a short description and set hasName to false\")\n  title string? @description(\"The title of a person, e.g., Prof. Dr.\")\n  hasName bool @description(\"Indecation if this is a person with a name (true) or different entity (false)\")\n}\n\n\n// Extract all information from the entire module cataloge\nfunction ExtractModuleCatalog(module_catalog: string) -> ModuleCatalog {\n  // Extracts the entire module in one go\n  client \"openai/gpt-4o-mini\" \n  // client \"anthropic/claude-3-haiku-20240307\"\n  prompt #\"\n    Extract the content from this university module cataloge. Make sure to extract all of the listed modules and do not stop after the first few ones.\n    \n    This is the module cataloge:\n    {{ module_catalog }}\n\n    Consider this information for the ouput format:\n    Extract all modules!\n\n    {{ ctx.output_format }}\n  \"#\n}\n\ntest extract_module_catalog {\n  functions [ExtractModuleCatalog]\n  args {\n    module_catalog #\"\n    \n    \"#\n  }\n}\n\nfunction ExtractModulesList(module_catalog: string) -> ModuleList {\n  client \"openai/gpt-4o-mini\"\n  prompt #\"\n    Extract the modules from this university module cataloge in the defined schema.\n    {{ module_catalog }}\n\n    {{ ctx.output_format }}\n  \"#\n}\n\ntest extract_modules {\n  functions [ExtractModulesList]\n  args {\n    module_catalog #\"\n    \n    \"#\n  }\n}\n\n\nfunction ExtractStudyProgrammOverview(module_catalog: string) -> StudyProgrammOverview {\n  client \"openai/gpt-4o-mini\"\n  prompt #\"\n    Extract the information from this university module cataloge according to the defined schema.\n    {{ module_catalog }}\n\n    {{ ctx.output_format }}\n  \"#\n}\n\ntest extract_program_overview {\n  functions [ExtractStudyProgrammOverview]\n  args {\n    module_catalog #\"\n\n    \"#\n  }\n}\n\n",
}

def get_baml_files():
    return file_map