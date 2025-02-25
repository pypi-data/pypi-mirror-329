# -*- coding: utf-8 -*-
import re
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from windmillartifactv1.client import artifact_api_artifact as artifact_api

from . import skill_api_datasource as datasource_api

skill_name_regex = re.compile(
    r"^workspaces/(?P<workspace_id>.+?)/skills/(?P<local_name>.+?)$"
)


class Skill(BaseModel):
    """
    Skill model.
    """

    name: str = Field(alias="name")
    local_name: str = Field(alias="localName")
    display_name: str = Field(alias="displayName")
    description: str = Field(alias="description")
    workspace_id: str = Field(alias="workspaceID")

    kind: str = Field(alias="kind")
    create_kind: str = Field(alias="createKind")
    from_kind: str = Field(alias="fromKind")

    tags: Optional[dict] = Field(default=None, alias="tags")
    image_uri: Optional[str] = Field(default=None, alias="imageURI")
    accelerators: Optional[list] = Field(default=None, alias="accelerators")
    model_type: Optional[str] = Field(default=None, alias="modelType")
    status: str = Field(alias="status")
    data_sources: Optional[datasource_api.DataSource] = Field(
        default=None, alias="dataSources")

    graph: Optional[dict] = Field(default=None, alias="graph")
    debug: Optional[dict] = Field(default=None, alias="debug")

    artifact_count: int = Field(alias="artifactCount")
    released_version: int = Field(alias="releasedVersion")

    org_id: str = Field(alias="orgID")
    user_id: str = Field(alias="userID")

    default_level: int = Field(alias="defaultLevel")
    alarm_configs: Optional[list] = Field(default=None, alias="alarmConfigs")

    create_at: Optional[datetime] = Field(default=None, alias="createAt")
    update_at: Optional[datetime] = Field(default=None, alias="updateAt")


class SkillName(BaseModel):
    """
    Skill name, e.g. workspaces/:ws/skills/:localName
    """

    workspace_id: str
    local_name: str


def parse_skill_name(name: str) -> Optional[SkillName]:
    """
    Parse skill name to SkillName object.

    Args:
        name: str, skill name, e.g. workspaces/:ws/skills/:localName
    Returns:
        SkillName, 解析成功返回SkillName对象，否则返回None
    """

    match = skill_name_regex.match(name)
    if match:
        return SkillName(**match.groupdict())
    return None


class MergeRule(BaseModel):
    """ 
    Merge rule model.
    """

    default_level: int = Field(alias="defaultLevel")
    dimension: str = Field(alias="dimension")
    period: int = Field(alias="period")


class AlarmConfig(BaseModel):
    """
    Alarm config model.
    """
    app_name: str = Field(alias="appName")
    enabled: bool = Field(alias="enabled", default=None)
    merge_rule: MergeRule = Field(alias="mergeRule", default=None)


class GetSkillRequest(BaseModel):
    """
    Request for get skill.
    """

    workspace_id: str = Field(alias="workspaceID")
    local_name: str = Field(alias="localName")
    version: str = Field(alias="version")


class CreateSkillRequest(BaseModel):
    """
    Request for create skill.
    """

    workspace_id: str = Field(alias="workspaceID")
    local_name: str = Field(alias="localName")
    display_name: str = Field(alias="displayName")
    description: Optional[str] = Field(default=None, alias="description")
    kind: str = Field(alias="kind")
    crerate_kind: str = Field(alias="createKind")
    from_kind: str = Field(alias="fromKind")
    tags: Optional[dict] = Field(default=None, alias="tags")
    graph: Optional[dict] = Field(default=None, alias="graph")
    artifact: Optional[dict] = Field(default=None, alias="artifact")
    image_uri: Optional[str] = Field(default=None, alias="imageURI")
    default_level: int = Field(default=4, alias="defaultLevel")
    alarm_configs: Optional[list] = Field(default=None, alias="alarmConfigs")


class UpdateSkillRequest(BaseModel):
    """
    Request for update skill.
    """

    workspace_id: str = Field(alias="workspaceID")
    local_name: str = Field(alias="localName")
    display_name: Optional[str] = Field(default=None, alias="displayName")
    description: Optional[str] = Field(default=None, alias="description")
    tags: Optional[dict] = Field(default=None, alias="tags")
    released_version: Optional[int] = Field(
        default=None, alias="releasedVersion")
    image_uri: Optional[str] = Field(default=None, alias="imageURI")
