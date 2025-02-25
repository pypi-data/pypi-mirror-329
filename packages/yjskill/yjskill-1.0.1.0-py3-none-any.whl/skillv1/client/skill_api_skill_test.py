# -*- coding: utf-8 -*-
import unittest
import json

from windmillartifactv1.client import artifact_api_artifact as artifact_api

from .skill_api_skill import CreateSkillRequest, parse_skill_name
from ..tools.skill_synchronizer import build_skill_graph, check_accelerators


class TestSkillAPI(unittest.TestCase):
    """
    Test Device
    """

    # def test_check_edge(self):
    #     """
    #     检查技能是否能下发到盒子
    #     """
    #     skill_tag = {}
    #     model_accelerators = ["T4", ["gpu1"]]
    #     json.dumps(model_accelerators)
    #     skill_tag["accelerator"] = json.dumps(model_accelerators)

    #     edge = {
    #         "status": "Disconnected",
    #         "kind": "123"
    #     }
    #     device_config = {"abc": "gpu1"}
    #     ok, msg = check_edge(skill_tag=skill_tag, edge=edge,
    #                          device_config=device_config)
    #     self.assertEqual(ok, False)
    #     self.assertEqual(msg, "设备已断开连接")

    #     edge["status"] = "Processing"
    #     ok, msg = check_edge(skill_tag=skill_tag, edge=edge,
    #                          device_config=device_config)
    #     self.assertEqual(ok, False)
    #     self.assertEqual(msg, "设备正在下发中")

    #     edge["status"] = ""
    #     ok, msg = check_edge(skill_tag=skill_tag, edge=edge,
    #                          device_config=device_config)
    #     self.assertEqual(ok, False)
    #     self.assertEqual(msg, "未找到设备的硬件信息")

    #     edge["kind"] = "abc"
    #     ok, msg = check_edge(skill_tag=skill_tag, edge=edge,
    #                          device_config=device_config)
    #     self.assertEqual(ok, True)

    def test_check_accelerator(self):
        """
        检查技能是否能下发到加速器
        """

        skill_tag = ""
        device_tag = ""
        ok, msg = check_accelerators(
            skill_accelerator=skill_tag, device_accelelator=device_tag)
        self.assertEqual(ok, True)

        skill_tag = '[\"T4\",\"A100\"]'
        ok, msg = check_accelerators(
            skill_accelerator=skill_tag, device_accelelator=device_tag)
        self.assertEqual(ok, False)

        device_tag = "abc"
        ok, msg = check_accelerators(
            skill_accelerator=skill_tag, device_accelelator=device_tag)
        self.assertEqual(ok, False)

        device_tag = "A100"
        ok, msg = check_accelerators(
            skill_accelerator=skill_tag, device_accelelator=device_tag)
        self.assertEqual(ok, False)

    def test_build_graph(self):
        """
        Test build graph
        """
        graph = {
            "name": "workspaces/wsnfkyki/modelstores/",
            "content": {
                "name": "workspaces/wsnfkyki/modelstores/",
            }
        }
        graph = build_skill_graph(origin_graph=graph, replace={
                                  "wsnfkyki": "123456"})
        self.assertTrue(graph["name"] == "workspaces/123456/modelstores/")
        self.assertTrue(graph["content"]["name"] ==
                        "workspaces/123456/modelstores/")

    def test_create_skill_request(self):
        """
        Test create skill request
        """

        req = CreateSkillRequest(
            workspaceID="ws",
            localName="local",
            displayName="display",
            description="description",
            kind="Video",
            createKind="Manual",
            fromKind="Other",
            tags={"hello_tag": "world_tag"},
            graph={"name": "graph_name"},
            imageURL="http://www.baidu.com",
            defaultLevel=4)
        print(req.model_dump_json(by_alias=True))

    def test_parse_skill_name(self):
        """
        Test parse skill name
        """

        name = "workspaces/123/skills/sikk/versions/1"
        artifact_name = artifact_api.parse_artifact_name(name)
        print(f'{artifact_name.object_name}')
        print(f'{artifact_name.version}')
        skill_name = parse_skill_name(artifact_name.object_name)
        print(skill_name)
        assert skill_name.workspace_id == "123"
        assert skill_name.local_name == "sikk"
        assert artifact_name.version == "1"


def suite():
    """
    suite
    """
    suite = unittest.TestSuite()
    # suite.addTest(TestSkillAPI('test_check_accelerator'))
    suite.addTest(TestSkillAPI('test_parse_skill_name'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
