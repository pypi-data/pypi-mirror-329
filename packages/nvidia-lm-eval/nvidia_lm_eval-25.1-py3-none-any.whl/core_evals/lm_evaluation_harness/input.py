import logging
import os
import pathlib
import yaml
from typing import Optional

from .utils import MisconfigurationError, deep_update, dotlist_to_dict, is_package_installed
from .api_dataclasses import Task

def load_run_config(yaml_file: str) -> dict:
    """Load the run configuration from the YAML file.

    NOTE: The YAML config allows to override all the run configuration parameters.
    """
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def parse_cli_args(args) -> dict:
    """Parse CLI arguments into the run configuration format.

    NOTE: The CLI args allow to override a subset of the run configuration parameters.
    """
    config = {
        "config": {
            "type": args.eval_type,
            "output_dir": args.output_dir,
        },
        "target": {
            "api_endpoint": {
                "api_key": args.api_key_name,
                "model_id": args.model_id,
                "type": args.model_type,
                "url": args.model_url,
            }
        }
    }
    overrides = parse_override_params(args.overrides)
    # "--overrides takes precedence over other CLI args (e.g. --model_id)"
    config = deep_update(
        config, overrides, skip_nones=True
    )
    return config


def parse_override_params(override_params_str: Optional[str] = None) -> dict:
    if not override_params_str:
        return {}
    override_params = override_params_str.split(",")
    return dotlist_to_dict(override_params)


def validate_cli_args(run_config_cli_overrides: dict) -> None:
    required_keys = [
        (("config", "type"), "--eval_type"),
        (("config", "output_dir"), "--output_dir"),
        (("target", "api_endpoint", "model_id"), "--model_id"),
        (("target", "api_endpoint", "type"), "--model_type"),
        (("target", "api_endpoint", "url"), "--model_url"),
    ]

    for (keys, arg) in required_keys:
        d = run_config_cli_overrides
        for key in keys:
            if key not in d or d[key] is None:
                raise MisconfigurationError(f"Missing required argument: {arg} (run config key: {'.'.join(keys)})")
            d = d[key]


def get_framework_tasks(
    filepath: str, run_config_cli_overrides: Optional[dict] = None
) -> tuple[str, str, list[Task]]:
    framework = {}
    with open(filepath, "r") as f:
        framework = yaml.safe_load(f)

        framework_name = framework["framework"]["name"]
        pkg_name = framework["framework"]["pkg_name"]
        run_config_framework_defaults = framework["defaults"]

    tasks = dict()
    for task_dict in framework["evaluations"]:
        # Apply run config task defaults onto the framework defaults
        run_config = deep_update(
            run_config_framework_defaults, task_dict["defaults"], skip_nones=True)

        # Apply run config CLI overrides onto the framework+task defaults
        # TODO(pj): This is a hack and we should only override the config of the task
        #           that was picked in the CLI. Move it somehow one level up where we
        #           already have the task picked.
        run_config = deep_update(
            run_config, run_config_cli_overrides or {}, skip_nones=True)

        task = Task(
            framework_name=framework_name,
            pkg_name=pkg_name,
            **run_config,
        )

        tasks[task_dict["defaults"]["config"]["type"]] = task
    return framework_name, pkg_name, tasks


def get_available_tasks(run_config_cli_overrides: Optional[dict] = None) -> tuple[dict[str, dict[str, Task]], dict[str, Task]]:
    def_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'framework.yml')
    if not os.path.exists(def_file):
        raise ValueError(f"Framework Definition File does not exists at {def_file}")

    framework_task_mapping = {}  # framework name -> set of tasks   | used in 'framework.task' invocation
    task_name_mapping = {}       # task name      -> set of tasks   | used in 'task' invocation

    logging.debug(f"Loading task definitions from file: {def_file}")
    framework_name, pkg_name, framework_tasks = get_framework_tasks(def_file, run_config_cli_overrides)
    if not is_package_installed(pkg_name):
        logging.warning(f"Framework {framework_name} is not installed. Skipping. Tasks from this framework will not be available to run.")
    else:
        framework_task_mapping[framework_name] = framework_tasks
        task_name_mapping.update(framework_tasks)

    return framework_task_mapping, task_name_mapping


def validate_task(run_config_cli_overrides: dict) -> Task:
    # NOTE: evaluation type can be either 'framework.task' or 'task'
    # TODO(pj): Does it still make sense, when we have one framework per docker?
    eval_type_components = run_config_cli_overrides["config"]["type"].split(".")
    if len(eval_type_components) == 2:
        framework_name, task_name = eval_type_components
    elif len(eval_type_components) == 1:
        framework_name, task_name = None, eval_type_components[0]
    else:
        raise MisconfigurationError("eval_type must follow 'framework_name.task_name'. No additional dots are allowed.")

    framework_tasks_mapping, all_tasks_mapping = get_available_tasks(run_config_cli_overrides)
    
    if framework_name:
        try:
            tasks_mapping = framework_tasks_mapping[framework_name]
        except KeyError:
            raise MisconfigurationError(f"Unknown framework {framework_name}. Frameworks available: {', '.join(framework_tasks_mapping.keys())}")
    else:
        tasks_mapping = all_tasks_mapping
        
    try:
        task = tasks_mapping[task_name]
    except KeyError:
        raise MisconfigurationError(f"Unknown task {task_name}. Tasks available: {', '.join(tasks_mapping.keys())}")

    logging.info(f"Invoked config:\n{str(task)}")

    try:
        os.makedirs(task.config.output_dir, exist_ok=True)
    except OSError as error:
        print(f"An error occurred while creating output directory: {error}")
        
    with open(os.path.join(task.config.output_dir, "run_config.yml"), "w") as f:
        yaml.dump(task.model_dump(), f)

    return task