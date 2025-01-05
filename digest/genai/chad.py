"""
# langchain = "^0.2.16"


# example
from digest.genai.chad import Chad

from dotenv import load_dotenv
import os

load_dotenv()

chad_api = Chad(
    chad_api_key=os.getenv("CHAD_API_KEY"),
    model=os.getenv("CHAD_API_MODEL"),
)

print(chad_api.invoke("How are you?"))  # noqa: T201
"""

from typing import Any, cast

import requests
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.pydantic_v1 import SecretStr
from langchain_core.utils import convert_to_secret_str, get_from_dict_or_env, pre_init


class Chad(LLM):
    """Chad large language models.

    To use, you should have the environment variable ``Chad_API_KEY``
    set with your API key or pass it as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from langchain_community.llms import Chad
            chad_api = Chad(chad_api_key="my-api-key", model="gpt-4o-mini")
    """

    model: str = "gpt-4o-mini"
    """Model name to use."""

    temperature: float = 0.7
    """What sampling temperature to use."""

    maxTokens: int = 2000
    """The maximum number of tokens to generate in the completion."""

    chad_api_key: SecretStr | None = None

    base_url: str | None = None
    """Base url to use, if None decides based on model name."""

    class Config:
        extra = "forbid"

    @pre_init
    def validate_environment(cls, values: dict) -> dict:
        """Validate that api key exists in environment."""
        chad_api_key = convert_to_secret_str(get_from_dict_or_env(values, "chad_api_key", "CHAD_API_KEY"))
        values["chad_api_key"] = chad_api_key
        return values

    @property
    def _default_params(self) -> dict[str, Any]:
        """Get the default parameters for calling Chad API."""
        return {
            "temperature": self.temperature,
            "max_tokens": self.maxTokens,
        }

    @property
    def _identifying_params(self) -> dict[str, Any]:
        """Get the identifying parameters."""
        return {**{"model": self.model}, **self._default_params}

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "chad"

    def _call(
        self,
        prompt: str,
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> str:
        """Call out to Chad's complete endpoint.

        Args:
            prompt: The prompt to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            The string generated by the model.

        Example:
            .. code-block:: python

                response = ai21("Tell me a joke.")
        """
        if self.base_url is not None:
            base_url = self.base_url
        else:
            base_url = "https://ask.chadgpt.ru/api/public"
        params = {**self._default_params, **kwargs}
        self.chad_api_key = cast(SecretStr, self.chad_api_key)
        response = requests.post(
            url=f"{base_url}/{self.model}",
            json={
                "message": prompt,
                "api_key": self.chad_api_key.get_secret_value(),
                **params,
            },
        )
        if response.status_code != 200:
            optional_detail = response.json().get("error")
            raise ValueError(
                f"Chad /complete call failed with status code {response.status_code}. Details: {optional_detail}"
            )
        response_json = response.json()
        return response_json["response"]
