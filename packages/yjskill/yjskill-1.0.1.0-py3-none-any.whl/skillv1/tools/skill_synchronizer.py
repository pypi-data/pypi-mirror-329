import traceback
import json
from enum import Enum
from typing import Optional
from abc import ABCMeta, abstractmethod

import bcelogger
from pydantic import BaseModel
from jobv1.client import job_client
from jobv1.client import job_api_job as job_api
from jobv1.client import job_api_event as event_api
from jobv1.client import job_api_metric as metric_api
from jobv1.client import job_api_task as task_api
from windmillartifactv1.client import artifact_api_artifact as artifact_api


from ..client import skill_api_skill as skill_api
from ..client import skill_client


class SyncSkillKind(Enum):
    """
    SyncSkillKind is the kind of the sync skill.
    """

    Edge = "Edge"
    SubCloud = "SubCloud"


class SkillSynchronizerConfig(BaseModel):
    """
    技能同步器配置

    Attributes:
        sync_kind: str, 技能下发类型，Edge:下发到盒子,SubCloud:下发到子平台
        skill_name: str, 技能名称,对应SkillVersionName, e.g. "workspaces/:ws/skills/:localName/versions/:version"
        skill_create_kind: str, 技能创建类型, e.g. "Sync"
        skill_from_kind: str, 技能来源类型, e.g. "Edge"
        vistudio_endpoint: str, 技能服务后端, e.g. "http://ip:port"
        windmill_endpoint: str, windmill服务后端, e.g. "http://ip:port"
        target_names: list[str], 目标设备名称列表,对应DeviceName, e.g. ["workspaces/:ws/devices/:deviceName"]
        org_id: str
        user_id: str
        job_name: str, 技能下发任务名称
        skill_task_name: str, 技能下发子任务名称
        sync_model_succeed_resul: list[str], 模型下发成功结果列表,若模型下发失败则技能下发也失败
    """

    sync_kind: SyncSkillKind

    skill_name: str
    skill_create_kind: str
    skill_from_kind: str
    vistudio_endpoint: str
    windmill_endpoint: str

    target_names: list[str]

    org_id: str
    user_id: str

    job_name: str
    skill_task_name: str
    sync_model_result: dict


class SkillSynchronizer(metaclass=ABCMeta):
    """
    技能同步器
    """

    config: SkillSynchronizerConfig
    skill_name: skill_api.SkillName
    skill_version: str
    skill: skill_api.Skill
    targets: list[dict]  # 下发到的目的地

    __skill_cli: skill_client.SkillClient
    __job_cli: job_client.JobClient

    __skill_succeed_count = 0
    __skill_failed_count = 0
    __job_succeed_count = 0
    __job_failed_count = 0
    __job_metric_display_name = "技能下发"
    __skill_task_metric_display_name = "技能下发子任务"
    __event_reason_format = "{}（{}）{}"  # 中文名（id）成功/失败原因

    def __init__(self, config: SkillSynchronizerConfig):
        """
        initialize the class.
        """

        self.config = config
        artifact_name = artifact_api.parse_artifact_name(
            self.config.skill_name)
        self.skill_version = artifact_name.version
        self.skill_name = skill_api.parse_skill_name(artifact_name.object_name)
        bcelogger.info(
            f"SyncSkillInitialize skill_name={self.skill_name}, skill_version={self.skill_version}")
        self.__setup()

    def __setup(self):
        """
        设置技能同步器
        """

        self.__skill_cli = skill_client.SkillClient(endpoint=self.config.vistudio_endpoint,
                                                    context={"OrgID": self.config.org_id,
                                                             "UserID": self.config.user_id})
        self.__job_cli = job_client.JobClient(endpoint=self.config.windmill_endpoint,
                                              context={"OrgID": self.config.org_id,
                                                       "UserID": self.config.user_id})

    def __get_skill(self):
        """
        获取技能信息

        Returns:
            boolean: 是否成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
        """

        req = skill_api.GetSkillRequest(
            workspaceID=self.skill_name.workspace_id,
            localName=self.skill_name.local_name,
            version=self.skill_version)
        try:
            skill = self.__skill_cli.get_skill(req=req)
            if skill.graph is not None and 'draft' in skill.graph:
                skill.graph['draft'] = {}
            self.skill = skill
            bcelogger.info("GetSkill req=%s, resp=%s", req, self.skill)
            return True, {}
        except Exception as e:
            bcelogger.error("SyncSkillGetSkill %s Failed: %s",
                            self.skill_name.local_name,
                            traceback.format_exc())
            return False, {"error": str(e), "reason": "获取技能失败"}

    def __create_metric(self, local_name: metric_api.MetricLocalName,
                        display_name: str,
                        kind: metric_api.MetricKind,
                        data_type: metric_api.DataType,
                        value: list[str],
                        task_name: Optional[str] = None):
        """
        创建metric
        """

        job_name = job_api.parse_job_name(self.config.job_name)
        req = metric_api.CreateMetricRequest(workspace_id=job_name.workspace_id,
                                             job_name=job_name.local_name,
                                             display_name=display_name,
                                             local_name=local_name,
                                             kind=kind,
                                             data_type=data_type,
                                             value=value)
        if task_name is not None:
            req.task_name = task_name
        try:
            resp = self.__job_cli.create_metric(req)
            bcelogger.debug("CreateMetric req=%s, resp is %s", req, resp)
        except Exception as e:
            bcelogger.error("create_metric create_metric_req= %s, Failed: %s",
                            req.model_dump(by_alias=True),
                            str(e))

    def __create_event(self,
                       kind: event_api.EventKind,
                       reason: str,
                       message: str,
                       task_name: Optional[str] = None):
        """
        创建事件
        """

        job_name = job_api.parse_job_name(self.config.job_name)
        req = event_api.CreateEventRequest(
            workspace_id=job_name.workspace_id,
            job_name=job_name.local_name,
            kind=kind,
            reason=reason[:100],
            message=message[:500])
        if task_name is not None:
            req.task_name = task_name
        try:
            resp = self.__job_cli.create_event(req)
            bcelogger.debug("CreateEvent req=%s, resp=%s", req, resp)
        except Exception as e:
            bcelogger.error("CreateEventFailed req=%s, Failed: %s",
                            req.model_dump(by_alias=True),
                            str(e))

    def __mark_job_failed(self, reason: str, message: str):
        """
        更新job状态为失败
        """

        # job status failed
        self.__create_metric(display_name=self.__job_metric_display_name,
                             local_name=metric_api.MetricLocalName.JobStatus,
                             kind=metric_api.MetricKind.Gauge,
                             data_type=metric_api.DataType.String,
                             value=["Failed"])
        # 失败原因
        self.__create_event(kind=event_api.EventKind.Failed,
                            reason=reason,
                            message=message)

    def __create_skill_failed_metric(self):
        """
        创建技能失败的指标
        """

        self.__create_metric(display_name=self.__skill_task_metric_display_name,
                             local_name=metric_api.MetricLocalName.Failed,
                             task_name=self.config.skill_task_name,
                             kind=metric_api.MetricKind.Counter,
                             data_type=metric_api.DataType.Int,
                             value=[str(self.__skill_failed_count)])

    def __create_skill_succeed_metric(self):
        """
        创建技能成功的指标
        """

        self.__create_metric(display_name=self.__skill_task_metric_display_name,
                             local_name=metric_api.MetricLocalName.Success,
                             task_name=self.config.skill_task_name,
                             kind=metric_api.MetricKind.Counter,
                             data_type=metric_api.DataType.Int,
                             value=[str(self.__skill_succeed_count)])

    def __create_skill_total_metric(self):
        """
        创建技能总数指标
        """

        self.__create_metric(display_name=self.__skill_task_metric_display_name,
                             local_name=metric_api.MetricLocalName.Total,
                             task_name=self.config.skill_task_name,
                             kind=metric_api.MetricKind.Counter,
                             data_type=metric_api.DataType.Int,
                             value=[str(len(self.targets))])

    def __create_job_failed_metric_event(self, message: str, reason: str):
        """
        创建job失败metric和event
        """

        # job metric
        self.__create_metric(display_name=self.__job_metric_display_name,
                             local_name=metric_api.MetricLocalName.Failed,
                             kind=metric_api.MetricKind.Counter,
                             data_type=metric_api.DataType.Int,
                             value=[str(self.__job_failed_count)])

        # job event
        self.__create_event(kind=event_api.EventKind.Failed,
                            reason=reason,
                            message=message)

    def __create_job_succeed_metric_event(self, message: str, reason: str):
        """
        创建job失败metric和event
        """

        # job metric
        self.__create_metric(display_name=self.__job_metric_display_name,
                             local_name=metric_api.MetricLocalName.Success,
                             kind=metric_api.MetricKind.Counter,
                             data_type=metric_api.DataType.Int,
                             value=[str(self.__job_succeed_count)])
        # job event
        self.__create_event(kind=event_api.EventKind.Succeed,
                            reason=reason,
                            message=message)

    def __sync_skill(self, target: dict):
        """
        下发技能
        1. 对接任务中心

        Args:
            req: SyncSkillRequest, 技能下发请求参数
        Returns:
            bool: 是否下发成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
        """

        ok, err, result = self.preprocess_sync_skill(target=target)
        if not ok:
            self.__skill_failed_count += 1
            self.__create_skill_failed_metric()
            return False, err

        create_skill_req = result.get("create_skill_request")
        create_skill_extra_data = result.get("extra_data")
        ok, err, skill_resp = self.create_skill(req=create_skill_req,
                                                target=target)
        if not ok:
            self.__skill_failed_count += 1
            # skill task metric
            self.__create_skill_failed_metric()
            # 继续执行后置处理
            self.postprocess_sync_skill(skill=None, target=target)
            return False, err

        ok, err = self.postprocess_sync_skill(skill=skill_resp, target=target)
        if not ok:
            self.__skill_failed_count += 1
            # skill task metric
            self.__create_skill_failed_metric()
            return False, err

        self.__skill_succeed_count += 1
        # 技能下发成功
        self.__create_skill_succeed_metric()
        return True, {}

    def __update_task_display_name(self, display_name: str):
        """
        更新任务显示名称

        Args:
            display_name: str, 新的display_name
        """

        # 更新task的display_name，因为pf的task无法在创建时设置display_name
        try:
            job_name = job_api.parse_job_name(self.config.job_name)
            update_task_req = task_api.UpdateTaskRequest(
                workspace_id=job_name.workspace_id,
                job_name=job_name.local_name,
                local_name=self.config.skill_task_name,
                display_name=display_name)
            self.__job_cli.update_task(request=update_task_req)
        except Exception as e:
            bcelogger.error(
                "SyncSkillUpdateTaskDisplayName Failed: %s", traceback.format_exc())

    @ abstractmethod
    def list_targets(self):
        """
        获取下发目的地列表

        Returns:
            bool: 是否成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
            list[dict]: 目标列表
        """

        pass

    @ abstractmethod
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

        pass

    @ abstractmethod
    def sync_model(self, target: dict,
                   extra_data: dict):
        """
        下发模型

        Args:
            target: dict, 下发目标
            extra_data: dict, 额外参数
        Returns:
            bool: 是否下发成功
            dict: 错误信息, 例如：{"error": "Internal Server Error xxxx", "reason": "技能上线失败"}
        """

        pass

    @ abstractmethod
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

        pass

    @ abstractmethod
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

        pass

    def run(self):
        """
        执行技能下发逻辑
        """

        bcelogger.info("SyncSkill Start")

        self.__update_task_display_name("技能模板下发")

        ok, msg = self.__get_skill()
        if not ok:
            self.__mark_job_failed(reason=msg["reason"],
                                   message=msg["error"][:500])
            return

        bcelogger.debug("SyncSkillGetSkill Succeed, skill:%s", self.skill)

        ok, msg, self.targets = self.list_targets()
        if not ok:
            self.__mark_job_failed(reason=msg["reason"],
                                   message=msg["error"][:500])
            return

        bcelogger.debug(
            "SyncSkillListTargets Succeed, targets:%s", self.targets)

        # 要从Artifact的tag取，因为下发是指定了技能的版本
        # skill_tag = []
        # if skill.graph is not None and 'artifact' in skill.graph:
        #     skill_tag = skill.graph['artifact']['tags']
        # bcelogger.debug("SyncSkillSkillTags: %s", skill_tag)

        self.__create_skill_total_metric()

        for target in self.targets:
            bcelogger.info("SyncSkillTargetInfo: %s", target)
            target_displayname = target.get("displayName", "")
            target_id = target.get("localName", None)

            # 下发模型
            sync_model_extra_data = {}
            sync_model_extra_data["model_succeed_result"] = self.config.sync_model_result
            ok, msg = self.sync_model(
                target=target, extra_data=sync_model_extra_data)
            if not ok:
                self.__skill_failed_count += 1
                self.__job_failed_count += 1

                self.__create_skill_failed_metric()
                self.__create_job_failed_metric_event(message=msg["error"][:500],
                                                      reason=msg["reason"])
                continue

            ok, msg = self.__sync_skill(target=target)
            if not ok:
                self.__job_failed_count += 1
                reason = self.__event_reason_format.format(
                    target_displayname, target_id, msg["reason"])
                self.__create_job_failed_metric_event(message=msg["error"][:500],
                                                      reason=reason)
                continue

            # job下发成功
            self.__job_succeed_count += 1
            reason = self.__event_reason_format.format(
                target_displayname, target_id, "下发成功")
            self.__create_job_succeed_metric_event(
                message=reason, reason=reason)

            bcelogger.info("SyncSkill End")


def check_accelerators(skill_accelerator: str,
                       target_accelelator: str):
    """
    检查硬件是否匹配

    Args:
        skill_accelerator(str): 技能硬件信息(tag['accelerator'])
        target_accelelator(str): 设备硬件型号
    Returns:
        bool: 是否匹配
        str: 错误信息
    """

    if skill_accelerator == "":
        return True, ""

    if target_accelelator == "":
        return False, "设备硬件不适配"

    # 将技能硬件信息转换为列表
    skill_accelerators = json.loads(skill_accelerator)
    device_accelerators = [target_accelelator]

    for sac in skill_accelerators:
        if sac not in device_accelerators:
            return False, "设备硬件不适配"

    return True, ""


def build_skill_graph(
        origin_graph: dict,
        replace: dict):
    """
    构建graph, 内容替换<old,new>

    Args:
        origin_graph: dict 原始图
        replace: dict 替换关系<old,new>
    Returns:
        dict: 新图
    """

    origin_graph_json = json.dumps(origin_graph)
    for old, new in replace.items():
        origin_graph_json = origin_graph_json.replace(old, new)
    return json.loads(origin_graph_json)


def get_model_name(graph: dict):
    """
    获取模型名称

    Args:
        graph: dict 图
    Returns:
        str: 模型名称, 若未找到返回None
    """

    nodes = graph['nodes']
    for node in nodes:
        if node['kind'] == 'ObjectDetectOperator':
            for property in node['properties']:
                if property['name'] == 'modelName':
                    return property['value']
    return None
