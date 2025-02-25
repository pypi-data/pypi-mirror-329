#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
windmill_dump.py
Authors: zhangzhijun06(zhangzhijun06@baidu.com)
Date:    2024/09/04-2:38 PM
"""
import bcelogger
import subprocess
import traceback
import yaml
import os
from argparse import ArgumentParser

from baidubce.exception import BceHttpClientError
from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.filesystem import download_by_filesystem
from windmilltrainingv1.client.training_api_job import parse_job_name
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillcategoryv1.client.category_api import match
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


def run():
    """
    import model.
    """
    args = parse_args()
    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={"OrgID": org_id, "UserID": user_id})

    # 下载模型
    model_store = parse_modelstore_name(args.model_store_name)
    job_name = parse_job_name(args.job_name)
    tags = {}
    file_name = "model.tar"
    try:
        if args.uri.startswith("http"):
            cmd = ['curl', '-o', file_name, args.uri]
            subprocess.run(cmd, shell=False, check=True)
        else:
            filesystem = windmill_client.suggest_first_filesystem(model_store.workspace_id,
                                                                  guest_name=model_store.get_name())
            file_name = os.path.basename(args.uri)
            download_by_filesystem(filesystem, args.uri, file_name)
    except Exception as e:
        tags = {
            "errorCode": "102",
            "errorMessage": "模型路径有误：uri不存在！"
        }
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        return

    # 模型解压
    try:
        result = subprocess.run(['tar', '-xf', file_name, '-C', '.'],
                                check=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        bcelogger.info(f"Import Model Job {args.job_name} Success: {result.stdout}")
    except Exception as e:
        tags = {
            "errorCode": "103",
            "errorMessage": "文件解压报错！"
        }
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        return

    if not os.path.exists("apply.yaml"):
        tags = {
            "errorCode": "101",
            "errorMessage": "文件格式错误：apply.yaml文件不存在！"
        }
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: apply.yaml file does not exist")
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        return

    # 解析并上传模型
    model_list = []
    with open('apply.yaml', 'r') as fb:
        for data in yaml.safe_load_all(fb):
            tags[data["metadata"]["localName"]] = ""
            model_list.append(data)
    windmill_client.update_job(workspace_id=job_name.workspace_id,
                               project_name=job_name.project_name,
                               local_name=job_name.local_name,
                               tags=tags)

    try:
        for model in model_list:
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
                        artifact_uri=model["metadata"]["artifact"]["uri"])

            if match(model["metadata"]["category"], Category.CategoryImageEnsemble.value):
                model_list = windmill_client.get_model_manifest(model_store.workspace_id,
                                                                model_store.local_name,
                                                                resp.localName,
                                                                str(resp.artifact["version"]))
                for item in model_list.subModels:
                    tags[item["localName"]] = str(item["artifact"]["version"])
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "内部服务错误！"
        }
        bcelogger.error(f"ImportModelJob {args.job_name} Failed: {traceback.format_exc()}")

    windmill_client.update_job(workspace_id=job_name.workspace_id,
                               project_name=job_name.project_name,
                               local_name=job_name.local_name,
                               tags=tags)


if __name__ == "__main__":
    run()
