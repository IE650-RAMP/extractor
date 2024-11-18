enum Semester {
  FFS @description("Fall/Spring semester")
  HWS @description("Winter semester")
}

enum AssessmentForm {
  WRITTEN @description("Assessment is a written exam")
  ORAL @description("Assessment is an oral exam")
  ASSIGNEMNT @description("Assessment is an assignemnt")
  REPORT @description("Assessment is a written report")
  PRESENTATION @description("Assessment is a presentation")
  PRACTICAL @description("Assessment includes practical examination components")
}

enum Degree {
    BACHELOR_OF_ARTS @description("Bachelor of Arts")
    BACHELOR_OF_SCIENCE @description("Bachelor of Science")
    BACHELOR_OF_EDUCATION @description("Bachelor of Education")
    BACHELOR_OF_LAWS @description("Bachelor of Laws")
    MASTER_OF_SCIENCE @description("Master of Science")
    MASTER_OF_ARTS @description("Master of Arts")
    MASTER_OF_COMPARATIVE_BUSINESS_LAW @description("Master of Comparative Business Law")
    MASTER_OF_LAWS @description("Master of Laws")
    MASTER_OF_EDUCATION @description("Master of Education")
}

class ModuleCatalog {
  studyProgram StudyProgram @description("The study program, this module cataloge is about.")
  studyAreas StudyArea[] @description("A list of the study areas in this module cataloge")
}

class StudyProgram {
  name string @description("The name of the study program, e.g., 'MMDS'")
  hasDegree Degree[] @description("Degrees associated with this study program")
} // could directly include study program name and degre in ModuleCatalog

class StudyArea {
  name string @description("The name of the study area, e.g., 'Data Science Fundamentals'")
  requiredEcts int[] @description("The number of ects that has to be completed in this study area. Either exact number or lower and upper bound of a range.")
  modules Module[] @description("A list of all modules in this study area")
}

// ----

class StudyProgrammOverview {
  name string @description("The name of the study program, e.g., 'MMDS'")
  hasDegree Degree[] @description("Degrees associated with this study program")
  studyArea StudyAreaOverview[] @description("The different areas of study within the study program")

}

class StudyAreaOverview {
  name string @description("The name of the study area, e.g., 'Data Science Fundamentals'")
  requiredEcts int[] @description("The number of ects that has to be completed in this study area. Either exact number or lower and upper bound of a range.")
  modules ModuleOverview[] @description("A list of all modules (with their name and id) in this study area")
}

class ModuleOverview {
  name string @description("The name of the module e.g. machine_learning (in snake case)")
  id string @description("The ID of the module typically a letter-number combination e.g. IE_100 (in snake case)")
}

class ModuleList {
  modules Module[] 
}

class Module {
  name string @description("The name of the module (in snake case)")
  id string @description("The ID of the module typically a letter-number combination e.g. IE_100 (in snake case)")
  ects int @description("The number of ECTS points for the module")
  workloadInPerson int @description("The in-person workload hours for the module")
  workloadSelfStudy int @description("The self-study workload hours for the module")
  offeredIn Semester[] @description("The semester when the module is offered")
  recommendedSemester int[] @description("Recommended semesters to take this module")
  recommendedLiterature string[] @description("List of recommended literature for the module")
  
  hasLecturer Person[] @description("The persons that gives the lecture for this module")
  hasPersonInCharge Person[] @description("The person that is in charge of the module")
  
  assessmentForms AssessmentForm[] @description("The forms of assesment for this moudle")
  examinationDistribution string? @description("Distribution method for examinations in this module (e.g. 80/20, 100)")
  examinationDuration int? @description("Duration of the examination in minutes")
  
  requiredPrerequisiteModules string[] @description("A list of module IDs (typically a letter-number combination such as IE_100) that are a explicitly stated as required prerequisite for this module")
  optionalPrerequisiteModules string[] @description("A list of module IDs (typically a letter-number combination such as IE_100) that are a optional additional prerequisite for this module")
  additionalPrerequisite string? @description("Any additional prerequisites for the module")
  furtherModules string[] @description("A list of module names that are recommended subsequent modules")
  // isFollowupOfModule string[] @description("List of modules that this module follows up on")
  // isMandatoryPrerequisiteOf string[] @description("List of modules that require this module as a mandatory prerequisite")
  // isRecommendedPrerequisiteOf string[] @description("List of modules for which this module is a recommended prerequisite")
  
  // isPartOfStudyArea StudyArea[] @description("List of study areas this module is a part of")
}

class Person {
  name string @description("The name of a person without their title. If no name is given use a short description and set hasName to false")
  title string? @description("The title of a person, e.g., Prof. Dr.")
  hasName bool @description("Indecation if this is a person with a name (true) or different entity (false)")
}


// Extract all information from the entire module cataloge
function ExtractModuleCatalog(module_catalog: string) -> ModuleCatalog {
  // Extracts the entire module in one go
  client "openai/gpt-4o-mini" 
  // client "anthropic/claude-3-haiku-20240307"
  prompt #"
    Extract the content from this university module cataloge. Make sure to extract all of the listed modules and do not stop after the first few ones.
    
    This is the module cataloge:
    {{ module_catalog }}

    Consider this information for the ouput format:
    Extract all modules!

    {{ ctx.output_format }}
  "#
}

test extract_module_catalog {
  functions [ExtractModuleCatalog]
  args {
    module_catalog #"
    
    "#
  }
}

function ExtractModulesList(module_catalog: string) -> ModuleList {
  client "openai/gpt-4o-mini"
  prompt #"
    Extract the modules from this university module cataloge in the defined schema.
    {{ module_catalog }}

    {{ ctx.output_format }}
  "#
}

test extract_modules {
  functions [ExtractModulesList]
  args {
    module_catalog #"
    
    "#
  }
}


function ExtractStudyProgrammOverview(module_catalog: string) -> StudyProgrammOverview {
  client "openai/gpt-4o-mini"
  prompt #"
    Extract the information from this university module cataloge according to the defined schema.
    {{ module_catalog }}

    {{ ctx.output_format }}
  "#
}

test extract_program_overview {
  functions [ExtractStudyProgrammOverview]
  args {
    module_catalog #"

    "#
  }
}

