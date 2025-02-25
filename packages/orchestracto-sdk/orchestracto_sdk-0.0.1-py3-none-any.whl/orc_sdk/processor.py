import argparse
import dataclasses
import datetime
import importlib.util
import inspect
import os
import os.path
import subprocess
import sys
import tempfile
from typing import Any

import yaml

from orc_client.client import OrcClient

from orc_sdk.workflow import WorkflowRuntimeObject
from orc_sdk.step import FuncStep, RetValWrapper


def load_module(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def compile_wf_config(wfro: WorkflowRuntimeObject) -> dict[str, Any]:
    wf_config = {
        "triggers": [],
        "steps": [],
    }

    steps = wfro.get_steps()
    for step_id, sci_info in steps.items():
        if isinstance(sci_info.sci, FuncStep):
            func_signature = inspect.signature(sci_info.sci.func)

            passed_args = {}
            for i, arg in enumerate(sci_info.sci.func_args):
                arg_name = list(func_signature.parameters.keys())[i]  # FIXME??
                passed_args[arg_name] = arg

            for name, value in sci_info.sci.func_kwargs.items():
                passed_args[name] = value

            step_args = []
            for i, name in enumerate(func_signature.parameters):
                if name in passed_args:
                    if isinstance(passed_args[name], RetValWrapper):
                        src_type = "step_output"
                        src_ref = f"{passed_args[name].sci.step_id}.{passed_args[name].name}"
                    else:
                        src_type = "constant"
                        src_ref = passed_args[name]
                else:
                    src_type = "constant"
                    src_ref = func_signature.parameters[name].default

                step_args.append({
                    "name": name,
                    "src_type": src_type,
                    "src_ref": src_ref,
                })

            secrets = []
            for secret in sci_info.sci.secrets:
                secrets.append({
                    "key": secret.key,
                    "value_ref": secret.value_ref,
                    "value_src_type": secret.value_src_type,
                })

            wf_config["steps"].append({
                "step_id": step_id,
                "task_type": "docker",
                "task_params": {
                    "docker_image": "TODO",
                    "command": sci_info.sci.func.__name__,
                },
                "args": step_args,
                "secrets": secrets,
                "outputs": [{
                    "name": name,
                } for name in sci_info.sci.retval_names],
                "depends_on": list(sci_info.depends_on),
                "cache": {
                    "enable": sci_info.sci.cache.enable,
                },
            })
        else:
            raise NotImplementedError

    wf_config["triggers"] = wfro.triggers

    return wf_config


def get_wfro_from_file(filename: str) -> WorkflowRuntimeObject:
    module = load_module(filename, "user_code")
    for key, obj in module.__dict__.items():
        if getattr(obj, "is_workflow", False):
            wfro = obj()  # TODO: args?
            return wfro
    else:
        raise Exception("No workflow found")


def get_file_module_root(filename: str) -> str:
    dirname = os.path.dirname(os.path.abspath(filename))
    if not os.path.exists(os.path.join(dirname, "__init__.py")):
        return filename
    return get_file_module_root(dirname)


BASE_IMAGE = "cr.eu-north1.nebius.cloud/e00faee7vas5hpsh3s/orchestracto/sdk-simple-runtime:24"


def login_in_registry(registry_url: str, token: str):
    proc = subprocess.Popen(
        ["docker", "login", registry_url, "--password-stdin", "-u", "user"],
        stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr
    )
    proc.communicate(token.encode())
    proc.wait()


def build_docker_with_reqs(
        workflow_path: str,
        image_name: str,
        wf_file_module: str,
        additional_requirements: list[str],
        base_image: str = BASE_IMAGE,
) -> str:
    py_packages_installation = f"""
        RUN pip install -U {" ".join(additional_requirements)}
        """ if additional_requirements else ""

    dockerfile = f"""
        FROM {BASE_IMAGE} AS sdk_runtime
        FROM {base_image}
        USER root
        {py_packages_installation}
        RUN mkdir /orc
        COPY {os.path.basename(wf_file_module)} /orc/lib/{os.path.basename(wf_file_module)}
        COPY --from=sdk_runtime /usr/local/lib/python3.12/site-packages/orc_sdk /orc/lib/orc_sdk
        COPY --from=sdk_runtime /usr/local/bin/orc_run_step /usr/local/bin/orc_run_step
        RUN new_shebang='#!/usr/bin/env python3' && sed -i "1s|.*|$new_shebang|" /usr/local/bin/orc_run_step
        RUN chmod +x /usr/local/bin/orc_run_step
    """

    registry_url = os.environ.get("REGISTRY_URL")  # TODO: get from //sys/@ui_config?..
    if registry_url is None:
        registry_url = "registry." + os.environ["YT_PROXY"].removeprefix("https://").removeprefix("http://")

    login_in_registry(registry_url, os.environ["YT_TOKEN"])

    image_rel_path = workflow_path.removeprefix("//") + "/" + image_name
    docker_tag = f"{registry_url}/home/orchestracto/public_registry/{image_rel_path}:latest"

    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, "w") as f:
            f.write(dockerfile)
        subprocess.check_call(["docker", "build", "-t", docker_tag, "-f", tf.name, "--platform", "linux/amd64", os.path.dirname(wf_file_module), "--push"])

    return docker_tag


def get_docker_image_with_sha(docker_image: str) -> str:
    return subprocess.check_output([
        "docker", "inspect", "--format", "{{index .RepoDigests 0}}", docker_image
    ]).decode().strip()


@dataclasses.dataclass
class WorkflowInfo:
    workflow_path: str
    workflow_config: dict[str, Any]


def get_wf_info_from_file(filename: str) -> WorkflowInfo:
    wfro = get_wfro_from_file(filename)
    wf_config = compile_wf_config(wfro)

    wf_file_module = get_file_module_root(filename)

    if os.path.abspath(wf_file_module) != os.path.abspath(filename):
        wf_file_module_dir = os.path.dirname(wf_file_module)  # FIXME
        rel_file_path = os.path.abspath(filename).removeprefix(wf_file_module_dir + "/")
    else:
        rel_file_path = os.path.basename(filename)  # TODO FIXME
    path_in_container = f"/orc/lib/{rel_file_path}"

    default_docker_tag = build_docker_with_reqs(
        wfro.workflow_path, "default",
        wf_file_module,
        wfro.additional_requirements
    )

    wfro_steps = wfro.get_steps()

    for step in wf_config["steps"]:
        step_id = step["step_id"]
        sci = wfro_steps[step_id].sci
        assert isinstance(sci, FuncStep)
        if sci.additional_requirements or sci.base_image:
            docker_tag = build_docker_with_reqs(
                wfro.workflow_path, step_id,
                wf_file_module,
                wfro.additional_requirements + sci.additional_requirements,
                base_image=sci.base_image or BASE_IMAGE,
            )
            step["task_params"]["docker_image"] = docker_tag
        else:
            step["task_params"]["docker_image"] = default_docker_tag

        step["task_params"]["env"] = {"PYTHONPATH": "/orc/lib", "YT_BASE_LAYER": step["task_params"]["docker_image"]}
        step["task_params"]["command"] = f"orc_run_step {path_in_container} {step_id} >&2"  # FIXME: corrupts cache key
        step["task_params"]["func_code_hash"] = sci.func_code_hash

    return WorkflowInfo(workflow_path=wfro.workflow_path, workflow_config=wf_config)


def process_python_file(filename: str):
    wf_info = get_wf_info_from_file(filename)

    if "ORC_URL" not in os.environ:
        yt_proxy = os.environ.get("YT_PROXY")
        if yt_proxy is None:
            raise ValueError("Either ORC_URL or YT_PROXY environment variable should be set")
        orc_url = "https://orc." + yt_proxy.removeprefix("https://").removeprefix("http://")
    else:
        orc_url = os.environ["ORC_URL"]

    orc_client = OrcClient(orc_url=orc_url, yt_token=os.environ["YT_TOKEN"])
    orc_client.update_workflow(wf_info.workflow_path, wf_info.workflow_config)


def configure_arg_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(dest="command")

    get_config = subparsers.add_parser("get-config")
    get_config.add_argument("filename", type=str)

    process_parser = subparsers.add_parser("process")
    process_parser.add_argument("filename", type=str)

    return parser


def process_args(args: argparse.Namespace):
    match args.command:
        case "process":
            process_python_file(args.filename)
