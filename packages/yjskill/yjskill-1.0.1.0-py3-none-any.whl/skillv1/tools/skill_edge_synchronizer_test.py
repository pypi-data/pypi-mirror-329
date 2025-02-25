# -*- coding: utf-8 -*-

import unittest

from ..client import skill_api_skill as skill_api


class TestSyncEdge(unittest.TestCase):
    """
    TestSyncEdge
    """

    def test_create_skill_req(self):
        """
        Test create_skill_req
        """

        create_skill_req = skill_api.CreateSkillRequest(
            workspaceID="ws",
            localName="local name",
            displayName="display name",
            description="description",
            kind="kd",
            fromKind="Edge",
            createKind="Sync")

        result = {}
        result["create_skill_request"] = create_skill_req

        req = result.get("create_skill_request")
        print(f'workspace_id: {req.workspace_id}')


def suite():
    """
    suite
    """
    suite = unittest.TestSuite()
    suite.addTest(TestSyncEdge('test_create_skill_req'))
    return suite


if __name__ == '__main__':
    print('starting tests...')
    unittest.main(defaultTest='suite')
