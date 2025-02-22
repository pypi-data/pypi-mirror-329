import os
import argparse
import sys
import yaml
import logging

# NOTE(dfridman): will be removed once all benchmarks comply with updated output format
from .api_dataclasses import EvaluationConfig, EvaluationResult, EvaluationTarget
from .evaluate import evaluate_accuracy
from .input import get_available_tasks, load_run_config, parse_cli_args, validate_cli_args, validate_task
from .utils import deep_update


def run_eval() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Debug the core_evals script")
    subparsers = parser.add_subparsers(help='Functions')
    parser_ls = subparsers.add_parser('ls', help='List available evaluation types')
    parser_ls.set_defaults(command="ls")

    parser_run = subparsers.add_parser('run_eval', help="Run the evaluation")
    parser_run.add_argument('--eval_type', type=str, help="Run config.: task name")
    parser_run.add_argument('--model_id', type=str, help="Run config.: model name")
    parser_run.add_argument('--model_type', type=str, help="Run config.: endpoint type", choices=['chat', 'completions', 'vlm'])
    parser_run.add_argument('--model_url', type=str, help="Run config.: model URI")
    parser_run.add_argument('--output_dir', type=str, help="Run config.: results output dir.")
    parser_run.add_argument('--api_key_name', type=str, help="Run config.: API key env variable name (optional)", default=None)
    parser_run.add_argument('--run_config', type=str, help="Load the run configuration from the YAML file (optional and overridden by the cli arguments)", default=None)
    parser_run.add_argument('--overrides', type=str, help="Comma-separated dot-style parameters to override config values (overriding values from run_config and CLI args)", default=None)
    parser_run.add_argument('--dry_run', action='store_true', help="Shows rendered config and command instead of running", default=False)
    parser_run.set_defaults(command="run_eval")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if "command" not in args:
        parser.print_help()
        sys.exit(0)

    if args.command == "ls":
        _, task_name_mapping = get_available_tasks()
        print("Available tasks:")
        for task in sorted(task_name_mapping.values(), key = lambda task: task.config.type):
            print(f"* {task.config.type} (in {task.framework_name})")

    elif args.command == "run_eval":
        run_config = load_run_config(args.run_config) if args.run_config else {}
        # CLI args take precedence over YAML run config
        run_config = deep_update(
            run_config, parse_cli_args(args), skip_nones=True
        )
        validate_cli_args(run_config)
        if args.dry_run:
            task = validate_task(run_config)
            print("Rendered config:\n")
            config = task.model_dump()
            print(yaml.dump(
                config, sort_keys=False, default_flow_style=False, indent=2))
            print("\nRendered command:\n")
            cmd = task.render_command()
            print(cmd)
            exit(0)
        
        eval_cfg = EvaluationConfig(**run_config["config"])
        target_cfg = EvaluationTarget(**run_config["target"])

        evaluation_result = evaluate_accuracy(eval_cfg, target_cfg)
        if isinstance(evaluation_result, EvaluationResult):
            evaluation_result_dict = evaluation_result.model_dump()
        else:
            logging.warning("Deprecated output API is used. Will be updated soon.")
            evaluation_result_dict = evaluation_result
        
        run_command = validate_task({"config": eval_cfg.model_dump(), "target": target_cfg.model_dump()}).render_command()
        evaluation_result_dict = {
            "git_hash": os.getenv("CORE_EVALS_GIT_HASH"),
            "command": run_command,
            **run_config,
            "results": evaluation_result_dict,
        }
        with open(os.path.join(eval_cfg.output_dir, "results.yml"), "w") as f:
            yaml.dump(evaluation_result_dict, f)


        print("========== RESULTS ==========")
        print(yaml.dump(evaluation_result_dict))

if __name__ == "__main__":
    run_eval()
