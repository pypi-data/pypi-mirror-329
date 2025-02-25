#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/21 15:58
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : model_client.py
# @Software: PyCharm
"""
import json
import os
import shutil
from typing import Optional, Dict

import bcelogger
import yaml
from baidubce.http import http_content_types
from baidubce.http import http_methods
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from bceinternalsdk.client.paging import PagingRequest
from tritonv2.bls_parser import GaeaBLSParser
from tritonv2.model_config import ModelConfig
from windmillartifactv1.client.artifact_api_artifact import (
    LocationStyle,
    get_location_path,
    parse_artifact_name,
    Alias,
)
from windmillartifactv1.client.artifact_client import ArtifactClient
from windmillcategoryv1.client.category_api import match
from windmillcomputev1.client.compute_client import ComputeClient
from windmillcomputev1.filesystem import download_by_filesystem
from windmillmodelv1.graph.graph import Graph

from .model_api_model import Category, ModelName, parse_model_name
from .model_api_modelstore import ModelStoreName


def write_apply_yaml(apply_list, sep, output_path):
    """
    write apply yaml file
    Args:
        apply_list: apply list
        sep: separator 分隔符
        output_path: output path
    """
    with open(output_path, "w") as f:
        for idx, item in enumerate(apply_list):
            yaml.dump(item, f, default_flow_style=False)

            if idx < len(apply_list) - 1:
                f.write(sep)


class ModelClient(BceInternalClient):
    """
    A client class for interacting with the model service. Initializes with default configuration.

    This client provides an interface to interact with the model&model store service using BCE (Baidu Cloud Engine) API.
    It supports operations related to creating and retrieving artifacts within a specified workspace.
    """

    """
        model store api
    """

    def create_model_store(
        self,
        workspace_id: str,
        local_name: str,
        filesystem: str,
        display_name: Optional[str] = "",
        description: Optional[str] = "",
    ):
        """
        Creates a model store in the system.

        Args:
            workspace_id (str): 工作区 id
            local_name (str): 系统名称
            filesystem (str): 存储资源名称
            display_name (str, optional): 模型仓库名称
            description (str, optional): 模型仓库描述
        Returns:
            HTTP request response
        """
        body = {
            "workspaceID": workspace_id,
            "localName": local_name,
            "fileSystemName": filesystem,
            "displayName": display_name,
            "description": description,
        }

        return self._send_request(
            http_method=http_methods.POST,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/" + workspace_id + "/modelstores", encoding="utf-8"
            ),
            body=json.dumps(body),
        )

    def list_model_store(
        self,
        workspace_id: str,
        filter_param: Optional[str] = "",
        page_request: Optional[PagingRequest] = PagingRequest(),
    ):
        """
        Lists model stores in the system.
        Args:
            workspace_id (str): 工作区 id
            filter_param (str, optional): 搜索条件，支持系统名称、模型名称、描述。
            page_request (PagingRequest, optional): 分页请求配置。默认为 PagingRequest()。

        Returns:
            HTTP request response
        """
        params = {
            "filter": filter_param,
            "pageNo": str(page_request.get_page_no()),
            "pageSize": str(page_request.get_page_size()),
            "order": page_request.order,
            "orderBy": page_request.orderby,
        }
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/" + workspace_id + "/modelstores", encoding="utf-8"
            ),
            params=params,
        )

    def get_model_store(self, workspace_id: str, local_name: str):
        """
        Retrieves model store information.

        Args:
            workspace_id (str): 工作区 id
            local_name (str): 系统名称

        Returns:
            HTTP request response
        """
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/" + workspace_id + "/modelstores/" + local_name,
                encoding="utf-8",
            ),
        )

    def update_model_store(
        self,
        workspace_id: str,
        local_name: str,
        display_name: Optional[str] = "",
        description: Optional[str] = "",
    ):
        """
        Updates model store information.

        Args:
            workspace_id (str): 工作区 id
            local_name (str): 系统名称
            display_name (str, optional): 模型仓库名称
            description (str, optional): 模型仓库描述

        Returns:
            HTTP request response
        """
        body = {
            "workspaceID": workspace_id,
            "modelStoreName": local_name,
            "displayName": display_name,
            "description": description,
        }

        return self._send_request(
            http_method=http_methods.PUT,
            path=bytes(
                "/v1/workspaces/" + workspace_id + "/modelstores/" + local_name,
                encoding="utf-8",
            ),
            body=json.dumps(body),
        )

    def delete_model_store(self, workspace_id: str, local_name: str):
        """
        Deletes a model store from the system.

        Args:
            workspace_id (str): 工作区 id
            local_name (str): 系统名称

        Returns:
            HTTP request response
        """
        return self._send_request(
            http_method=http_methods.DELETE,
            path=bytes(
                "/v1/workspaces/" + workspace_id + "/modelstores/" + local_name,
                encoding="utf-8",
            ),
        )

    def import_model(
        self,
        workspace_id: str,
        local_name: str,
        spec_uri: str,
        source_uri: str,
        source_filesystem: dict,
        spec_kind: Optional[str] = "PaddleFlow",
    ):
        """
        import model from remote filesystem and deploy model

        Args:
            workspace_id (str): 工作区 id
            local_name (str): 系统名称
            spec_uri (str): 导入模型使用的 pipeline 文件路径, e.g. "file:///root/pipelines/model/arm/import_model_k8s.yaml"
            source_uri (str): 模型文件下载地址, e.g. "s3://workspaces/ws01/jobs/job1/model.tar"
            source_filesystem (dict): 源 filesystem 信息
            spec_kind (str, optional): 导入模型使用的 pipeline 作业类型,
                支持 Local, PaddleFlow, Argo, Ray, Kube，默认为 PaddleFlow


        Returns:
            HTTP request response
        """
        body = {
            "workspaceID": workspace_id,
            "modelStoreName": local_name,
            "specURI": spec_uri,
            "specKind": spec_kind,
            "sourceURI": source_uri,
            "sourceFileSystem": source_filesystem,
        }

        return self._send_request(
            http_method=http_methods.POST,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/modelstores/"
                + local_name
                + "/models/import",
                encoding="utf-8",
            ),
            body=json.dumps(body),
        )

    """
    model api
    """

    def create_model(
        self,
        workspace_id: str,
        model_store_name: str,
        local_name: str,
        category: str,
        model_formats: list,
        display_name: Optional[str] = "",
        description: Optional[str] = "",
        schema_uri: Optional[str] = "",
        artifact_uri: Optional[str] = "",
        artifact_description: Optional[str] = "",
        prefer_model_server_parameters: Optional[dict] = None,
        artifact_alias: Optional[list] = None,
        artifact_metadata: Optional[str] = None,
        artifact_tags: Optional[dict] = None,
        style: Optional[LocationStyle] = LocationStyle.DEFAULT.value,
        source_filesystem: Optional[dict] = None,
    ):
        """
        创建模型。

        Args:
            workspace_id (str): 工作区 id，例如："ws01"。
            model_store_name (str): 模型仓库名称，例如："ms01"。
            local_name (str): 系统名称，例如："model01"。
            category (str): 模型类别，例如："Image/OCR"。
            model_formats (list): 模型文件框架类型，例如：["PaddlePaddle"]。
            display_name (str, optional): 模型名称，例如："模型01"。
            description (str, optional): 模型描述，例如："模型描述"。
            schema_uri (str, optional): 模型对应的预测服务的接口文档地址。
            artifact_uri (str, optional): 版本文件路径。
            artifact_description (str, optional): 版本描述。
            artifact_alias (list, optional): 版本别名，例如 ["default"]。
            artifact_metadata (str, optional): 版本基本信息。
            artifact_tags (dict, optional): 版本标签。
            style: (LocationStyle): 上传的文件路径风格，默认为 Default。
            prefer_model_server_parameters: (dict, optional): 模型服务参数。
            source_filesystem (dict, optional): 模型包文件源存储位置的 filesystem 信息。

        Returns:
            HTTP request response
        """
        object_name = ModelName(
            workspace_id=workspace_id,
            model_store_name=model_store_name,
            local_name=local_name,
        ).get_name()
        if artifact_uri != "":
            artifact_uri = ArtifactClient(
                self.config, context=self.context
            ).create_location_with_uri(
                uri=artifact_uri,
                object_name=object_name,
                style=style,
                source_filesystem=source_filesystem,
            )

        body = {
            "workspaceID": workspace_id,
            "modelStoreName": model_store_name,
            "localName": local_name,
            "displayName": display_name,
            "description": description,
            "category": category,
            "modelFormats": model_formats,
            "schemaUri": schema_uri,
            "artifact": {
                "uri": artifact_uri,
                "description": artifact_description,
                "alias": artifact_alias,
                "tags": artifact_tags,
                "metadata": artifact_metadata,
            },
            "preferModelServerParameters": prefer_model_server_parameters,
        }
        return self._send_request(
            http_method=http_methods.POST,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/modelstores/"
                + model_store_name
                + "/models",
                encoding="utf-8",
            ),
            body=json.dumps(body),
        )

    def list_model(
        self,
        workspace_id: str,
        model_store_name: str,
        names: Optional[list] = None,
        categories: Optional[list] = None,
        model_formats: Optional[list] = None,
        tags: Optional[list] = None,
        filter_param: Optional[str] = "",
        page_request: Optional[PagingRequest] = PagingRequest(),
    ):
        """

        Lists models in the system.

        Args:
            workspace_id (str): 工作区 id
            model_store_name (str): 模型仓库名称
            names: 模型名称列表, 例如：["model01", "model02"]
            categories (list, optional): 按模型类别筛选模型 例如: ["Image/OCR"]
            model_formats (list, optional): 按模型文件框架类型筛选模型 例如: ["PaddlePaddle"]
            tags (list, optional): 按模型版本标签筛选模型 例如: [{key1:value1}, {key2:value2}]
            filter_param (str, optional): 搜索条件，支持系统名称、模型名称、描述。
            page_request (PagingRequest, optional): 分页请求配置。默认为 PagingRequest()。
        Returns:
            HTTP request response
        """
        params = {
            "pageNo": page_request.get_page_no(),
            "pageSize": page_request.get_page_size(),
            "order": page_request.order,
            "orderBy": page_request.orderby,
            "modelFormats": model_formats,
            "filter": filter_param,
        }
        if names:
            params["names"] = names
        if categories:
            params["categories"] = categories
        if tags:
            params["tags"] = tags
        return self._send_request(
            http_method=http_methods.GET,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/modelstores/"
                + model_store_name
                + "/models",
                encoding="utf-8",
            ),
            body=json.dumps(params),
        )

    def get_model(self, workspace_id: str, model_store_name: str, local_name: str):
        """
        Retrieves model information.

        Args:
            local_name (str): 系统名称，例如："model01"
            model_store_name (str): 模型仓库名称，例如："ms01"
            workspace_id (str): 工作区 id，例如："ws01"
        Returns:
            HTTP request response
        """
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/modelstores/"
                + model_store_name
                + "/models/"
                + local_name,
                encoding="utf-8",
            ),
        )

    def get_model_manifest(
        self, workspace_id: str, model_store_name: str, local_name: str, version: str
    ):
        """
        Retrieves model manifest information.

        Args:
            local_name (str): 系统名称，例如："model01"
            model_store_name (str): 模型仓库名称，例如："ms01"
            workspace_id (str): 工作区 id，例如："ws01"
            version: 版本号，例如："1"
        Returns:
            HTTP request response
        """
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/modelstores/"
                + model_store_name
                + "/models/"
                + local_name
                + "/versions/"
                + version
                + "/manifest",
                encoding="utf-8",
            ),
        )

    def update_model(
        self,
        workspace_id: str,
        model_store_name: str,
        local_name: str,
        category: str,
        display_name: Optional[str] = "",
        description: Optional[str] = "",
        model_formats: Optional[str] = "",
        schema_uri: Optional[str] = "",
        prefer_model_server_parameters: Optional[dict] = None,
    ):
        """
        Updates model information.

        Args:
            workspace_id (str): 工作区 id
            model_store_name (str): 模型仓库名称
            local_name (str): 系统名称
            display_name (str, optional): 模型名称，例如："模型01"
            description (str, optional): 模型描述，例如："model description"
            category (str, optional): 模型类别，例如："Image/OCR"
            model_formats (str, optional): 模型文件框架类型，例如："[PaddlePaddle]"
            schema_uri (str, optional): 模型对应的预测服务的接口文档地址

        Returns:
            HTTP request response
        """
        body = {
            key: value
            for key, value in {
                "displayName": display_name,
                "description": description,
                "category": category,
                "modelFormats": model_formats,
                "workspaceID": workspace_id,
                "modelStoreName": model_store_name,
                "localName": local_name,
                "schemaUri": schema_uri,
                "preferModelServerParameters": prefer_model_server_parameters,
            }.items()
            if value is not None and value != ""
        }

        return self._send_request(
            http_method=http_methods.PUT,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/modelstores/"
                + model_store_name
                + "/models/"
                + local_name,
                encoding="utf-8",
            ),
            body=json.dumps(body),
        )

    def delete_model(self, workspace_id: str, model_store_name: str, local_name: str):
        """
        Deletes a model from the system.

        Args:
            workspace_id (str): 工作区 id
            model_store_name (str): 模型仓库名称
            local_name (str): 系统名称
        Returns:
            HTTP request response
        """
        return self._send_request(
            http_method=http_methods.DELETE,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/modelstores/"
                + model_store_name
                + "/models/"
                + local_name,
                encoding="utf-8",
            ),
        )

    def dump_models(
        self,
        artifact_name: str,
        location_style: str = "Triton",
        rename: str = None,
        output_uri: str = ".",
        only_generate_structure: bool = False,
    ):
        """
        dump models from windmill(main function)
        Args:
            artifact_name: artifact_name，例如："workspaces/ws-1/modelstores/default/pipelines/default/versions/1"
            location_style: location style, default is "Triton"
            rename: rename file name. change files to specified name. default is None
            output_uri: model output file path
            only_generate_structure: only generate model structure, default is False
        """
        # 1. 获取model dump列表文件
        # a. 解析artifact_name，获取workspace_id, model_store_name, model_name, version
        artifact_name = parse_artifact_name(artifact_name)
        model_name = parse_model_name(artifact_name.object_name)

        # b.  获取model manifest 列表文件
        manifest_list = self.get_model_manifest(
            model_name.workspace_id,
            model_name.model_store_name,
            model_name.local_name,
            artifact_name.version,
        )

        # 2. 准备下载模型文件
        # a. 获取 suggest fs 实例化bs
        model_store_name = ModelStoreName(
            workspace_id=model_name.workspace_id, local_name=model_name.model_store_name
        )
        compute_client = ComputeClient(self.config, context=self.context)
        filesystem = compute_client.suggest_first_filesystem(
            model_name.workspace_id, model_store_name.get_name()
        )

        # b. 遍历manifest_list result，下载模型文件
        apply_models = []
        ensemble = None
        for item in manifest_list.subModels:
            new_local_name = None
            if rename and item["name"] == model_name.get_name():
                new_local_name = rename

            if not only_generate_structure:
                self._dump_model(
                    filesystem, item, location_style, new_local_name, output_uri
                )

            if isinstance(item.get("category"), dict):
                item["category"] = item["category"].get("category")

            if match(item["category"], Category.CategoryImageEnsemble.value):
                ensemble = {"kind": "Model", "metadata": item}
                continue
            apply_models.append({"kind": "Model", "metadata": item})

        apply_models.append(ensemble)

        output_path = os.path.join(output_uri, "apply.yaml")
        write_apply_yaml(apply_models, "---\n", output_path)

    def build_graph(
        self,
        ensemble_name: str,
        sub_models: Dict,
        extra_models: Dict,
        input_uri: str = "/home/windmill/tmp/model",
    ):
        """ """
        # 1. 下载ensemble model
        ensemble_model = parse_model_name(
            parse_artifact_name(name=ensemble_name).object_name
        )
        ensemble_output_uri = os.path.join(input_uri, ensemble_model.local_name)
        artifact_client = ArtifactClient(self.config, context=self.context)
        artifact_client.download_artifact(
            name=ensemble_name, output_uri=ensemble_output_uri
        )

        # 2. 获取ensemble config
        ensemble_config = ModelConfig.create_from_file(
            model_config_filepath=os.path.join(ensemble_output_uri, "config.pbtxt")
        )

        # 3. 解析 scheduling step
        ensemble_steps = {}
        sub_models.update(extra_models)
        bcelogger.info(f"Sub models is {sub_models}")
        for name, step in ensemble_config.get_ensemble_steps().items():
            bcelogger.info(f"Parsing step {name} is {step}")
            ensemble_steps[name] = step
            sub_models[name] = sub_models.get(name, "latest")
            bcelogger.info(f"Model name {name} version {sub_models[name]}")

        # 4. 解析bls节点
        bls_parse = GaeaBLSParser(
            artifact_client,
            workspace_id=ensemble_model.workspace_id,
            model_store_name=ensemble_model.model_store_name,
            input_uri=input_uri,
        )
        for name, _ in ensemble_config.get_ensemble_steps().items():
            object_name = ModelName(
                workspace_id=ensemble_model.workspace_id,
                model_store_name=ensemble_model.model_store_name,
                local_name=name,
            ).get_name()
            model_output_uri = os.path.join(input_uri, name)
            bcelogger.info(
                f"Downloading model:{object_name} version:{sub_models[name]} to {model_output_uri}"
            )
            artifact_client.download_artifact(
                object_name=object_name,
                version=sub_models[name],
                output_uri=model_output_uri,
            )
            bls_parse(
                model_name=name,
                model_uri=model_output_uri,
                ensemble_steps=ensemble_steps,
                sub_models=sub_models,
            )

        # 5. 获取 models
        models = {}
        for name, step in ensemble_steps.items():
            bcelogger.info(f"Parsing step {name} is {step}")

            response = self.get_model(
                workspace_id=ensemble_model.workspace_id,
                model_store_name=ensemble_model.model_store_name,
                local_name=name,
            )

            response = json.loads(response.raw_data)
            response["version"] = (
                sub_models[name]
                if sub_models[name] != "latest"
                else str(response["artifact"]["version"])
            )
            response["category"] = response["category"]["category"]
            models[name] = response

        # 6. 构建graph
        graph = Graph(models=models)
        graph_content = graph.build(
            name=ensemble_name,
            local_name=ensemble_model.local_name,
            ensemble_steps=ensemble_steps,
        )

        return graph_content

    def _dump_model(
        self,
        filesystem,
        model,
        location_style: str,
        rename: str = None,
        output_uri: str = ".",
    ):
        """
        dump model
        Args:
            filesystem: file system instance
            model(dict): model info
            location_style: location style, default is "Triton"
            output_uri: model output file path

        Returns
            apply_obj: apply object
        """
        # 1. 获取model dump列表文件
        if rename:
            output_uri = output_uri.rstrip("/") + "/" + rename
        else:
            output_uri = output_uri.rstrip("/") + "/" + model["localName"]

        output_uri = get_location_path(
            output_uri, location_style, str(model["artifact"]["version"])
        )
        if not os.path.exists(output_uri):
            os.makedirs(output_uri)

        # 2. 下载模型文件
        download_by_filesystem(filesystem, model["artifact"]["uri"], output_uri)

        # 3. 调整模型文件
        for file_name in os.listdir(output_uri):
            src_path = output_uri + "/" + file_name
            if os.path.isdir(src_path):
                continue

            if (
                file_name.endswith(".yaml")
                or file_name.endswith(".yml")
                or file_name.endswith(".pbtxt")
            ):
                dest_path = os.path.abspath(output_uri + "/../" + file_name)
                shutil.copyfile(src_path, dest_path)

        # 4. 读取 artifact.yaml 文件内容 生成创建模型输入
        with open(output_uri + "/artifact.yaml", "r") as file:
            data = yaml.safe_load(file)

        model["category"] = model["category"]["category"]
        model["artifact"] = data
        model["artifact"]["uri"] = output_uri

        if match(model["category"], Category.CategoryImageEnsemble.value):
            update_model_metadata(model["artifact"]["metadata"])


def update_model_metadata(model_metadata):
    """
    更新模型元数据
    Args:
        model_metadata: 元数据信息
    """
    # 1. 调整 extraModels 为空
    if (
        model_metadata.get("extraModels") is not None
        and len(model_metadata.get("extraModels")) != 0
    ):
        for key, _ in model_metadata["extraModels"].items():
            model_metadata["extraModels"][key] = Alias.LATEST.value

    # 2. 设置 subModels 为空
    model_metadata["subModels"] = {}
