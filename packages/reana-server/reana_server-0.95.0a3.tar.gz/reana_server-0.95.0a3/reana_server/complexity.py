# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2021, 2022 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REANA workflow complexity estimation."""

from typing import Dict, List, Tuple

from reana_commons.job_utils import kubernetes_memory_to_bytes
from reana_commons.errors import REANAKubernetesMemoryLimitExceeded

from reana_server.config import (
    REANA_KUBERNETES_JOBS_MEMORY_LIMIT,
    REANA_KUBERNETES_JOBS_MAX_USER_MEMORY_LIMIT,
    REANA_KUBERNETES_JOBS_MAX_USER_MEMORY_LIMIT_IN_BYTES,
)


def validate_job_memory_limits(complexity: List[Tuple[int, float]]) -> None:
    """Validate that job memory limits does not exceed the maximum memory limit that users can assign to their job containers.

    :param complexity: workflow complexity list which consists of number of initial jobs and the memory in bytes they require. (e.g. [(8, 1073741824), (5, 2147483648)])
    :raises REANAKubernetesMemoryLimitExceeded: If workflow job memory limits exceed the maximum memory limit that users can assign to their job containers.
    """
    if not complexity:
        return None
    max_job_memory = max(complexity, key=lambda x: x[1])[1]

    if (
        REANA_KUBERNETES_JOBS_MAX_USER_MEMORY_LIMIT_IN_BYTES
        and max_job_memory > REANA_KUBERNETES_JOBS_MAX_USER_MEMORY_LIMIT_IN_BYTES
    ):
        raise REANAKubernetesMemoryLimitExceeded(
            f'The "kubernetes_memory_limit" provided in the workflow exceeds the limit ({REANA_KUBERNETES_JOBS_MAX_USER_MEMORY_LIMIT}).'
        )
    return None


def get_workflow_min_job_memory(complexity):
    """Return minimal job memory from workflow complexity.

    :param complexity: workflow complexity list which consists of number of initial jobs and the memory in bytes they require. (e.g. [(8, 1073741824), (5, 2147483648)])
    :return: minimal job memory (e.g. 1073741824)
    """
    if not complexity:
        return 0
    return min(complexity, key=lambda x: x[1])[1]


def estimate_complexity(workflow_type, reana_yaml):
    """Estimate complexity in REANA workflow.

    :param workflow_type: A supported workflow specification type.
    :param reana_yaml: REANA YAML specification.
    """

    def build_estimator(workflow_type, reana_yaml):
        if workflow_type == "serial":
            return SerialComplexityEstimator(reana_yaml)
        elif workflow_type == "yadage":
            return YadageComplexityEstimator(reana_yaml)
        elif workflow_type == "cwl":
            return CWLComplexityEstimator(reana_yaml)
        elif workflow_type == "snakemake":
            return SnakemakeComplexityEstimator(reana_yaml)
        else:
            raise Exception(
                "Workflow type '{0}' is not supported".format(workflow_type)
            )

    estimator = build_estimator(workflow_type, reana_yaml)
    try:
        complexity = estimator.estimate_complexity()
    except Exception:
        return []
    return complexity


class ComplexityEstimatorBase:
    """REANA workflow complexity estimator base class."""

    def __init__(self, reana_yaml):
        """Estimate complexity in REANA workflow.

        :param reana_yaml: REANA YAML specification.
        :param initial_step: initial workflow execution step.
        """
        self.reana_yaml = reana_yaml
        self.specification = reana_yaml.get("workflow", {}).get("specification", {})
        self.input_params = reana_yaml.get("inputs", {}).get("parameters", {})

    def parse_specification(self, initial_step):
        """Parse REANA workflow specification tree."""
        raise NotImplementedError

    def estimate_complexity(self, initial_step="init"):
        """Estimate complexity in parsed REANA workflow tree."""
        steps = self.parse_specification(initial_step)
        return self._calculate_complexity(steps)

    def _calculate_complexity(self, steps):
        """Calculate complexity in parsed REANA workflow tree."""
        complexity = []
        for step in steps.values():
            complexity += step["complexity"]
        return complexity

    def _get_number_of_jobs(self, step):
        """Get number of jobs based on compute backend."""
        backend = step.get("compute_backend")
        if backend and backend != "kubernetes":
            return 0
        return 1

    def _get_memory_limit(self, step):
        """Get memory limit value."""
        memory_limit = (
            step.get("kubernetes_memory_limit") or REANA_KUBERNETES_JOBS_MEMORY_LIMIT
        )
        return kubernetes_memory_to_bytes(memory_limit)


class SerialComplexityEstimator(ComplexityEstimatorBase):
    """REANA serial workflow complexity estimation."""

    def _parse_steps(self, steps):
        """Parse serial workflow specification tree."""
        tree = []
        for idx, step in enumerate(steps):
            name = step.get("name", str(idx))
            jobs = self._get_number_of_jobs(step)
            memory_limit = self._get_memory_limit(step)
            complexity = [(jobs, memory_limit)]
            tree.append({name: {"complexity": complexity}})
        return tree

    def parse_specification(self, initial_step):
        """Parse and filter out serial workflow specification tree."""
        spec_steps = self.specification.get("steps", [])
        steps = self._parse_steps(spec_steps)
        if initial_step == "init":
            return steps[0] if steps else {}
        return next(filter(lambda step: initial_step in step.keys(), steps), {})


class YadageComplexityEstimator(ComplexityEstimatorBase):
    """REANA Yadage workflow complexity estimation."""

    def _parse_steps(self, stages, initial_step):
        """Parse and filter out Yadage workflow tree."""

        def _is_initial_stage(stage):
            dependencies = stage.get("dependencies", {}).get("expressions", [])

            if dependencies == [initial_step]:
                return True

            if initial_step == "init":
                # Not defined dependencies should be treated as `init`
                return not dependencies
            return False

        def _get_stage_complexity(stage):
            resources = (
                stage.get("scheduler", {})
                .get("step", {})
                .get("environment", {})
                .get("resources", [])
            )
            compute_backend = next(
                filter(
                    lambda r: isinstance(r, dict) and "compute_backend" in r.keys(),
                    resources,
                ),
                {},
            )
            k8s_memory_limit = next(
                filter(
                    lambda r: isinstance(r, dict)
                    and "kubernetes_memory_limit" in r.keys(),
                    resources,
                ),
                {},
            )
            jobs = self._get_number_of_jobs(compute_backend)
            memory_limit = self._get_memory_limit(k8s_memory_limit)
            return [(jobs, memory_limit)]

        def _parse_stages(stages):
            tree = {}
            for stage in stages:
                if not _is_initial_stage(stage):
                    continue
                name = stage["name"]
                scheduler = stage.get("scheduler", {})
                parameters = scheduler.get("parameters", [])
                tree[name] = {"params": parameters, "stages": {}, "scatter_params": []}

                # Parse stage complexity
                tree[name]["complexity"] = _get_stage_complexity(stage)

                # Parse nested stages
                if "workflow" in scheduler:
                    nested_stages = scheduler["workflow"].get("stages", [])
                    parsed_stages = _parse_stages(nested_stages)
                    tree[name]["stages"].update(parsed_stages)

                # Parse scatter parameters
                if "scatter" in scheduler and scheduler["scatter"]["method"] == "zip":
                    tree[name]["scatter_params"] = scheduler["scatter"]["parameters"]

            return tree

        return _parse_stages(stages)

    def _populate_parameters(self, stages, parent_params):
        """Populate parsed Yadage workflow tree with parameter values."""

        def _parse_params(stage, parent_params):
            parent_params = parent_params.copy()
            for param in stage["params"]:
                if isinstance(param["value"], list):
                    parent_params[param["key"]] = param["value"]
                elif isinstance(param["value"], dict):
                    # Example: input_file: {step: init, output: files}
                    # In this case `files` values should be taken from
                    # `parent_params` and saved as `input_file`
                    output = param["value"].get("output", "")
                    parent_value = parent_params.get(output, "")
                    parent_params[param["key"]] = parent_value
                else:
                    parent_params[param["key"]] = [param["value"]]
            return parent_params

        def _parse_stages(stages, parent_params):
            stages = stages.copy()
            for stage in stages.keys():
                stage_value = stages[stage]
                # Handle params
                params = _parse_params(stage_value, parent_params)
                stage_value["params"] = params
                # Handle nested stages
                stage_value["stages"] = _parse_stages(stage_value["stages"], params)
            return stages

        return _parse_stages(stages, parent_params)

    def _populate_complexity(self, stages):
        """Calculate number of jobs and memory needed for the parsed Yadage workflow tree."""

        def _parse_stages(stages):
            stages = stages.copy()
            for stage in stages.keys():
                stage_value = stages[stage]
                complexity = stage_value["complexity"]

                # Handle nested stages
                parsed_stages = _parse_stages(stage_value["stages"])
                stage_value["stages"] = parsed_stages
                if parsed_stages:
                    complexity = self._calculate_complexity(parsed_stages)

                # Handle scatter parameters
                if stage_value["scatter_params"]:
                    first_param = stage_value["scatter_params"][0]
                    param_len = len(stage_value["params"].get(first_param, []))
                    complexity = [(item[0] * param_len, item[1]) for item in complexity]

                stage_value["complexity"] = complexity
            return stages

        return _parse_stages(stages)

    def parse_specification(self, initial_step):
        """Parse Yadage workflow specification tree."""
        steps = self._parse_steps(self.specification["stages"], initial_step)
        steps = self._populate_parameters(steps, self.input_params)
        steps = self._populate_complexity(steps)
        return steps


class CWLComplexityEstimator(ComplexityEstimatorBase):
    """REANA CWL workflow complexity estimation."""

    def _parse_steps(self, workflow):
        """Parse CWL workflow specification tree."""
        tree = {}
        steps = workflow.get("steps", [])
        wid = workflow.get("id")
        for step in steps:
            name = step.get("id")
            run = step.get("run")
            hints = step.get("hints", [{}]).pop()
            # Parse scatter params
            scatter = step.get("scatter")
            scatter_params = None
            if scatter:
                scatter_params = (
                    next(
                        filter(lambda p: p["id"] == scatter, step.get("in", [])),
                        {},
                    )
                    .get("source")
                    .split("/")
                    .pop()
                )
            # Parse nested workflows
            nested_workflow = self._parse_steps(run) if isinstance(run, dict) else None
            # Parse initial complexity
            jobs = self._get_number_of_jobs(hints)
            memory_limit = self._get_memory_limit(hints)
            complexity = [(jobs, memory_limit)]
            # Parse params and dependencies
            params = list(map(lambda i: i.get("source", ""), step.get("in", [])))
            dependencies = set()
            for param in params:
                # Extract dependencies from param (e.g '#main/gendata/data')
                if param:
                    dependencies.update(param.replace(wid + "/", "").split("/")[0:-1])

            tree[name] = {
                "complexity": complexity,
                "params": params,
                "dependencies": list(dependencies),
                "scatter_params": scatter_params,
                "workflow": nested_workflow,
            }
        return tree

    def _parse_workflow(self, workflow):
        """Parse CWL workflow specification tree."""
        tree = {}
        if isinstance(workflow, dict):
            return self._parse_steps(workflow)
        elif isinstance(workflow, list):
            for wf in workflow:
                tree.update(self._parse_steps(wf))
        return tree

    def _populate_dependencies(self, steps):
        """Populate dependencies to parsed CWL workflow tree steps."""
        for step, value in steps.items():
            nested_workflow = value.get("workflow")
            if nested_workflow and isinstance(nested_workflow, str):
                for nested_step, nested_value in steps.items():
                    if nested_workflow in nested_step:
                        nested_value["dependencies"] += value["dependencies"]
        return steps

    def _populate_complexity(self, steps):
        """Populate complexity to parsed CWL workflow tree steps."""

        def _parse_steps(steps):
            steps = steps.copy()
            for step, value in steps.items():
                scatter_params = value.get("scatter_params")
                nested_workflow = value.get("workflow")
                complexity = value.get("complexity")

                # Handle nested stages
                if nested_workflow and isinstance(nested_workflow, dict):
                    parsed_steps = _parse_steps(nested_workflow)
                    value["workflow"] = parsed_steps
                    if parsed_steps:
                        parsed_steps = self._filter_initial_steps(parsed_steps, "init")
                        complexity = self._calculate_complexity(parsed_steps)

                # Handle scatter parameters
                if scatter_params:
                    param_len = len(self.input_params.get(scatter_params, []))
                    if not param_len:
                        continue
                    complexity = [(item[0] * param_len, item[1]) for item in complexity]

                value["complexity"] = complexity
            return steps

        return _parse_steps(steps)

    def _filter_initial_steps(self, steps, initial_step):
        """Filter out initial CWL workflow tree steps."""
        tree = {}
        for step, value in steps.items():
            dependencies = value.get("dependencies", [])

            if dependencies == [initial_step]:
                tree[step] = value

            if initial_step == "init" and not dependencies:
                tree[step] = value

        return tree

    def parse_specification(self, initial_step):
        """Parse and filter out CWL workflow specification tree."""
        workflow = self.specification.get("$graph", self.specification)
        steps = self._parse_workflow(workflow)
        steps = self._populate_dependencies(steps)
        steps = self._populate_complexity(steps)
        steps = self._filter_initial_steps(steps, initial_step)
        return steps


class SnakemakeComplexityEstimator(ComplexityEstimatorBase):
    """REANA Snakemake workflow complexity estimation."""

    def _calculate_complexity(
        self, job_dependencies: Dict[str, List[str]]
    ) -> List[Tuple[int, float]]:
        """Calculate complexity of an array of job dependencies."""
        spec_steps = self.specification.get("steps", [])
        jobs_count = len(job_dependencies)
        memory_limit = 0
        for dep in job_dependencies:
            step = next(filter(lambda step: step["name"] == dep, spec_steps))
            memory_limit += self._get_memory_limit(step)
        memory_limit = memory_limit / jobs_count
        return [(jobs_count, memory_limit)]

    def _get_max_complexity(
        self, complexity: List[Tuple[int, float]]
    ) -> List[Tuple[int, float]]:
        """Get complexity of maximum concurrent job(s) allocated memory."""
        return [max(complexity, key=lambda item: item[0] * item[1])]

    def _filter_repeated_dependencies(
        self, job_dependencies: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """Filter out repeated dependencies to guess paralellization."""
        filtered_job_deps = {}
        for job, deps in job_dependencies.items():
            filtered_job_deps[job] = set(deps).difference(
                # flatten job deps
                subjob_dep
                for job_dep in deps
                for subjob_dep in job_dependencies[job_dep]
            )
        return filtered_job_deps

    def estimate_complexity(self) -> List[Tuple[int, float]]:
        """Estimate complexity array in parsed Snakemake workflow tree."""
        # dict of jobs and job dependencies
        job_dependencies = self.specification.get("job_dependencies", {})
        filtered_job_deps = self._filter_repeated_dependencies(job_dependencies)
        complexity = []
        for job_deps in filtered_job_deps.values():
            if job_deps:
                complexity += self._calculate_complexity(job_deps)
        return self._get_max_complexity(complexity)
