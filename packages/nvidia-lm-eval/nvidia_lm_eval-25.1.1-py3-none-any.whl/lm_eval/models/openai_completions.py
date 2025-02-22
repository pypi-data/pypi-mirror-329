import os
from collections import defaultdict
from functools import cached_property
from typing import Any, Dict, List, Optional, Tuple, Union

from lm_eval.api.registry import register_model
from lm_eval.models.api_models import TemplateAPI
from lm_eval.utils import eval_logger


@register_model("local-completions")
class LocalCompletionsAPI(TemplateAPI):
    def __init__(
        self,
        base_url=None,
        tokenizer_backend="huggingface",
        **kwargs,
    ):
        super().__init__(
            base_url=base_url, tokenizer_backend=tokenizer_backend, **kwargs
        )

    def _create_payload(
        self,
        messages: Union[List[List[int]], List[dict], List[str], str],
        generate: bool = False,
        gen_kwargs: Optional[dict] = None,
        stream: bool = False,
        seed: int = 1234,
        **kwargs,
    ) -> dict:
        if generate:
            gen_kwargs.pop("do_sample", False)
            if "max_tokens" in gen_kwargs:
                max_tokens = gen_kwargs.pop("max_tokens")
            else:
                max_tokens = gen_kwargs.pop("max_gen_toks", self._max_gen_toks)
            temperature = gen_kwargs.pop("temperature", 0)
            stop = gen_kwargs.pop("until", ["<|endoftext|>"])
            return {
                "prompt": messages,
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stop": stop,
                "stream": stream,
                "seed": seed,
                **gen_kwargs,
            }
        else:
            return {
                "model": self.model,
                "prompt": messages,
                "temperature": 0,
                "max_tokens": 1,
                "logprobs": 1,
                "stream": stream,
                "seed": seed,
                "echo": True,
            }

    @staticmethod
    def parse_logprobs(
        outputs: Union[Dict, List[Dict]],
        tokens: List[List[int]] = None,
        ctxlens: List[int] = None,
        **kwargs,
    ) -> List[Tuple[float, bool]]:
        """Parse either full or chunked (streamed) output.

        NOTE: Choices are batch elements here.
        """
        if isinstance(outputs, list):  # Streamed output
            # NOTE: When streaming logprobs, each batch element's logprobs come back in
            #       a single and separate message. It is so because, when generate=False,
            #       we generate max_tokens=1 per batch element (see _create_payload).
            choices = [None] * len(outputs)
            for out in outputs:
                choice = out["choices"][0]
                # Preserve the order of elements in the batch
                choices[choice["index"]] = choice
        else:  # Full output
            choices = outputs["choices"]

        res = []
        for choice, ctxlen in zip(choices, ctxlens):
            assert ctxlen > 0, "Context length must be greater than 0"
            logprobs = sum(choice["logprobs"]["token_logprobs"][ctxlen:-1])
            tokens = choice["logprobs"]["token_logprobs"][ctxlen:-1]
            top_logprobs = choice["logprobs"]["top_logprobs"][ctxlen:-1]
            is_greedy = True
            for tok, top in zip(tokens, top_logprobs):
                if tok != max(top, key=top.get):
                    is_greedy = False
                    break
            res.append((logprobs, is_greedy))
        return res

    @staticmethod
    def parse_generations(outputs: Union[Dict, List[Dict]], **kwargs) -> List[str]:
        """Parse either full or chunked (streamed) output.

        NOTE: Choices are batch elements here.
        """
        if isinstance(outputs, list):  # Streamed output
            # NOTE: When streaming completions, each one is chunked across multiple
            #       messages. However, each message contains only one chunk of a single
            #       batch element's completion and chunks should be ordered.
            choices = defaultdict(str)
            for out in outputs:
                choice = out["choices"][0]
                choices[choice["index"]] += choice["text"]
            # Preserve the order of elements in the batch
            return [choices[i] for i in range(len(choices))]
        else:  # Full output
            # Unpack the completions
            return [choice["text"] for choice in outputs["choices"]]

    @property
    def api_key(self):
        return os.environ.get("OPENAI_API_KEY", "")


@register_model("local-chat-completions")
class LocalChatCompletion(LocalCompletionsAPI):
    def __init__(
        self,
        base_url=None,
        tokenizer_backend=None,
        tokenized_requests=False,
        **kwargs,
    ):
        eval_logger.warning(
            "chat-completions endpoint requires the `--apply_chat_template` flag."
        )
        super().__init__(
            base_url=base_url,
            tokenizer_backend=tokenizer_backend,
            tokenized_requests=tokenized_requests,
            **kwargs,
        )
        if self._batch_size > 1:
            eval_logger.warning(
                "Chat completions does not support batching. Defaulting to batch size 1."
            )
            self._batch_size = 1

    def _create_payload(
        self,
        messages: List[Dict],
        generate: bool = False,
        gen_kwargs: dict = None,
        stream: bool = False,
        seed: int = 1234,
        **kwargs,
    ) -> dict:
        assert gen_kwargs.get("n", 1) == 1, "Only one chat completion per request is supported."

        gen_kwargs.pop("do_sample", False)
        if "max_tokens" in gen_kwargs:
            max_tokens = gen_kwargs.pop("max_tokens")
        else:
            max_tokens = gen_kwargs.pop("max_gen_toks", self._max_gen_toks)
        temperature = gen_kwargs.pop("temperature", 0)
        stop = gen_kwargs.pop("until", ["<|endoftext|>"])
        if not isinstance(stop, (list, tuple)):
            stop = [stop]
        return {
            "messages": messages,
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": stop[:4],
            "stream": stream,
            "seed": seed,
            **gen_kwargs,
        }

    @staticmethod
    def parse_generations(outputs: Union[Dict, List[Dict]], **kwargs) -> List[str]:
        """Parse either full or chunked (streamed) output.

        NOTE: We generate one chat completion for each request (see _create_payload),
              hence we take the first choice.
        NOTE: Chat completion API doesn't support batching (see __init__),
              therefore we return a single message.
        """
        if isinstance(outputs, list):  # Streamed output
            # Aggregate deltas into a single message
            chunks = [
                # Drop the None content in the first chunk
                chunk["choices"][0]["delta"]["content"] or ""
                for chunk in outputs
            ]
            return ["".join(chunks)]
        else:  # Full output
            # Unpack the completion
            return [outputs["choices"][0]["message"]["content"]]

    def tok_encode(
        self,
        string: Union[str, Any],
        left_truncate_len=None,
        add_special_tokens=None,
        **kwargs,
    ) -> Union[List[str], List[int], Any]:
        return string

    def loglikelihood(self, requests, **kwargs):
        raise NotImplementedError(
            "Loglikelihood is not supported for chat completions. Consider using the completions API instead."
        )


@register_model(
    "openai-completions",
)
class OpenAICompletionsAPI(LocalCompletionsAPI):
    def __init__(
        self,
        base_url="https://api.openai.com/v1/completions",
        tokenizer_backend="tiktoken",
        **kwargs,
    ):
        super().__init__(
            base_url=base_url, tokenizer_backend=tokenizer_backend, **kwargs
        )

    @cached_property
    def api_key(self):
        """Override this property to return the API key for the API request."""
        key = os.environ.get("OPENAI_API_KEY", None)
        if key is None:
            raise ValueError(
                "API key not found. Please set the OPENAI_API_KEY environment variable."
            )
        return key

    def loglikelihood(self, requests, **kwargs):
        assert (
            self.model != "gpt-3.5-turbo"
        ), "Loglikelihood is not supported for gpt-3.5-turbo"
        return super().loglikelihood(requests, **kwargs)

    def chat_template(self, chat_template: Union[bool, str] = False) -> Optional[str]:
        return ""


@register_model("openai-chat-completions")
class OpenAIChatCompletion(LocalChatCompletion):
    def __init__(
        self,
        base_url="https://api.openai.com/v1/chat/completions",
        tokenizer_backend=None,
        tokenized_requests=False,
        **kwargs,
    ):
        super().__init__(
            base_url=base_url,
            tokenizer_backend=tokenizer_backend,
            tokenized_requests=tokenized_requests,
            **kwargs,
        )

    @cached_property
    def api_key(self):
        """Override this property to return the API key for the API request."""
        key = os.environ.get("OPENAI_API_KEY", None)
        if key is None:
            raise ValueError(
                "API key not found. Please set the OPENAI_API_KEY environment variable."
            )
        return key
