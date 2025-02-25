#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2023/9/25
# @Author  : yanxiaodong
# @File    : model_api_modelstore.py
"""
import re
from typing import Optional
from pydantic import BaseModel

modelstore_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/modelstores/(?P<local_name>.+?)$"
)


class ModelStoreName(BaseModel):
    """
    The name of model.
    """

    workspace_id: str
    local_name: str

    def get_name(self):
        """
        get name
        :return:
        """
        return f"workspaces/{self.workspace_id}/modelstores/{self.local_name}"


def parse_modelstore_name(name: str) -> Optional[ModelStoreName]:
    """
    Get ModelStoreName
    """
    m = modelstore_name_regex.match(name)
    if m is None:
        return None
    return ModelStoreName(
        workspace_id=m.group("workspace_id"),
        local_name=m.group("local_name"),
    )
