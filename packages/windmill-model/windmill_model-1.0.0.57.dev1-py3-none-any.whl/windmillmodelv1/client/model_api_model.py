#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/29
# @Author  : yanxiaodong
# @File    : model_api_model.py
"""
import re
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from pygraphv1.client.graph_api_graph import GraphContent

model_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/modelstores/(?P<model_store_name>.+?)/models/(?P<local_name>.+?)$"
)


class Category(Enum):
    """
    Model Category
    """
    CategoryImageOCR = "Image/OCR"
    CategoryImageClassificationMultiClass = "Image/ImageClassification/MultiClass"
    CategoryImageClassificationMultiTask = "Image/ImageClassification/MultiTask"
    CategoryImageObjectDetection = "Image/ObjectDetection"
    CategoryImageSemanticSegmentation = "Image/SemanticSegmentation"
    CategoryImageInstanceSegmentation = "Image/InstanceSegmentation"
    CategoryImageKeypointDetection = "Image/KeypointDetection"
    CategoryImageChangeDetectionInstanceSegmentation = "Image/ChangeDetection/InstanceSegmentation"
    CategoryImageChangeDetectionObjectDetection = "Image/ChangeDetection/ObjectDetection"
    CategoryImageChangeDetectionSemanticSegmentation = "Image/ChangeDetection/SemanticSegmentation"
    CategoryImageAnomalyDetection = "Image/AnomalyDetection"
    CategoryImageObjectTracking = "Image/ObjectTracking"

    CategoryImageEnsemble = "Image/Ensemble"
    CategoryImagePreprocess = "Image/Preprocess"
    CategoryImagePostprocess = "Image/Postprocess"

    CategoryMultimodal = "Multimodal"
    CategoryNLPTextGeneration = "NLP/TextGeneration"
    CategoryNLPQuestionAnswering = "NLP/QuestionAnswering"


class ModelName(BaseModel):
    """
    The name of model.
    """

    workspace_id: str
    model_store_name: str
    local_name: str

    class Config:
        """
        命名空间配置
        : 避免命名空间冲突
        """
        protected_namespaces = []

    def get_name(self):
        """
        get name
        :return:
        """
        return f"workspaces/{self.workspace_id}/modelstores/{self.model_store_name}/models/{self.local_name}"


class Label(BaseModel):
    """
    The label of model.
    """

    id: Optional[int] = None
    extraID: Optional[str] = None
    name: Optional[str] = None
    displayName: Optional[str] = None
    parentID: Optional[int] = None
    modelName: Optional[str] = None
    modelDisplayName: Optional[str] = None
    threshold: Optional[float] = None
    whitelistThreshold: Optional[float] = None


class InputSize(BaseModel):
    """
    The size of input.
    """

    width: Optional[int] = None
    height: Optional[int] = None


class ModelMetadata(BaseModel):
    """
    The metadata of model.
    """

    experimentName: Optional[str] = None
    experimentRunID: Optional[str] = None
    jobName: Optional[str] = None
    jobDisplayName: Optional[str] = None
    labels: Optional[List[Label]] = None
    algorithmParameters: Optional[Dict[str, str]] = None
    maxBoxNum: Optional[int] = None
    inputSize: Optional[InputSize] = None
    subModels: Optional[Dict[str, str]] = None
    extraModels: Optional[Dict[str, str]] = None
    inferConfig: Optional[Any] = None
    modelConfig: Optional[Any] = None
    graphContent: Optional[GraphContent] = None


class ResourceList(BaseModel):
    """
    Resource list.
    """
    cpu: Optional[str] = ""
    mem: Optional[str] = ""


class Resource(BaseModel):
    """
    Resource.
    """
    accelerator: Optional[str] = ""
    gpu: Optional[str] = ""
    limits: Optional[ResourceList] = None
    requests: Optional[ResourceList] = None


class PreferModelServerParameters(BaseModel):
    """
    Model server parameters.
    """

    image: Optional[str] = None  # 模型服务镜像
    env: Optional[Dict[str, str]] = None  # 模型服务环境变量 {"key1": "value1"}
    args: Optional[Dict[str, str]] = None  # 模型服务推理参数 {"backend-config": "tensorrt,plugins=/opt/xxx.so"}
    resource: Optional[Resource] = None  # 模型服务资源配置
    qps: Optional[float] = 0.0  # 模型推理每秒请求数


class InferParameter(BaseModel):
    """
    Parameter.
    """
    name: Optional[str] = None
    nameCN: Optional[str] = None
    labelName: Optional[str] = None
    namespace: Optional[str] = None
    default: Optional[float] = None
    range: Optional[str] = None
    type: Optional[str] = None
    step: Optional[float] = None
    description: Optional[str] = None


class InferParameters(BaseModel):
    """
    Inference parameters.
    """

    modelName: Optional[str] = None
    modelDisplayName: Optional[str] = None
    isTrack: Optional[bool] = None
    parameters: Optional[List[InferParameter]] = None


def parse_model_name(name: str) -> Optional[ModelName]:
    """
    Get ModelName。
    """
    m = model_name_regex.match(name)
    if m is None:
        return None
    return ModelName(
        workspace_id=m.group("workspace_id"),
        model_store_name=m.group("model_store_name"),
        local_name=m.group("local_name"),
    )
