# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import os
import json

import bcelogger

from .skill_synchronizer import SyncSkillKind, SkillSynchronizerConfig
from .skill_edge_synchronizer import SkillEdgeSynchronizer


def run():
    """
    运行技能下发
    """

    bcelogger.info("SyncSkill Start")

    args = parse_args()
    bcelogger.info("SyncSkill Args: %s", args)

    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    job_name = os.getenv("JOB_NAME", "")
    skill_task_name = os.getenv("PF_STEP_NAME", "")
    model_result_path = os.getenv(
        "PF_INPUT_ARTIFACT_MODEL_URI", "")
    vistudio_endpoint = os.getenv("VISTUDIO_ENDPOINT", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    bcelogger.info("SyncSkill envs, \n \
                   org_id: %s, \n \
                   user_id: %s, \n \
                   job_name: %s, \n \
                   skill_task_name: %s, \n \
                   vistudio_endpoint: %s, \n \
                   windmill_endpoint: %s, \n \
                   model_result_path: %s", org_id, user_id,
                   job_name, skill_task_name, vistudio_endpoint,
                   windmill_endpoint, model_result_path)
    # key=device_name, value={}
    model_succeed_result = {}
    if os.path.exists(model_result_path):
        with open(model_result_path, 'r', encoding='utf-8') as file:
            model_succeed_result = json.load(file)
            bcelogger.info("SyncSkill ModelSucceedResult: %s",
                           model_succeed_result)
    else:
        bcelogger.warning(
            f'SyncSkill ModelSucceedResult File Not Exists, %s', model_result_path)

    sync_kind = SyncSkillKind[args.sync_kind]

    target_names = args.target_names.split(",")
    config = SkillSynchronizerConfig(
        sync_kind=sync_kind,
        skill_name=args.skill_name,
        skill_create_kind="Sync",
        skill_from_kind="Edge",
        vistudio_endpoint=vistudio_endpoint,
        target_names=target_names,
        windmill_endpoint=windmill_endpoint,
        org_id=org_id,
        user_id=user_id,
        job_name=job_name,
        skill_task_name=skill_task_name,
        sync_model_result=model_succeed_result)

    syncer = None
    if SyncSkillKind.Edge == sync_kind:
        syncer = SkillEdgeSynchronizer(config=config)
    else:
        # 其他类型的同步器暂不支持
        raise ValueError(f"Unsupported sync kind {args.sync_kind}")
    syncer.run()
    bcelogger.info("SyncSkill End")


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--sync_kind", required=True, type=str, default="Edge")
    parser.add_argument("--skill_name",
                        required=True, type=str, default="")
    parser.add_argument("--target_names", required=True, type=str, default="")

    args, _ = parser.parse_known_args()
    return args


if __name__ == "__main__":
    run()
