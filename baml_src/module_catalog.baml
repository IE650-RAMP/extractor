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

class ModuleCataloge {
  studyProgram StudyProgram @description("The study program, this module cataloge is about.")
  // modules Module[] @description("A list of all modules in the module cataloge")
  studyAreas StudyArea[] @description("A list of the study areas in this module cataloge")
}

class StudyProgram {
  name string @description("The name of the study program, e.g., 'MMDS'")
  hasDegree Degree[] @description("Degrees associated with this study program")
} // could directly include study program name and degre in ModuleCataloge

class StudyArea {
  name string @description("The name of the study area, e.g., 'Data Science Fundamentals'")
  requiredEcts int[] @description("The number of ects that has to be completed in this study area. Either exact number or lower and upper bound of a range.")
  modules Module[] @description("A list of all modules in this study area")

  // isPartOfStudyProgram StudyProgram[] @description("List of study programs that include this study area")
}

class Module {
  name string @description("The name of the module in snake case")
  id string @description("The ID of the module typically a letter-number combination e.g. IE100")
  ects int @description("The European Credit Transfer and Accumulation System (ECTS) points for the module")
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
  
  prerequisiteModules string[] @description("A list of module IDs (typically a letter-number combination such as IE100) that are a explicitly stated as required prerequisite for this module")
  additionalPrerequisite string? @description("Any additional prerequisites for the module")
  furtherModules string[] @description("A list of module names that are recommended subsequent modules")
  // isFollowupOfModule string[] @description("List of modules that this module follows up on")
  // isMandatoryPrerequisiteOf string[] @description("List of modules that require this module as a mandatory prerequisite")
  // isRecommendedPrerequisiteOf string[] @description("List of modules for which this module is a recommended prerequisite")
  
  // isPartOfStudyArea StudyArea[] @description("List of study areas this module is a part of")
}

class Person {
  name string @description("The name of a person, e.g., a lecturer or person in charge of a module")
  title string? @description("The title of a person, e.g., Prof. Dr.")
  isPerson bool @description("Indecation if this is a person (true) or different entity (false)")
  // isChairOf string[] @description("List of modules or programs that this person chairs")
}



function ExtractModuleCatalog(module_catalog: string) -> ModuleCataloge {
  client "openai/gpt-4o-mini" 
  prompt #"
    Extract the content from this university module cataloge:
    {{ module_catalog }}

    {{ ctx.output_format }}
  "#
}

// Test the function with a sample resume. Open the VSCode playground to run this.
test extract_module_catalog {
  functions [ExtractModuleCatalog]
  args {
    module_catalog #"
     
    "#
  }
}
