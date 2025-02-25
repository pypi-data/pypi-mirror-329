# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DataSource(BaseModel):
    """
    数据源
    """

    name: str = Field(alias="name")
    local_name: str = Field(alias="localName")
    display_name: str = Field(alias="displayName")
    description: str = Field(alias="description")
    workspace_id: str = Field(alias="workspaceID")

    kind: str = Field(alias="kind")
    uri: Optional[str] = Field(alias="URI", default=None)
    ip: Optional[str] = Field(alias="IP", default=None)

    from_kind: str = Field(alias="fromKind")
    from_id: str = Field(alias="fromID")

    config: Optional[dict] = Field(alias="config", default=None)

    status: str = Field(alias="status")
    enabled: bool = Field(alias="enabled")

    skills: Optional[list[str]] = Field(alias="skills", default=None)

    org_id: str = Field(alias="orgID")
    user_id: str = Field(alias="userID")
    dept_id: Optional[str] = Field(alias="deptID", default=None)

    create_at: Optional[datetime] = Field(default=None, alias="createAt")
    update_at: Optional[datetime] = Field(default=None, alias="updateAt")
