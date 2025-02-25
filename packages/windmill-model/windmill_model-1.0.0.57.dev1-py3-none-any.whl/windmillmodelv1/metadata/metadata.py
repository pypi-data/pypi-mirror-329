#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/8/2
# @Author  : yanxiaodong
# @File    : model_metadata_update.py
"""
import os
from collections import defaultdict
from typing import Dict, List
import yaml

import bcelogger
from pygraphv1.client.graph_api_graph import GraphContent
from windmillmodelv1.client.model_api_model import Label, ModelMetadata, InferParameters, InferParameter


def update_metadata(graph: GraphContent, metadata: Dict, input_uri: str = "/home/windmill/tmp/model"):
    """
    Update the model metadata.
    兼容以前算法定义的模型包描述文件规范 https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/0ebIgLpF-L/I1E7bZqZ7Q/SA_YV6fjalxz2M
    """
    postprocess_filename = "parse.yaml"
    infer_config_filename = "config.yaml"
    whitelist_filename = "white_list.yaml"

    track_flag = "track"

    postprocess_file = None
    track_file = None
    infer_config_files = []
    whitelist_file = None
    for root, dirs, files in os.walk(input_uri):
        for file in files:
            absolute_file = os.path.join(root, file)
            if postprocess_filename == os.path.basename(absolute_file):
                postprocess_file = absolute_file
            elif infer_config_filename == os.path.basename(absolute_file) and track_flag in absolute_file:
                track_file = absolute_file
            elif infer_config_filename == os.path.basename(absolute_file):
                infer_config_files.append(absolute_file)
            elif whitelist_filename == os.path.basename(absolute_file):
                whitelist_file = absolute_file
            else:
                continue

    model_metadata = ModelMetadata()
    model_metadata.graphContent = graph
    model_metadata.subModels = metadata["subModels"] if metadata.get("subModels") is not None else {}
    model_metadata.extraModels = metadata["extraModels"] if metadata.get("extraModels", {}) is not None else {}
    model_metadata.labels = []
    model_metadata.inferConfig = []

    # 1. 更新标签信息
    bcelogger.info(f"Postprocess file: {postprocess_file}")
    set_metadata_labels(input_uri=postprocess_file,
                        model_metadata=model_metadata)
    bcelogger.info(f"Model metadata: {model_metadata.dict(by_alias=True, exclude_none=True)['labels']}")

    # 2. 更新白名单信息
    bcelogger.info(f"Whitelist file: {whitelist_file}")
    set_metadata_whitelist(input_uri=whitelist_file,
                           postprocess_file=postprocess_file,
                           model_metadata=model_metadata)
    bcelogger.info(f"Model metadata: {model_metadata.dict(by_alias=True, exclude_none=True)['labels']}")

    # 3. 更新track配置信息
    bcelogger.info(f"Infer track file: {track_file}")
    set_track_config(input_uri=track_file,
                     postprocess_file=postprocess_file,
                     model_metadata=model_metadata)
    bcelogger.info(f"Model metadata: {model_metadata.dict(by_alias=True, exclude_none=True)['inferConfig']}")

    # 4. 更新推理配置信息
    bcelogger.info(f"Infer config files {infer_config_files}")
    set_infer_config(input_uris=infer_config_files, model_metadata=model_metadata)
    bcelogger.info(f"Model metadata: {model_metadata.dict(by_alias=True, exclude_none=True)['inferConfig']}")

    metadata.update(model_metadata.dict(by_alias=True))


def set_track_config(input_uri: str,
                     postprocess_file: str,
                     model_metadata: ModelMetadata):
    """
    Update the track config.
    """
    if input_uri is None or postprocess_file is None:
        return

    postprocess_content = yaml.load(open(postprocess_file, "r"), Loader=yaml.FullLoader)
    track_type = postprocess_content.get("track_type", False)
    if not track_type:
        return

    config_content = yaml.load(open(input_uri, "r"), Loader=yaml.FullLoader)

    for item in config_content["model_parameters"]:
        parameters = InferParameters()
        parameters.modelName = item["master_model"]
        parameters.modelDisplayName = ""
        parameters.isTrack = True
        parameters.parameters = []
        for parameter in item["parameters"]:
            parameter["nameCN"] = parameter.pop("name_cn", "")
            parameter["labelName"] = parameter["name"]
            parameter = InferParameter(**parameter)
            parameters.parameters.append(parameter)
        model_metadata.inferConfig.append(parameters)


def set_infer_config(input_uris: List[str], model_metadata: ModelMetadata):
    """
    Update the infer config.
    """
    infer_config = defaultdict(list)
    for file in input_uris:
        content = yaml.load(open(file, "r"), Loader=yaml.FullLoader)
        infer_config["model_parameters"].extend(content["model_parameters"])

    infer_config_id2value = defaultdict(dict)
    for item in infer_config.get("model_parameters", []):
        for parameter in item["parameters"]:
            infer_config_id2value[parameter["namespace"]] = parameter

    label_model2value = defaultdict(dict)
    for label in model_metadata.labels:
        label_model2value[(label.modelName, label.modelDisplayName)][label.name] = label

    for model, labels in label_model2value.items():
        parameters = InferParameters()
        parameters.modelName = model[0]
        parameters.modelDisplayName = model[1]
        parameters.isTrack = False
        parameters.parameters = []
        for label_name, label in labels.items():
            if label.extraID is not None and label.extraID not in infer_config_id2value:
                parameter = InferParameter(name=label_name,
                                           nameCN="",
                                           labelName=label_name,
                                           namespace=label.extraID,
                                           default=0.5,
                                           range="0,1",
                                           step=0.01,
                                           type="float",
                                           description="")
            elif label.extraID is not None and label.extraID in infer_config_id2value:
                label.threshold = infer_config_id2value[label.extraID]["default"]
                infer_config_id2value[label.extraID]["nameCN"] = infer_config_id2value[label.extraID].pop("name_cn", "")
                infer_config_id2value[label.extraID]["labelName"] = label_name
                parameter = InferParameter(**infer_config_id2value[label.extraID])
            else:
                continue
            parameters.parameters.append(parameter)

        model_metadata.inferConfig.append(parameters)


def set_metadata_whitelist(input_uri: str, postprocess_file: str, model_metadata: ModelMetadata):
    """
    Update the whitelist.
    """
    if input_uri is None or postprocess_file is None:
        return

    postprocess_content = yaml.load(open(postprocess_file, "r"), Loader=yaml.FullLoader)
    if postprocess_content.get("support_white_list", "false") == "false":
        return

    whitelist_content = yaml.load(open(input_uri, "r"), Loader=yaml.FullLoader)

    whitelist_id2value = {}
    for item in whitelist_content.get("white_list", []):
        whitelist_id2value[item["category"]["id"]] = item["similarity_threshold"]

    for label in model_metadata.labels:
        if label.extraID in whitelist_id2value:
            label.whitelistThreshold = whitelist_id2value[label.extraID]


def set_metadata_labels(input_uri: str, model_metadata: ModelMetadata):
    """
    Update the labels.
    """
    if input_uri is None:
        bcelogger.warning("No postprocess file found")
        return []

    content = yaml.load(open(input_uri, "r"), Loader=yaml.FullLoader)
    assert len(content["outputs"]) > 0, f"No output found in {content}"
    assert "fields_map" in content["outputs"][0], f'Field fields_map not in {content["outputs"][0]}'

    label_names = set()
    output = content["outputs"][0]
    for item in output["fields_map"]:
        model_name = item["model_name"].split("|")[0]
        model_display_name = ""
        if not (model_name in model_metadata.subModels or model_name in model_metadata.extraModels):
            model_display_name = item.get("model_cn_name", "")
        label_index = -1

        if len(item["categories"]) == 0:
            continue
        elif isinstance(item["categories"][0], list):
            for sub_item in item["categories"]:
                label_index = parse_labels(model_labels=sub_item,
                                           model_metadata=model_metadata,
                                           model_name=model_name,
                                           model_display_name=model_display_name,
                                           label_names=label_names,
                                           label_index=label_index)
        elif isinstance(item["categories"][0], dict):
            parse_labels(model_labels=item["categories"],
                         model_metadata=model_metadata,
                         model_name=model_name,
                         model_display_name=model_display_name,
                         label_names=label_names,
                         label_index=label_index)
        else:
            bcelogger.error(f'Model name {item["model_name"]} labels {item["categories"]} is invalid')


def parse_labels(model_labels: List[Dict],
                 model_metadata: ModelMetadata,
                 model_name: str,
                 model_display_name: str,
                 label_names: set,
                 label_index: int):
    """
    Parse the labels.
    """
    parent_name2id = {}

    for label in model_labels:
        bcelogger.info(f'Model {model_name} label: {label}')
        parent_name = None
        parent_id = None

        # label id 处理未int,目前包括遗下几种情况:
        # 1. 数字字符串 "1"
        # 2. 字符串 "che"
        # 3. 带父类的字符串 "安全帽｜0"
        # 4. 整数
        label_id = label["id"]
        if isinstance(label_id, str) and label_id.isdigit():
            label_id = int(label_id)
        elif isinstance(label_id, str) and len(label_id.split("|")) > 1:
            parent_name = label_id.split("|")[0]
            label_id = int(label_id.split("|")[-1])
        elif isinstance(label_id, int):
            label_id = label_id
        else:
            label_index += 1
            label_id = label_index

        # parent id 和 parent name 处理
        if "super_category" in label:
            parent_name = label["super_category"]
        if parent_name is not None:
            if "super_category_id" in label:
                parent_id = label["super_category_id"]
            if parent_id is None:
                if parent_name not in parent_name2id:
                    label_index += 1
                parent_id = label_index
            parent_name2id[parent_name] = parent_id

        # 校验多个模型标签是否有相同的name，有的话过滤
        label_name = label["name"]
        if parent_name is not None and parent_name in label_names:
            continue
        if parent_name is None and label_name in label_names:
            continue

        if parent_id is not None:
            label_instance = Label(id=label_id,
                                   name=label_name,
                                   parentID=parent_id,
                                   modelName=model_name,
                                   modelDisplayName=model_display_name,
                                   extraID=str(label["id"]))
        else:
            label_instance = Label(id=label_id,
                                   name=label_name,
                                   modelName=model_name,
                                   modelDisplayName=model_display_name,
                                   extraID=str(label["id"]))
            label_names.add(label_name)

        model_metadata.labels.append(label_instance)

    for parent_name, parent_id in parent_name2id.items():
        label_names.add(parent_name)
        model_metadata.labels.append(Label(id=parent_id,
                                           name=parent_name,
                                           modelName=model_name,
                                           modelDisplayName=model_display_name))

    return label_index
