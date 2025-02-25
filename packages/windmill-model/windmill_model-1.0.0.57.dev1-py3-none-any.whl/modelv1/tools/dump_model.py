#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/9/10
# @Author  : zhangzhijun
# @File    : dump_model.py
"""
import os
import shutil

from argparse import ArgumentParser

import bcelogger

from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import parse_model_name

from tritonv2.model_config import ModelConfig
from tritonv2.utils import BlobStoreFactory


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--model_name", required=False, type=str, default="")
    parser.add_argument("--output_uri",
                        required=False,
                        type=str,
                        default="/data/model")
    parser.add_argument("--rename",
                        required=False,
                        type=str,
                        default="ensemble")
    parser.add_argument("--set_submodel_version",
                        action="store_true",
                        required=False,
                        default=False)
    # 是否禁用模型下载, 使用本地模型文件时开启禁用, 默认不禁用
    parser.add_argument("--disable_dump_model",
                        action="store_true",
                        required=False,
                        default=False,
                        help="disable download model from filesystem, enable when use local models")

    args, _ = parser.parse_known_args()

    return args


def modify_model(windmill_client, artifact_name, model_path, model_version=None):
    """
    modify the file path and submodel version of the model according to the artifact information
    """

    if model_version is None:
        model_version = {}  # key: model name, value: model version
    name = parse_artifact_name(artifact_name)
    model_name = parse_model_name(name.object_name)
    bs = BlobStoreFactory.create(kind="local", bucket="", endpoint_url="")

    manifest_list = windmill_client.get_model_manifest(model_name.workspace_id,
                                                       model_name.model_store_name,
                                                       model_name.local_name,
                                                       name.version)
    for model in manifest_list.subModels:
        model_version[model["localName"]] = str(model["artifact"]["version"])

    for model in manifest_list.subModels:
        # 兼容一个模型包中有多个 ensemble 节点的情况
        if model["localName"] != model_name.local_name:
            modify_model(windmill_client, model["artifact"]["name"], model_path, model_version)

        # set sub model version of ensemble model
        sub_model_version_path = os.path.join(str(model_path), model["localName"],
                                              str(model["artifact"]["version"]))
        if not os.path.exists(sub_model_version_path):
            raise ValueError(f"can not find model file of {model_name.local_name} in local path {model_path}")

        # modify the directory structure according to triton standards
        for file_name in os.listdir(sub_model_version_path):
            src_path = sub_model_version_path + "/" + file_name
            if os.path.isdir(src_path):
                continue

            if file_name.endswith(".yaml") or file_name.endswith(".yml") or file_name.endswith(".pbtxt"):
                dest_path = os.path.abspath(sub_model_version_path + "/../" + file_name)
                shutil.copyfile(src_path, dest_path)

        sub_model_path = os.path.join(str(model_path), model["localName"])
        config_path = os.path.join(sub_model_path, "config.pbtxt")
        if not bs.exist(config_path):
            continue
        config = ModelConfig.create_from_file(config_path)
        if config.is_ensemble():
            step = config.get_ensemble_steps()
            for sub_model_name, sub_model_info in step.items():
                if sub_model_name not in model_version.keys():
                    raise ValueError(f"{model_name.local_name} has no submodel {sub_model_name}")
                config.set_scheduling_model_version(sub_model_name, model_version[sub_model_name])
            config.write_to_file(config_path, bs)

        if config.is_bls():
            sub_models = config.get_bls_submodels()
            for sub_model_name, sub_model_version in sub_models.items():
                if sub_model_name not in model_version.keys():
                    raise ValueError(f"{model_name.local_name} has no submodel {sub_model_name}")
                config.set_bls_submodels_version(sub_model_name, model_version[sub_model_name])
            config.write_to_file(config_path, bs)


def run():
    """
    dump model.
    """
    args = parse_args()
    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={
                                         "OrgID": org_id,
                                         "UserID": user_id
                                     })

    model_path = args.output_uri
    if not args.disable_dump_model:
        output_uri = os.path.join(args.output_uri, args.model_name)
        if not os.path.exists(output_uri):
            os.makedirs(output_uri)

        if len(os.listdir(output_uri)) > 0:
            bcelogger.warning(
                f"Output directory {output_uri} already exists and is not empty.")
            return
        else:
            windmill_client.dump_models(artifact_name=args.model_name,
                                        rename=args.rename,
                                        output_uri=output_uri)
            bcelogger.info(f"Model {args.model_name} dumped successfully")
            model_path = output_uri

    # set the version of the submodel
    if args.set_submodel_version:
        modify_model(windmill_client, args.model_name, model_path)


if __name__ == "__main__":
    run()
