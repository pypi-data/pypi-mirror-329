"""LLM Commons"""

from typing import Any, ClassVar

from cmem_plugin_base.dataintegration.context import (
    PluginContext,
)
from cmem_plugin_base.dataintegration.types import Autocompletion, StringParameterType
from openai import AuthenticationError, OpenAI


class SamePathError(ValueError):
    """Same Path Exception"""

    def __init__(self, path: str):
        super().__init__(f"Path '{path}' can not be input AND output path.")


class OpenAPIModel(StringParameterType):
    """OpenAPI Model Type"""

    autocompletion_depends_on_parameters: ClassVar[list[str]] = ["url", "api_key"]

    # auto complete for values
    allow_only_autocompleted_values: bool = True
    # auto complete for labels
    autocomplete_value_with_labels: bool = True

    def autocomplete(
        self,
        query_terms: list[str],
        depend_on_parameter_values: list[Any],
        context: PluginContext,
    ) -> list[Autocompletion]:
        """Return all results that match ALL provided query terms."""
        _ = context
        url = depend_on_parameter_values[0]
        api_key = depend_on_parameter_values[1]
        api_key = api_key if isinstance(api_key, str) else api_key.decrypt()
        result = []
        try:
            api = OpenAI(api_key=api_key, base_url=url)
            models = api.models.list()
            filtered_models = set()
            if query_terms:
                for term in query_terms:
                    for model in models:
                        if term in model.id:
                            filtered_models.add(model.id)
            else:
                filtered_models = {_.id for _ in models}
            result = [Autocompletion(value=f"{_}", label=f"{_}") for _ in filtered_models]
        except AuthenticationError as error:
            raise ValueError(
                "Failed to authenticate with OpenAI API, Please check URL and API key."
            ) from error

        result.sort(key=lambda x: x.label)
        return result
