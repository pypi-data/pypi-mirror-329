import logging

from .api_dataclasses import EvaluationConfig, EvaluationResult, EvaluationTarget
from .input import validate_task
from .utils import MisconfigurationError, run_command

def evaluate_accuracy(
    eval_cfg: EvaluationConfig, target_cfg: EvaluationTarget
) -> EvaluationResult:
    try:
        from .output import parse_output
    except ImportError:
        raise ImportError("No valid output parser was found for the framework. Please add a proper parse_output implementation.")

    run_config_cli_overrides = {
        "config": eval_cfg.model_dump(),
        "target": target_cfg.model_dump()
    }
    task = validate_task(run_config_cli_overrides)
    if (task.config.supported_endpoint_types is None
        or task.target.api_endpoint.type not in task.config.supported_endpoint_types):
        raise MisconfigurationError(
            f"The benchmark '{task.config.type}' does not support the model type '{task.target.api_endpoint.type}'. "
            f"The benchmark supports '{task.config.supported_endpoint_types}'.")

    cmd = task.render_command()
    logging.info(f"Command: {cmd}")
    return_code = run_command(cmd, verbose=True)
    if return_code != 0:
        raise RuntimeError("Evaluation failed! Please consult the logs above")

    evaluation_result = parse_output(task.config.output_dir)
    return evaluation_result
