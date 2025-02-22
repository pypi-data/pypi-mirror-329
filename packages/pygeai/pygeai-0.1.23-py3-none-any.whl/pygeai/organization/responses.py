from typing import Optional

from pydantic.main import BaseModel

from pygeai.core.base.models import Assistant, Project, Organization, ProjectSearchProfile, ProjectToken, \
    UsageLimit, ProjectItem


class AssistantListResponse(BaseModel):
    assistants: list[Assistant]


class ProjectListResponse(BaseModel):
    projects: list[Project]


class ProjectDataResponse(BaseModel):
    project: Project


class ProjectTokensResponse(BaseModel):
    tokens: list[ProjectToken]


class ProjectItemListResponse(BaseModel):
    items: list[ProjectItem]
