"""Create Embeddings via OpenAI embeddings API endpoint"""

import json
from collections.abc import Generator, Sequence
from string import Template

from cmem_plugin_base.dataintegration.context import (
    ExecutionContext,
    ExecutionReport,
)
from cmem_plugin_base.dataintegration.description import Icon, Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities,
    Entity,
    EntityPath,
    EntitySchema,
)
from cmem_plugin_base.dataintegration.parameter.multiline import MultilineStringParameterType
from cmem_plugin_base.dataintegration.parameter.password import Password, PasswordParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from cmem_plugin_base.dataintegration.ports import (
    FixedNumberOfInputs,
    FixedSchemaPort,
    FlexibleSchemaPort,
)
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

from cmem_plugin_llm.commons import OpenAPIModel, SamePathError

DEFAULT_INSTRUCTION_OUTPUT_PATH = "_instruction_output"
MODEL_EXAMPLE = "gpt-4o"
INSTRUCTION_EXAMPLE = r"""Write a paragraph about this entity: ${entity}"""
PROMPT_TEMPLATE_EXAMPLE = r"""
        [{
            "role": "developer",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "${instruct}"
        }]
"""


@Plugin(
    label="Execute Instructions",
    plugin_id="cmem_plugin_llm-ExecuteInstructions",
    icon=Icon(package=__package__, file_name="execute_instruction.svg"),
    description="Send instructions (prompt) to an LLM and process the result.",
    parameters=[
        PluginParameter(
            name="url",
            label="URL",
            description="URL of the OpenAI API (without endpoint path and without trailing slash)",
            default_value="https://api.openai.com/v1",
        ),
        PluginParameter(
            name="api_key",
            label="API key",
            param_type=PasswordParameterType(),
            description="Fill the OpenAI API key if needed "
            "(or give a dummy value in case you access an unsecured endpoint).",
        ),
        PluginParameter(
            name="model",
            label="Instruct Model",
            description=f"The instruct model, e.g. {MODEL_EXAMPLE}",
            param_type=OpenAPIModel(),
        ),
        PluginParameter(
            name="instruct_tempalte",
            label="Instruction",
            description="A template instruction.",
            default_value=INSTRUCTION_EXAMPLE,
            param_type=MultilineStringParameterType(),
        ),
        PluginParameter(
            name="timout_single_request",
            label="Timeout",
            description="The timeout of a single request in milliseconds",
            advanced=True,
            default_value=10000,
        ),
        PluginParameter(
            name="prompt_template",
            label="Prompt Template",
            description="""A prompt template compatible with OpenAI chat completion API message
            object.""",
            advanced=True,
            default_value=PROMPT_TEMPLATE_EXAMPLE,
            param_type=MultilineStringParameterType(),
        ),
        PluginParameter(
            name="instruct_output_path",
            label="Instruct Ouput Path",
            description="The entity path where the instruction result will be writen.",
            advanced=True,
            default_value=DEFAULT_INSTRUCTION_OUTPUT_PATH,
        ),
    ],
)
class ExecuteInstruction(WorkflowPlugin):
    """Execute Instructions from OpenAI completion API endpoint over entities"""

    execution_context: ExecutionContext
    embeddings: OpenAIEmbeddings
    instruct_output_path: str
    instruct_report: ExecutionReport
    prompt_template: str
    instruct_template: str
    client: OpenAI
    model: str

    def __init__(  # noqa: PLR0913
        self,
        url: str,
        api_key: Password | str = "",
        model: str = MODEL_EXAMPLE,
        timout_single_request: int = 10000,
        instruct_output_path: str = DEFAULT_INSTRUCTION_OUTPUT_PATH,
        prompt_template: str = PROMPT_TEMPLATE_EXAMPLE,
        instruct_tempalte: str = INSTRUCTION_EXAMPLE,
    ) -> None:
        self.base_url = url
        self.timout_single_request = timout_single_request
        self.api_key = api_key if isinstance(api_key, str) else api_key.decrypt()
        if self.api_key == "":
            self.api_key = "dummy-key"
        self.instruct_output_path = instruct_output_path
        self.prompt_template = prompt_template
        self.instruct_template = instruct_tempalte
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.instruct_report = ExecutionReport()
        self.instruct_report.operation = "executing"
        self.instruct_report.operation_desc = "instructions executed"
        self._setup_ports()

    def _setup_ports(self) -> None:
        """Configure input and output ports depending on the configuration"""
        self.input_ports = FixedNumberOfInputs([FlexibleSchemaPort()])
        output_paths = [EntityPath(path=self.instruct_output_path)]
        output_schema = EntitySchema(type_uri="entity", paths=output_paths)
        self.output_port = FixedSchemaPort(schema=output_schema)

    def _generate_output_schema(self, input_schema: EntitySchema) -> EntitySchema:
        """Get output schema"""
        paths = list(input_schema.paths).copy()
        paths.append(EntityPath(self.instruct_output_path))
        return EntitySchema(type_uri=input_schema.type_uri, paths=paths)

    def _cancel_workflow(self) -> bool:
        """Cancel workflow"""
        try:
            if self.execution_context.workflow.status() == "Canceling":
                self.log.info("End task (Cancelled Workflow).")
                return True
        except AttributeError:
            pass
        return False

    def _instruct_report_update(self, n: int) -> None:
        """Update report"""
        if hasattr(self.execution_context, "report"):
            self.instruct_report.entity_count += n
            self.execution_context.report.update(self.instruct_report)

    @staticmethod
    def _entity_to_dict(paths: Sequence[EntityPath], entity: Entity) -> dict[str, list[str]]:
        """Create a dict representation of an entity"""
        entity_dic = {}
        for key, value in zip(paths, entity.values, strict=False):
            entity_dic[key.path] = list(value)
        return entity_dic

    @staticmethod
    def _template_fill(template: str, variable: str, value: str) -> str:
        """Fill the template replacing the variable by the given value"""
        variable_map: dict = {}
        variable_map[variable] = value
        return Template(template).safe_substitute(variable_map)

    def _process_entities(self, entities: Entities) -> Generator[Entity]:
        """Process an entity list (chunked), yielding new entity objects"""
        entity: Entity
        self._instruct_report_update(0)
        for entity in entities.entities:
            entity_dict = self._entity_to_dict(entities.schema.paths, entity)
            instruct: str = self._template_fill(
                self.instruct_template, "entity", json.dumps(entity_dict)
            )
            messages = json.loads(self.prompt_template)
            instruction = messages[1]["content"]
            instruction_user: str = self._template_fill(instruction, "instruct", instruct)
            messages[1]["content"] = instruction_user
            completion = self.client.chat.completions.create(model=self.model, messages=messages)
            entity_dict[self.instruct_output_path] = [completion.choices[0].message.content or ""]
            values = list(entity_dict.values())
            self._instruct_report_update(1)
            if self._cancel_workflow():
                break
            yield Entity(uri=entity.uri, values=values)

    def execute(
        self,
        inputs: Sequence[Entities],
        context: ExecutionContext,
    ) -> Entities:
        """Run the workflow operator."""
        self.log.info("Start")
        self.execution_context = context
        first_input: Entities = inputs[0]
        if self.instruct_output_path in [_.path for _ in first_input.schema.paths]:
            raise SamePathError(self.instruct_output_path)
        entities = self._process_entities(first_input)
        schema = self._generate_output_schema(first_input.schema)
        self.log.info("End")
        return Entities(entities=entities, schema=schema)
