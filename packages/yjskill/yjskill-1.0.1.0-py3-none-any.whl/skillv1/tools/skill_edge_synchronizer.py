import traceback
import os
import json

import bcelogger
from devicev1.client import device_client, device_api

from . import skill_synchronizer
from ..client import skill_api_skill as skill_api


class SkillEdgeSynchronizer(skill_synchronizer.SkillSynchronizer):
    """
    技能同步到盒子
    """

    device_accelerator_config = {}
    device_hub_name = "default"

    device_cli: device_client.DeviceClient

    def __init__(self, config: skill_synchronizer.SkillSynchronizerConfig):
        """
        初始化技能同步到盒子
        """
        super().__init__(config=config)
        self.__setup()

    def __setup(self):
        """
        设置技能同步到盒子的相关参数
        """

        self.device_cli = device_client.DeviceClient(endpoint=self.config.windmill_endpoint,
                                                     context={"OrgID": self.config.org_id,
                                                              "UserID": self.config.user_id})
        ok, err, resp = self.__get_device_configuration()
        if not ok:
            raise RuntimeError(f"Get Device Configuration Failed: {err}")
        self.device_accelerator_config = resp

    def __check_edge(self,
                     edge: dict):
        """
        检查技能是否能下发

        Args:
            dest (dict): 下发的目的地，例如：盒子信息
        Returns:
            bool: 是否匹配
            str: 错误信息
        """

        if edge["status"] == "Disconnected":
            return False, "设备已断开连接"

        # TODO 下发中，认为失败 (联调阶段先不校验)
        if edge["status"] == "Processing":
            return False, "设备正在下发中"

        if edge["kind"] not in self.device_accelerator_config:
            return False, "未找到设备的硬件信息"

        if self.skill.graph is None:
            bcelogger.warning("CheckEdge Skill Graph is None")
            return False, "未找到技能的硬件信息"

        artifact = self.skill.graph.get('artifact', None)
        if artifact is None:
            bcelogger.warning("CheckEdge Skill Artifact is None")
            return False, "未找到技能的硬件信息"

        skill_tag = self.skill.graph['artifact'].get('tags', {})

        return skill_synchronizer.check_accelerators(
            skill_accelerator=skill_tag.get("accelerator", ""),
            target_accelelator=self.device_accelerator_config[edge["kind"]])

    def __get_device_configuration(self):
        """
        获取设备配置

        Returns:
            boolean: 是否成功
            str: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
            dict: 设备硬件-显卡对应关系
        """

        workspace_id = self.skill_name.workspace_id
        # 注意，应该用device的workspace_id，而不是skill的workspace_id
        if len(self.config.sync_model_result) > 0:
            device_name = next(iter(self.config.sync_model_result))
            device_name = device_api.parse_device_name(device_name)
            workspace_id = device_name.workspace_id

        req = device_client.GetConfigurationRequest(
            workspace_id=workspace_id,
            device_hub_name="default",
            local_name="default")
        resp = {}
        try:
            resp = self.device_cli.get_configuration(req=req)
            bcelogger.info("GetDeviceConfiguration req=%s, resp=%s", req, resp)
        except Exception as e:
            bcelogger.error("SyncSkillGetDeviceConfiguration get_configuration_req=%s Failed: %s",
                            req.model_dump(by_alias=True),
                            traceback.format_exc())
            return False, {"error": str(e), "reason": "查询设备配置失败"}, resp

        deviceAcceleratorConfig = {}
        if resp is not None and resp.device_configs is not None:
            for item in resp.device_configs:
                deviceAcceleratorConfig[item.kind] = item.gpu
        return True, {}, deviceAcceleratorConfig

    def __update_device_status(self,
                               workspace_id: str,
                               device_hub_name: str,
                               device_name: str,
                               status: str):
        """
        更新设备状态

        Returns:
            bool: 是否成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "创建技能失败"}
        """

        try:
            update_device_req = device_api.UpdateDeviceRequest(
                workspaceID=workspace_id,
                deviceHubName=device_hub_name,
                deviceName=device_name,
                status=status,
            )
            update_device_resp = self.device_cli.update_device(
                request=update_device_req)
            bcelogger.info('UpdateDevice req=%s, resp=%s',
                           update_device_req, update_device_resp)
            return True, {}
        except Exception as e:
            bcelogger.error("UpdateDeviceFailed device=%s Failed: %s",
                            device_name, traceback.format_exc())
            return False, {"error": str(e), "reason": f'更新设备状态为{status}失败'}

    def __release_skill(self,
                        skill: skill_api.Skill,
                        target: dict):
        """
        技能上线

        Args:
            released_version: int, 要上线的技能版本号
            extra_data: dict,额外参数
        Returns:
            bool: 是否成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
        """

        # 技能下发成功后，技能热更新
        artifact = None
        if skill.graph is not None:
            artifact = skill.graph.get('artifact')
        artifact_version = None
        if artifact is not None:
            artifact_version = artifact.get('version')
        if artifact_version is None:
            bcelogger.error("ReleaseSkillFailed artifact_version is none")
            return False, {"error": "技能版本号为空", "reason": "技能上线失败"}

        released_version = artifact_version

        device_hub_name = target.get("deviceHubName")
        device_name = target.get("localName")
        target_workspace = target.get("workspaceID")

        workspace_id = skill.workspaceID
        local_name = skill.localName
        update_skill_request = skill_api.UpdateSkillRequest(
            workspaceID=workspace_id,
            localName=local_name,
            releasedVersion=released_version)
        try:
            # 通过BIE调用盒子的create skill HTTP接口
            skill_url = f'api/vistudio/v1/workspaces/{workspace_id}/skills/{local_name}/put'
            invoke_method_req = device_api.InvokeMethodHTTPRequest(
                workspaceID=target_workspace,
                deviceHubName=device_hub_name,
                deviceName=device_name,
                uri=skill_url,
                body=update_skill_request.model_dump(by_alias=True),
            )
            skill_resp = self.device_cli.invoke_method_http(
                request=invoke_method_req)
            bcelogger.info('ReleaseSkill req=%s, resp=%s',
                           invoke_method_req, skill_resp)
            if hasattr(skill_resp, 'success') and skill_resp.success == False:
                raise Exception(skill_resp.message)
            return True, {}
        except Exception as e:
            bcelogger.error("ReleaseSkillFailed device=%s Failed: %s",
                            device_name, traceback.format_exc())
            return False, {"error": str(e), "reason": "技能上线失败"}

    def list_targets(self):
        """
        获取下发目的地列表

        Returns:
            bool: 是否成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
            list[dict]: 目标列表
        """

        device_local_name = []
        # 要使用device_name中的workspace，而不是技能的workspace，因为有公共技能
        # TODO: 此处仅考虑了多个device都是同一个workspace的情况
        workspace_id = ""
        for name in self.config.target_names:
            device_name = device_api.parse_device_name(name)
            device_local_name.append(device_name.local_name)
            workspace_id = device_name.workspace_id

        list_device_req = device_api.ListDeviceRequest(
            workspaceID=workspace_id,
            deviceHubName="default",
            pageSize=200,
            pageNo=1,
            selects=device_local_name)
        try:
            devices = []
            resp = self.device_cli.list_device(req=list_device_req)
            if resp is not None and resp.result is not None:
                devices.extend(resp.result)
            bcelogger.info(
                "ListDevices list_device_req=%s, resp len=%d", list_device_req, len(devices))
            return True, {}, devices
        except Exception as e:
            bcelogger.error("SyncSkillListDevice list_device_req=%s Failed: %s",
                            list_device_req.model_dump(by_alias=True),
                            traceback.format_exc())
            return False, {"error": str(e), "reason": "查询设备失败"}, []

    def create_skill(self,
                     req: skill_api.CreateSkillRequest,
                     target: dict):
        """
        创建技能

        Args:
            req: skill_api.CreateSkillRequest, 技能创建请求参数
            target: dict, 下发目标
        Returns:
            bool: 是否成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "创建技能失败"}
            skill: 创建的技能的信息
        """

        device_name = target.get("localName")
        target_workspace = target.get("workspaceID")
        try:
            # 通过BIE调用盒子的create skill HTTP接口
            device_url = f'v1/workspaces/{req.workspace_id}/skills'
            invoke_method_req = device_api.InvokeMethodHTTPRequest(
                workspaceID=target_workspace,
                deviceHubName=self.device_hub_name,
                deviceName=device_name,
                uri=device_url,
                body=req.model_dump(by_alias=True),
            )
            skill_resp = self.device_cli.invoke_method_http(
                request=invoke_method_req)
            bcelogger.info('CreateSkill req=%s, resp=%s',
                           invoke_method_req, skill_resp)
            return True, {}, skill_resp
        except Exception as e:
            bcelogger.error("SyncSkillCreateSkill device=%s Failed: %s",
                            device_name, traceback.format_exc())
            return False, {"error": str(e), "reason": "创建技能失败"}, {}

    def preprocess_sync_skill(self, target: dict):
        """
        sync_skill的前处理

        Args:
            target: dict, 下发目标
        Returns:
            bool: 是否成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
            dict: {"create_skill_request": skill_api.CreateSkillRequest}
        """

        ok, err_msg = self.__check_edge(edge=target)
        if not ok:
            bcelogger.error("PreSyncSkillFailed: %s", err_msg)
            return False, {"error": err_msg, "reason": err_msg}, {}

        # 盒子状态改为下发中
        ok, err = self.__update_device_status(workspace_id=target["workspaceID"],
                                              device_hub_name=target["deviceHubName"],
                                              device_name=target["localName"],
                                              status="Processing")
        if not ok:
            bcelogger.error("PreSyncSkillFailed: %s", err_msg)
            return False, err, {}

        skill = self.skill
        target_workspace = target.get("workspaceID", None)
        model_result = self.config.sync_model_result.get(target["name"])
        target_model_name = model_result.get("artifactName")
        old_model_name = skill_synchronizer.get_model_name(self.skill.graph)
        bcelogger.debug(
            "PreSyncSkill old_model_name: %s, target_model_name: %s",
            old_model_name, target_model_name)

        skill_target_workspace = skill.workspaceID

        replace = {}
        if skill.workspaceID != "public":
            replace = {skill.workspaceID: target_workspace}
            skill_target_workspace = target_workspace
        if old_model_name is not None and old_model_name != target_model_name:
            replace[old_model_name] = target_model_name
        # 技能下发
        # 修改graph中的workspaceID
        graph = skill_synchronizer.build_skill_graph(
            origin_graph=skill.graph,
            replace=replace)
        bcelogger.debug("PreSyncSkill build_skill_graph: %s",
                        json.dumps(graph, ensure_ascii=False))

        create_skill_req = skill_api.CreateSkillRequest(
            workspaceID=skill_target_workspace,
            localName=skill.localName,
            displayName=skill.displayName,
            description=skill.description,
            kind=skill.kind,
            fromKind=self.config.skill_from_kind,
            createKind=self.config.skill_create_kind,
            tags=skill.tags,
            graph=graph,
            artifact=skill.graph.get('artifact'),
            imageURI=skill.imageURI,
            defaultLevel=skill.defaultLevel,
            alarmConfigs=skill.alarmConfigs)

        result = {}
        result["create_skill_request"] = create_skill_req
        extra_data = {}
        extra_data["device_name"] = target.get("localName")
        result["extra_data"] = extra_data
        bcelogger.info("PreSyncSkill result: %s", result)
        return True, {}, result

    def postprocess_sync_skill(self, skill: skill_api.Skill, target: dict):
        """
        sync_skill的后处理

        Args:
            skill: skill_api.Skill, 创建后的技能信息
            target: dict, 下发目标
        Returns:
            bool: 是否成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
        """

        # 盒子状态恢复
        self.__update_device_status(workspace_id=target["workspaceID"],
                                    device_hub_name=target["deviceHubName"],
                                    device_name=target["localName"],
                                    status="Connected")

        if skill is None:
            bcelogger.warning(
                "PostSyncSkill, skill is None, maybe create skill failed")
            return True, {}

        # 技能下发成功后，技能热更新
        return self.__release_skill(skill=skill,
                                    target=target)

    def sync_model(self, target: dict, extra_data: dict):
        """
        下发模型

        Args:
            target: dict, 下发目标
            extra_data: dict, 额外参数
        Returns:
            bool: 是否下发成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
        """

        model_succeed_result = extra_data.get("model_succeed_result", {})
        if target["name"] not in model_succeed_result:
            return False, {"error": "模型下发失败", "reason": "模型下发失败"}

        return True, {}
