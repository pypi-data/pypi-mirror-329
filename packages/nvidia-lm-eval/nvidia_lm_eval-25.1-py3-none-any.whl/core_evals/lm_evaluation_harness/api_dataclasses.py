from pydantic import BaseModel, Field
import jinja2
from typing import Any, Dict, Optional

# NOTE: For ApiEndpoint, EvaluationTarget, ConfigParams, and EvaluationConfig all fields
#       are Optional and default=None, because depending on the command run (run_eval or
#       ls) we either require them or don't. We also don't require user to provide all
#       of them. The framework.yml often provides the defaults.

class ApiEndpoint(BaseModel):
    api_key: Optional[str] = Field(description="Name of the env variable that stores API key for the model", default=None)
    model_id: Optional[str] = Field(description="Name of the model", default=None)
    stream: Optional[bool] = Field(description="Whether responses should be streamed", default=None)
    type: Optional[str] = Field(description="The type of the target", default=None)
    url: Optional[str] = Field(description="Url of the model", default=None)


class EvaluationTarget(BaseModel):
    api_endpoint: Optional[ApiEndpoint] = Field(description="API endpoint to be used for evaluation", default=None)


class ConfigParams(BaseModel):
    limit_samples: Optional[int] = Field(description="Limit number of evaluation samples", default=None)
    max_new_tokens: Optional[int] = Field(description="Max tokens to generate", default=None)
    max_retries: Optional[int] = Field(description="Number of REST request retries", default=None)
    parallelism: Optional[int] = Field(description="Parallelism to be used", default=None)
    task: Optional[str] = Field(description="Name of the task", default=None)
    temperature: Optional[float] = Field(description="Float value between 0 and 1. temp of 0 indicates greedy decoding, where the token with highest prob is chosen. Temperature can't be set to 0.0 currently", default=None)
    timeout: Optional[int] = Field(description="REST response timeout", default=None)
    top_p: Optional[float] = Field(description="Float value between 0 and 1; limits to the top tokens within a certain probability. top_p=0 means the model will only consider the single most likely token for the next prediction", default=None)
    extra: Optional[Dict[str, Any]] = Field(description="Framework specific parameters to be used for evaluation", default_factory=dict)


class EvaluationConfig(BaseModel):
    output_dir: Optional[str] = Field(description="Directory to output the results", default=None)
    params: Optional[ConfigParams] = Field(description="Parameters to be used for evaluation", default=None)
    supported_endpoint_types: Optional[list[str]] = Field(description="Supported endpoint types like chat or completions", default=None)
    type: Optional[str] = Field(description="Type of the task", default=None)


class Task(BaseModel):
    # TODO(pj): Here and everywhere else rename Task into Evaluation (incl. vars, etc.)
    command: str = Field(description="jinja template of the command to be executed")
    framework_name: str = Field(description="Name of the framework")
    pkg_name: str = Field(description="Name of the package")
    config: EvaluationConfig
    target: EvaluationTarget

    def render_command(self):
        return jinja2.Template(self.command, undefined=jinja2.StrictUndefined).render(self.model_dump())


class Score(BaseModel):
    value: float = Field(
        description="The value/score produced on this metric"
    )
    stats: Optional[Dict[str, Any]]= Field(
        description="Any metadata associated with this metric, as key-value pairs"
    )


class MetricResult(BaseModel):
    scores: Dict[str, Score] = Field(
        default_factory=dict,
        description="Mapping from metric name to scores."
    )


class TaskResult(BaseModel):
    metrics: Dict[str, MetricResult] = Field(
        default_factory=dict,
        description="The value for all the metrics computed for the task"
    )


class EvaluationResult(BaseModel):
    tasks: Optional[Dict[str, TaskResult]] = Field(
        default_factory=dict,
        description="The results at the task-level"
    )
    groups: Optional[Dict[str, TaskResult]] = Field(
        default_factory=dict,
        description="The results at the group-level"
    )
