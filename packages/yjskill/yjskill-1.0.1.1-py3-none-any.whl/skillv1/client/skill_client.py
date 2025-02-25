# -*- coding: utf-8 -*-
from baidubce.http import http_methods
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from .skill_api_skill import GetSkillRequest


class SkillClient(BceInternalClient):
    """
    A client class for interacting with the skill service. 
    """

    def get_skill(
            self,
            req: GetSkillRequest):
        """
        Get a skill.

        Args:
            workspace_id (str): 工作区 id，例如："ws01"
            skill_name (str): 技能系统名称，例如："skill01"
            version (str): 技能版本号，例如："1"
        Returns:
             HTTP request response
        """

        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/" + req.workspace_id + "/skills/" + req.local_name, encoding="utf-8"
            ),
            params=req.model_dump(by_alias=True),
        )
