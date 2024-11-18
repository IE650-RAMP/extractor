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
import baml_py
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional, Union, Literal

from . import types
from .types import Checked, Check

###############################################################################
#
#  These types are used for streaming, for when an instance of a type
#  is still being built up and any of its fields is not yet fully available.
#
###############################################################################


class Module(BaseModel):
    
    
    name: Optional[str] = None
    id: Optional[str] = None
    ects: Optional[int] = None
    workloadInPerson: Optional[int] = None
    workloadSelfStudy: Optional[int] = None
    offeredIn: List[Optional[types.Semester]]
    recommendedSemester: List[Optional[int]]
    recommendedLiterature: List[Optional[str]]
    hasLecturer: List["Person"]
    hasPersonInCharge: List["Person"]
    assessmentForms: List[Optional[types.AssessmentForm]]
    examinationDistribution: Optional[str] = None
    examinationDuration: Optional[int] = None
    requiredPrerequisiteModules: List[Optional[str]]
    optionalPrerequisiteModules: List[Optional[str]]
    additionalPrerequisite: Optional[str] = None
    furtherModules: List[Optional[str]]

class ModuleCatalog(BaseModel):
    
    
    studyProgram: Optional["StudyProgram"] = None
    studyAreas: List["StudyArea"]

class ModuleList(BaseModel):
    
    
    modules: List["Module"]

class ModuleOverview(BaseModel):
    
    
    name: Optional[str] = None
    id: Optional[str] = None

class Person(BaseModel):
    
    
    name: Optional[str] = None
    title: Optional[str] = None
    hasName: Optional[bool] = None

class StudyArea(BaseModel):
    
    
    name: Optional[str] = None
    requiredEcts: List[Optional[int]]
    modules: List["Module"]

class StudyAreaOverview(BaseModel):
    
    
    name: Optional[str] = None
    requiredEcts: List[Optional[int]]
    modules: List["ModuleOverview"]

class StudyProgram(BaseModel):
    
    
    name: Optional[str] = None
    hasDegree: List[Optional[types.Degree]]

class StudyProgrammOverview(BaseModel):
    
    
    name: Optional[str] = None
    hasDegree: List[Optional[types.Degree]]
    studyArea: List["StudyAreaOverview"]
