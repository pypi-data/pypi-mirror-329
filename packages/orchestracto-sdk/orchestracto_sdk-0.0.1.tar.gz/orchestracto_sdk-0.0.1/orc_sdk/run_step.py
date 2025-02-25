#!/usr/bin/env python3

import argparse
import importlib.util
import json
import os
import sys

from orc_sdk.step import FuncStep


def load_module(file_name, module_name):  # FIXME: duplicate
    spec = importlib.util.spec_from_file_location(module_name, file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pyfile_with_workflow")
    parser.add_argument("step_id")
    parser.add_argument("--base-layer")

    args = parser.parse_args()

    module = load_module(args.pyfile_with_workflow, "workflow")

    for key, obj in module.__dict__.items():
        if getattr(obj, "is_workflow", False):
            wfro = obj()
            break
    else:
        raise Exception("No workflow found")

    steps = wfro.get_steps()
    the_step_sci = steps[args.step_id].sci

    if not isinstance(the_step_sci, FuncStep):
        raise NotImplementedError

    for key, value in os.environ.items():
        if key.startswith("YT_SECURE_VAULT_"):
            os.environ[key.removeprefix("YT_SECURE_VAULT_")] = value

    returned_values = the_step_sci.run()

    if len(the_step_sci.retval_names) > 0:
        if not isinstance(returned_values, tuple):
            returned_values = (returned_values,)

        ret_dict = {}
        for idx, value in enumerate(returned_values):
            ret_dict[the_step_sci.retval_names[idx]] = value

        print(json.dumps(ret_dict))


if __name__ == "__main__":
    main()
