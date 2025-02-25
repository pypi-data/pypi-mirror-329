# -*- coding: utf-8 -*-
import unittest
import time
import json
import traceback

from . import skill_edge_synchronizer
from ..client.skill_api_skill import CreateSkillRequest, GetSkillRequest, UpdateSkillRequest
from jobv1.client.job_client import (
    JobClient,
    CreateJobRequest, CreateTaskRequest, CreateEventRequest, UpdateJobRequest,
    CreateMetricRequest, GetJobRequest, DeleteMetricRequest, DeleteJobRequest
)
from jobv1.client.job_api_event import EventKind
from jobv1.client.job_api_metric import MetricKind, CounterKind, MetricLocalName, DataType
from devicev1.client import device_client, device_api

from . import skill_synchronizer
from . import sync_skill

workspace_id = "wsgdessn"
job_local_name = "leibin_test_job_1"
# job_endpoint = "127.0.0.1:80"
job_endpoint = "http://10.224.41.35:8340"
device_endpoint = "10.224.41.35:8340"
org_id = "ab87a18d6bdf4fc39f35ddc880ac1989"
user_id = "7e0c86dd01ae4402aa0f4e003f3480fd"
skill_endpoint = "10.224.41.35:8440"
# skill_name = "sk-ToXHTrNv"
skill_name = "sk-HkSDwvWU"
skill_version = "3"


class TestSyncSkillll(unittest.TestCase):
    """
    Test SyncSkill Python SDK
    """

    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName)
        self.job_client = JobClient(endpoint=job_endpoint,
                                    context={"OrgID": org_id, "UserID": user_id})
        self.device_client = device_client.DeviceClient(endpoint=device_endpoint,
                                                        context={"OrgID": org_id, "UserID": user_id})
        self.skill_task_local_name = ""
        self.model_task_local_name = ""

        self.skill_name = f"workspaces/{workspace_id}/skills/{skill_name}/versions/1"
        self.target_names = [
            f"workspaces/{workspace_id}/devicehubs/default/devices/dbsh3000snc24g0017"]

        self.config = skill_synchronizer.SkillSynchronizerConfig(
            sync_kind=skill_synchronizer.SyncSkillKind.Edge,
            skill_name=self.skill_name,
            skill_create_kind="Sync",
            skill_from_kind="Edge",
            vistudio_endpoint=skill_endpoint,
            windmill_endpoint=device_endpoint,
            org_id=org_id,
            user_id=user_id,
            job_name="",
            skill_task_name="",
            sync_model_result={},
            target_names=self.target_names)
        self.syncer = skill_edge_synchronizer.SkillEdgeSynchronizer(
            config=self.config)

    def test_get_skill(self):
        """
        Test Get Skill
        """

        ok, msg = self.syncer._SkillSynchronizer__get_skill()
        skill = self.syncer.skill
        assert ok, f'Get Skill failed'

        if skill.graph is not None and 'draft' in skill.graph:
            skill.graph['draft'] = {}
            print(f"\nskill has draft, cleaned:\n")

        print(f"\nskill:\n{skill}")
        print(f'\nskill.loacalName:\n{skill.localName}')
        print(
            f"\nskill.graph:\n{json.dumps(skill.graph, ensure_ascii=False)}\n")
        print(
            f"\nskill.artifact:\n{skill.graph.get('artifact')}")
        skill_tag = []
        artifact_version = ""
        if skill.graph is not None and 'artifact' in skill.graph:
            skill_tag = skill.graph['artifact']['tags']
            artifact_version = skill.graph['artifact']['version']
        print(f"\nskill_tag:\n{skill_tag}")
        print(
            f"\nartifact_version:\n{type(artifact_version)}_{artifact_version}")
        print(f"\nskill.imageURI:\n{skill.imageURI}")
        print(f"\nskill.defaultLevel:\n{skill.defaultLevel}")
        print(f"\nskill.alarmConfigs:\n{skill.alarmConfigs}")

        nodes = skill.graph['nodes']
        for node in nodes:
            if node['kind'] == 'ObjectDetectOperator':
                for property in node['properties']:
                    if property['name'] == 'modelName':
                        print(f"\nmodel_name:\n{property['value']}")

        replace = {
            "workspaces/wsgdessn/modelstores/modelstore/models/ensemble/versions/1": "workspaces/wsgdessn/modelstores/ms-WtQTMetu/models/ensemble/versions/1"}
        new_graph = skill_synchronizer.build_skill_graph(
            skill.graph, replace=replace)
        print(f"\nnew_graph:\n{json.dumps(new_graph, ensure_ascii=False)}\n")

        print(f"\nskill.kind:\n{skill.kind}")
        edge = {
            'kind': 'DB-SH3',
            'status': 'Online',
        }
        ok, msg = self.syncer._SkillEdgeSynchronizer__check_edge(
            edge=edge)

        assert ok, msg

    def test_build_graph(self):
        """
        Test Build Graph
        """

    def test_parse_device_name(self):
        """
        parse device name
        """
        edge_name = "workspaces/wsgdessn/devicehubs/default/devices/dbsh3000snc24g0017"
        device_name = device_api.parse_device_name(edge_name)
        print(f'\ndevice_name: \n{device_name}')
        print(device_name.local_name)

    def test_list_devices(self):
        """
        Test List Devices
        """

        print(f"\nconfig:\n{self.config}\n")
        ok, msg, result = self.syncer.list_targets()
        print(f"\ndevices:\n{result}")
        if len(result) == 0:
            print("No devices found.")
            return
        target = result[0]
        target_displayname = target.get("displayName", "")
        target_id = target.get("localName", None)
        print(f"\ntarget_displayname:\n{target_displayname}")
        print(f"\ntarget_id:\n{target_id}")
        print(f"\ntarget.localName:\n{target.get('localName')}")

    def test_create_job(self):
        """
        Test Job Service
        """

        job_client = self.job_client

        self.test_del_job()

        create_job_req = CreateJobRequest(
            workspace_id=workspace_id,
            display_name="leibin_test_job",
            local_name=job_local_name,
            tasks=[
                CreateTaskRequest(
                    workspace_id=workspace_id,
                    display_name="技能下发",
                    kind="Distribute/Skill"
                ),
                CreateTaskRequest(
                    workspace_id=workspace_id,
                    display_name="模型下发",
                    kind="Distribute/Model"
                ),
            ],
            tags={"SkillName": "lb测试技能"},
        )
        create_job_resp = self.job_client.create_job(create_job_req)
        print(f'\ncreate_job_resp:\n{create_job_resp}')

        self.skill_task_local_name = create_job_resp.tasks[0].local_name
        print(f'\nskill_task_name:\n{self.skill_task_local_name}')
        self.model_task_local_name = create_job_resp.tasks[1].local_name
        print(f'\nmodel_task_name:\n{self.model_task_local_name}')

    def test_create_skill_task_event(self):
        """
        Test Create Skill Task Event
        """

        print(f'skill_task_name:{self.skill_task_local_name}')

        job_client = JobClient(endpoint=job_endpoint,
                               context={"OrgID": "org_id", "UserID": "user_id"})

        create_skill_task_event_req = CreateEventRequest(
            workspace_id=workspace_id,
            job_name=job_local_name,
            task_name=self.skill_task_local_name,
            kind=EventKind.Succeed,
            reason="手动更新技能task",
            message="就手动")
        create_skill_task_event_resp = job_client.create_event(
            create_skill_task_event_req)
        print(create_skill_task_event_resp)

    def test_del_job(self):
        """
        Test del job
        """
        try:

            # job_client = JobClient(endpoint=job_endpoint,
            #                        context={"OrgID": "org_id", "UserID": "user_id"})

            job = self.test_get_job()
            if job is None or job.name == "":
                print(f'\njob not exist\n')
                return

            create_metric_req = CreateMetricRequest(
                workspace_id=workspace_id,
                job_name=job_local_name,
                local_name=MetricLocalName.Status,
                kind=MetricKind.Gauge,
                data_type=DataType.String,
                value=['Failed']
            )
            create_metric_resp = self.job_client.create_metric(
                create_metric_req)
            print(f'\ncreate_metric_resp:\n {create_metric_resp}')

            time.sleep(5)
            del_job_req = DeleteJobRequest(
                workspace_id=workspace_id,
                local_name=job_local_name,
            )
            del_job_resp = self.job_client.delete_job(del_job_req)
            print(f'\ndel_job_resp:\n{del_job_resp}')
        except Exception as e:
            print(e)
            print(f'{traceback.format_exc()}')

    def test_get_job(self):
        """
        Test get job
        """

        get_job_req = GetJobRequest(
            workspace_id=workspace_id,
            local_name=job_local_name
        )
        # job_client = JobClient(endpoint=job_endpoint,
        #                        context={"OrgID": "org_id", "UserID": "user_id"})
        get_job_resp = self.job_client.get_job(get_job_req)
        print(f'\nget_job_resp:\n{get_job_resp}')
        print(f'\njob status: {get_job_resp.status}')
        print(
            f'\ntask {get_job_resp.tasks[0].name} status: {get_job_resp.tasks[0].status}')
        print(
            f'\ntask {get_job_resp.tasks[1].name} status: {get_job_resp.tasks[1].status}')
        return get_job_resp

    def test_metric(self):
        """
        Test metric
        """

        print(f'begin test_metric')
        self.test_create_job()

        # job_client = JobClient(endpoint=job_endpoint,
        #                        context={"OrgID": "org_id", "UserID": "user_id"})
        # del skill task metric
        del_metric_req = DeleteMetricRequest(
            workspace_id=workspace_id,
            job_name=job_local_name,
            task_name=self.skill_task_local_name,
            local_name=MetricLocalName.Total)
        del_metric_resp = self.job_client.delete_metric(del_metric_req)
        print(
            f'\ndel skill task metric total del_metric_resp: \n{del_metric_resp}')
        del_metric_req = DeleteMetricRequest(
            workspace_id=workspace_id,
            job_name=job_local_name,
            task_name=self.skill_task_local_name,
            local_name=MetricLocalName.Success)
        del_metric_resp = self.job_client.delete_metric(del_metric_req)
        print(
            f'\ndel skill task metric success del_metric_resp: \n{del_metric_resp}')
        # del model task metric
        del_metric_req = DeleteMetricRequest(
            workspace_id=workspace_id,
            job_name=job_local_name,
            task_name=self.model_task_local_name,
            local_name=MetricLocalName.Total)
        del_metric_resp = self.job_client.delete_metric(del_metric_req)
        print(f'\ndel model task total del_metric_resp: \n{del_metric_resp}')
        del_metric_req = DeleteMetricRequest(
            workspace_id=workspace_id,
            job_name=job_local_name,
            task_name=self.model_task_local_name,
            local_name=MetricLocalName.Success)
        del_metric_resp = self.job_client.delete_metric(del_metric_req)
        print(f'\ndel model task success del_metric_resp: \n{del_metric_resp}')

        # create skill task metric
        create_metric_total_req = CreateMetricRequest(
            workspace_id=workspace_id,
            job_name=job_local_name,
            task_name=self.skill_task_local_name,
            display_name="技能下发metric",
            local_name=MetricLocalName.Total,
            kind=MetricKind.Counter,
            counter_kind=CounterKind.Cumulative,
            value=['2']
        )
        create_metric_total_resp = self.job_client.create_metric(
            create_metric_total_req)
        print(f'\ncreate_metric_total_resp:\n{create_metric_total_resp}')

        # create model task metric
        create_metric_total_req = CreateMetricRequest(
            workspace_id=workspace_id,
            job_name=job_local_name,
            task_name=self.model_task_local_name,
            display_name="模型下发metric",
            local_name=MetricLocalName.Total,
            kind=MetricKind.Counter,
            counter_kind=CounterKind.Cumulative,
            value=['2']
        )
        create_metric_total_resp = self.job_client.create_metric(
            create_metric_total_req)
        print(f'\ncreate_metric_total_resp:\n{create_metric_total_resp}')

        time.sleep(5)
        # 模型metric +2
        create_metric_total_req = CreateMetricRequest(
            workspace_id=workspace_id,
            job_name=job_local_name,
            task_name=self.model_task_local_name,
            display_name="模型下发metric",
            local_name=MetricLocalName.Success,
            kind=MetricKind.Counter,
            counter_kind=CounterKind.Cumulative,
            value=['1']
        )
        self.job_client.create_metric(create_metric_total_req)
        print(f'\ncreate_metric_total_resp:\n{create_metric_total_resp}')

        self.test_get_job()

    def test_sync_skill_run(self):
        """
        Test run

        --sync_kind=Edge \
        --skill_name=workspaces/wsgdessn/skills/sk-ToXHTrNv/versions/1 \
        --target_names=workspaces/wsgdessn/devicehubs/default/devices/dbsh3000snc24g0017
        """
        sync_skill.run()


def suite():
    """
    suite
    """
    suite = unittest.TestSuite()
    # suite.addTest(TestSyncSkillll('test_metric'))
    suite.addTest(TestSyncSkillll('test_list_devices'))
    # suite.addTest(TestSyncSkillll('test_parse_device_name'))
    # suite.addTest(TestSyncSkillll('test_get_skill'))
    # suite.addTest(TestSyncSkillll('test_sync_skill_run'))
    return suite


if __name__ == '__main__':
    print('starting tests...')
    unittest.main(defaultTest='suite')
