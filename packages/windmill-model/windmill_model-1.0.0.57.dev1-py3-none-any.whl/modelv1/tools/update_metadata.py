#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/8/2
# @Author  : yanxiaodong
# @File    : model_metadata_update.py
"""
import base64
import time
import json
import shutil
from argparse import ArgumentParser

import bcelogger
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.metadata.metadata import update_metadata as model_update_metadata


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--windmill-endpoint", type=str, default="")
    parser.add_argument("--windmill-ak", type=str, default="")
    parser.add_argument("--windmill-sk", type=str, default="")
    parser.add_argument("--org-id", type=str, default="")
    parser.add_argument("--user-id", type=str, default="")
    parser.add_argument("--model-name", type=str, default="")
    parser.add_argument("--sub-models", type=str, default="")
    parser.add_argument("--extra-models", type=str, default="")

    args, _ = parser.parse_known_args()

    return args


def update_metadata(args):
    """
    Update the model metadata.
    """
    windmill_client = WindmillClient(ak=args.windmill_ak,
                                     sk=args.windmill_sk,
                                     endpoint=args.windmill_endpoint,
                                     context={"OrgID": args.org_id, "UserID": args.user_id})

    # 1. Build the model graph
    model_uri = f"/home/windmill/model/{time.time()}"
    sub_models = json.loads(base64.b64decode(args.sub_models))
    sub_models = sub_models if sub_models is not None else {}
    extra_models = json.loads(base64.b64decode(args.extra_models))
    extra_models = extra_models if extra_models is not None else {}
    graph = windmill_client.build_graph(ensemble_name=args.model_name,
                                        sub_models=sub_models,
                                        extra_models=extra_models,
                                        input_uri=model_uri)

    # 2. get artifact
    response = windmill_client.get_artifact(name=args.model_name)
    bcelogger.info(f"Model {args.model_name} response: {response}")

    # 3. update metadata
    model_update_metadata(graph=graph, metadata=response.metadata, input_uri=model_uri)

    # 4. update artifact
    windmill_client.update_artifact(name=args.model_name, metadata=response.metadata)
    bcelogger.info(f"Update model metadata {response.metadata} successfully")

    # 5. 删除模型
    shutil.rmtree(model_uri)
    bcelogger.info(f"Delete model {model_uri} successfully")


if __name__ == "__main__":
    args = parse_args()
    update_metadata(args)
