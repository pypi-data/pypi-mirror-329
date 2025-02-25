#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/7/19
# @Author  : yanxiaodong
# @File    : graph.py
"""
import copy
from typing import Any, Dict, List
from collections import defaultdict

import bcelogger
from pygraphv1.client.graph_api_graph import EdgeTarget, Edge, GraphContent
from pygraphv1.client.graph_api_operator import Operator
from pygraphv1.client.graph_api_variable import Variable


class Graph:
    """
    Graph class.
    """

    def __init__(self, models: Dict):
        self.models = models
        self.nodes = []
        self.edges = []

    def build_nodes(self, ensemble_steps: Dict):
        """
        Build nodes from steps.
        """
        for name, model in self.models.items():
            assert name in ensemble_steps, f"Model {name} not in steps {ensemble_steps}."
            step = ensemble_steps[name]
            bcelogger.info(f"Building node for model {name}")

            operator = Operator()
            operator.name = step["modelName"]
            operator.local_name = step["modelName"]

            operator.properties = []
            for key, value in model.items():
                variable = self._set_node_property(key, value)
                if variable is not None:
                    bcelogger.info(f"Setting node for model {name} properties for {key}:{value}")
                    operator.properties.append(variable)

            operator.inputs = []
            for key, value in step["inputMap"].items():
                bcelogger.info(f"Setting node for model {name} inputs for {key}:{value}")
                operator.inputs.append((Variable(name=key, type="int")))

            operator.outputs = []
            for key, value in step["outputMap"].items():
                bcelogger.info(f"Setting node for model {name} outputs for {key}:{value}")
                operator.outputs.append((Variable(name=key, type="int")))

            self.nodes.append(operator)

    def build_edges(self, ensemble_steps: Dict):
        """
        Build edges from steps.
        """
        inputs = defaultdict(list)
        outputs = defaultdict(dict)
        for name, step in ensemble_steps.items():
            new_step = copy.deepcopy(step)
            for key, value in step["inputMap"].items():
                new_step["inputMap"][value] = key
                inputs[value].append(new_step)
            for key, value in step["outputMap"].items():
                outputs[value] = new_step

        for key, output in outputs.items():
            if key not in inputs:
                bcelogger.info(f"It's the last node, no input for {key}")

            for input_ in inputs[key]:
                edge = Edge()
                bcelogger.info(f'Setting edge output for {output["modelName"]}:{key}')
                edge.from_ = EdgeTarget(operator=output["modelName"], output=key)
                bcelogger.info(f'Setting edge input for {input_["modelName"]}:{input_["inputMap"][key]}')
                edge.to = EdgeTarget(operator=input_["modelName"], input=input_["inputMap"][key])
                self.edges.append(edge)

    def _set_node_property(self, name: str, value: Any):
        if isinstance(value, str):
            variable = Variable(name=name, type="string", value=value, option="false", readonly="false")
            return variable

        if isinstance(value, List):
            variable = Variable(name=name, type="object", option="false", readonly="false", schema=[])
            for v in value:
                index = 1
                if isinstance(v, str):
                    variable.schema_.append(Variable(name=name + "_" + str(index),
                                                     type="string",
                                                     value=v,
                                                     option="false",
                                                     readonly="false"))
            return variable

        return

    def build(self, name: str, local_name: str, ensemble_steps: Dict):
        """
        __call__ method.
        """
        self.build_nodes(ensemble_steps)
        self.build_edges(ensemble_steps)

        graph_content = GraphContent()
        graph_content.name = name
        graph_content.local_name = local_name
        graph_content.nodes = self.nodes
        graph_content.edges = self.edges

        return graph_content
