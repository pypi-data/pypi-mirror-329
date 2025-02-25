#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
import_model.py
Authors: liyutao01(liyutao01@baidu.com)
Date:    2025/01/17
"""

import bcelogger
import subprocess
import traceback
import yaml
import os
from argparse import ArgumentParser

from baidubce.exception import BceHttpClientError
from bceinternalsdk.client.paging import PagingRequest
from jobv1.client.job_client import JobClient
from jobv1.client.job_api_event import CreateEventRequest, EventKind
from jobv1.client.job_api_job import parse_job_name, GetJobRequest, UpdateJobRequest
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name, LocationStyle
from windmillcategoryv1.client.category_api import match
from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.filesystem import download_by_filesystem, KIND_S3
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillmodelv1.client.model_api_model import Category


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--uri", required=False, type=str, default="")
    parser.add_argument("--model_store_name", required=False, type=str, default="")
    parser.add_argument("--job_name", required=False, type=str, default="")

    args, _ = parser.parse_known_args()
    return args


def delete_artifacts(windmill_client, artifact_list):
    """
    delete artifact in "artifact_list" and delete model files from filesystem.
    """

    for artifact in artifact_list:
        artifact_name = parse_artifact_name(artifact["name"])
        windmill_client.delete_artifact(object_name=artifact_name.object_name,
                                        version=str(artifact["version"]),
                                        force=True)


def download_model_package(windmill_client, job_client, args, source_filesystem):
    """
    download model package from remote to local.
    :return: bool, True if success, False if failed
    """

    job_name = parse_job_name(args.job_name)
    create_task_event_req = CreateEventRequest(
        workspace_id=job_name.workspace_id,
        job_name=job_name.local_name,
        kind=EventKind.Succeed,
        reason="模型导入成功",
        message="模型包成功创建并导入本地filesystem")

    # 下载模型包
    model_store = parse_modelstore_name(args.model_store_name)
    file_name = "model.tar"
    try:
        if args.uri.startswith("http"):  # http(s)
            cmd = ['curl', '-o', file_name, args.uri]
            subprocess.run(cmd, shell=False, check=True)
        else:  # s3
            if source_filesystem["kind"] != KIND_S3:
                source_filesystem = windmill_client.suggest_first_filesystem(model_store.workspace_id,
                                                                     guest_name=model_store.get_name())
            file_name = os.path.basename(args.uri)
            download_by_filesystem(source_filesystem, args.uri, file_name)
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "模型路径有误, uri不存在"
        create_task_event_req.message = "模型uri不存在!"
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return False

    # 解压模型包
    try:
        result = subprocess.run(['tar', '-xf', file_name, '-C', '.'],
                                check=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        bcelogger.info(f"Import Model Job {args.job_name} Success: {result.stdout}")
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "模型包格式错误, 解压失败"
        create_task_event_req.message = "模型包解压失败!"
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)
        return False

    if not os.path.exists("apply.yaml"):
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "文件格式错误, apply.yaml文件不存在"
        create_task_event_req.message = "文件格式错误: apply.yaml文件不存在!"
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: apply.yaml file does not exist")
        job_client.create_event(create_task_event_req)
        return False

    return True


def import_model(windmill_client, job_client, args, source_filesystem):
    """
    import model, save model files to local filesystem and create model.
    """

    ensemble_artifact_name = ""  # 模型导入成功后用于更新 job 信息, 上报新导入的模型包 ensemble 节点的 artifact name
    model_store = parse_modelstore_name(args.model_store_name)
    job_name = parse_job_name(args.job_name)
    create_task_event_req = CreateEventRequest(
        workspace_id=job_name.workspace_id,
        job_name=job_name.local_name,
        kind=EventKind.Succeed,
        reason="模型导入成功",
        message="模型包成功创建并导入本地filesystem")

    # 解析模型信息
    model_list = []
    with open('apply.yaml', 'r') as fb:
        for data in yaml.safe_load_all(fb):
            model_list.append(data)

    new_artifact_list = []  # 新导入的原子模型 artifact 列表, 用于模型导入失败时删除模型
    model_version = {}  # 保存导入的模型版本信息, key = 原子模型 localName, value = 模型版本
    try:
        for model in model_list:
            # 判断每个原子模型的 artifact 是否已经存在, 已经存在的 artifact 不重复下载和创建
            source_version = model.get("metadata", {}).get("artifact", {}).get("tags", {}).get("sourceVersion", "")
            if source_version != "":
                artifacts = windmill_client.list_artifact(object_name=(args.model_store_name + "/models/" +
                                                                       model["metadata"]["localName"]),
                                                          page_request=PagingRequest(page_no=1, page_size=1,
                                                                                     order="desc", orderby="version"),
                                                          tags={"sourceVersion": source_version})
                if artifacts.totalCount > 0:
                    artifact = artifacts.result[0]
                    model_version[model["metadata"]["localName"]] = str(artifact["version"])
                    if match(model.get("metadata", {}).get("category", ""), Category.CategoryImageEnsemble.value):
                        ensemble_artifact_name = artifact["name"]
                    bcelogger.info(f"{model['metadata']['localName']} already exists, artifact information: {artifact}")
                    continue

            # 下载没有下载过的模型 model 文件
            # 修正模型 metadata, 使每个节点的 subModels 和 extraModels 中的子模型版本都是本次导入的版本
            # 设置 extraModels 版本信息
            if (("metadata" in model.get("metadata", {}).get("artifact", {})) and
                    model.get("metadata", {}).get("artifact", {})["metadata"] and
                    len(model.get("metadata", {}).get("artifact", {}).get("metadata", {}).get("extraModels", {})) > 0):
                for extra_model_name, _ in model["metadata"]["artifact"]["metadata"]["extraModels"].items():
                    if extra_model_name not in model_version.keys():
                        create_task_event_req.kind = EventKind.Failed
                        create_task_event_req.reason = f"缺少原子模型 {extra_model_name}"
                        create_task_event_req.message = f"缺少原子模型 {extra_model_name}!"
                        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: "
                                        f"sub model {extra_model_name} is missing!")
                        job_client.create_event(create_task_event_req)

                        # 模型导入失败时删除新创建的 artifact
                        delete_artifacts(windmill_client, new_artifact_list)
                        return
                    model["metadata"]["artifact"]["metadata"]["extraModels"][extra_model_name] = (
                        model_version[extra_model_name])
            # 设置 subModels 版本信息
            if (("metadata" in model.get("metadata", {}).get("artifact", {})) and
                    model.get("metadata", {}).get("artifact", {})["metadata"] and
                    len(model.get("metadata", {}).get("artifact", {}).get("metadata", {}).get("subModels", {})) > 0):
                for sub_model_name, _ in model["metadata"]["artifact"]["metadata"]["subModels"].items():
                    if sub_model_name not in model_version.keys():
                        create_task_event_req.kind = EventKind.Failed
                        create_task_event_req.reason = f"缺少原子模型 {sub_model_name}"
                        create_task_event_req.message = f"缺少原子模型 {sub_model_name}!"
                        bcelogger.error(f"ImportDeployModelJob {args.job_name} Failed: "
                                        f"sub model {sub_model_name} is missing!")
                        job_client.create_event(create_task_event_req)

                        delete_artifacts(windmill_client, new_artifact_list)
                        return
                    model["metadata"]["artifact"]["metadata"]["subModels"][sub_model_name] = (
                        model_version[sub_model_name])

            # 如果本地存在模型文件, 直接将本地文件上传到目的 filesystem
            if os.path.isdir(os.path.join(os.getcwd(), model["metadata"]["artifact"]["uri"])):
                source_filesystem = {
                    "host": "",
                    "kind": "file",
                    "endpoint": os.getcwd(),
                    "credential": {
                        "accessKey": "",
                        "secretKey": "",
                    },
                    "config": {
                        "disableSSL": "",
                        "region": "",
                    }
                }

            # 创建模型
            resp = windmill_client.create_model(
                workspace_id=model_store.workspace_id,
                model_store_name=model_store.local_name,
                local_name=model["metadata"]["localName"],
                display_name=model["metadata"]["displayName"],
                prefer_model_server_parameters=model["metadata"]["preferModelServerParameters"],
                category=model["metadata"]["category"],
                model_formats=model["metadata"]["modelFormats"],
                artifact_tags=model["metadata"]["artifact"]["tags"],
                artifact_metadata=model["metadata"]["artifact"]["metadata"],
                artifact_uri=model["metadata"]["artifact"]["uri"],
                style=LocationStyle.TRITON.value,
                source_filesystem=source_filesystem)

            bcelogger.info(f"Create model successfully, model information: {resp}")

            # 记录新增模型 artifact 的信息, 方便模型导入出错时执行清理操作
            new_artifact_list.append(resp.artifact)
            model_version[model["metadata"]["localName"]] = str(resp.artifact["version"])
            if match(model.get("metadata", {}).get("category", ""), Category.CategoryImageEnsemble.value):
                ensemble_artifact_name = resp.artifact["name"]

    except BceHttpClientError as bce_error:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "无法创建模型"
        create_task_event_req.message = f"无法创建模型: {bce_error.last_error.args[0]}"
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)

        delete_artifacts(windmill_client, new_artifact_list)
        return
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "无法创建模型"
        create_task_event_req.message = "内部服务错误: 无法创建模型!"
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)

        delete_artifacts(windmill_client, new_artifact_list)
        return

    # 更新 job 信息, 上报新导入的模型包 ensemble 节点的 artifact name
    try:
        get_job_req = GetJobRequest(workspace_id=job_name.workspace_id, local_name=job_name.local_name)
        resp = job_client.get_job(get_job_req)
        tags = resp.tags if resp.tags else {}
        tags["artifactName"] = ensemble_artifact_name
        update_job_req = UpdateJobRequest(workspace_id=job_name.workspace_id, local_name=job_name.local_name, tags=tags)
        job_client.update_job(update_job_req)
    except BceHttpClientError as bce_error:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "无法更新 job 信息"
        create_task_event_req.message = f"无法更新 job 信息: {bce_error.last_error.args[0]}"
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)

        delete_artifacts(windmill_client, new_artifact_list)
        return
    except Exception as e:
        create_task_event_req.kind = EventKind.Failed
        create_task_event_req.reason = "无法更新 job 信息"
        create_task_event_req.message = "内部服务错误: 无法更新 job 信息!"
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")
        job_client.create_event(create_task_event_req)

        delete_artifacts(windmill_client, new_artifact_list)
        return

    # 模型导入任务成功, 更新 task 状态
    job_client.create_event(create_task_event_req)
    bcelogger.info(f"Import models successfully, models information: {model_version}")


def run():
    """
    download and import model.
    """

    args = parse_args()
    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={"OrgID": org_id, "UserID": user_id})

    job_client = JobClient(endpoint=windmill_endpoint,
                           context={"OrgID": org_id, "UserID": user_id})

    # 构建源 filesystem
    source_filesystem = {
        "host": os.getenv("SOURCE_HOST", ""),
        "kind": os.getenv("SOURCE_KIND", ""),
        "endpoint": os.getenv("SOURCE_ENDPOINT", ""),
        "credential": {
            "accessKey": os.getenv("SOURCE_ACCESS_KEY", ""),
            "secretKey": os.getenv("SOURCE_SECRET_KEY", ""),
        },
        "config": {
            "disableSSL": os.getenv("SOURCE_DISABLE_SSL", ""),
            "region": os.getenv("SOURCE_REGION", ""),
        }
    }

    if not download_model_package(windmill_client, job_client, args, source_filesystem):
        return

    import_model(windmill_client, job_client, args, source_filesystem)


if __name__ == "__main__":
    run()
