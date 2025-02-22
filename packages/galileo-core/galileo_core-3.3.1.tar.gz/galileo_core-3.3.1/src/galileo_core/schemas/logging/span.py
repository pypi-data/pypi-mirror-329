from json import dumps
from typing import Any, Dict, List, Literal, Optional, Sequence, Union

from pydantic import Field, field_validator
from typing_extensions import Annotated

from galileo_core.schemas.logging.llm import Message
from galileo_core.schemas.logging.step import BaseStep, Metrics, StepType
from galileo_core.schemas.shared.document import Document
from galileo_core.utils.json import PydanticJsonEncoder


class StepWithChildSpans(BaseStep):
    spans: List["Span"] = Field(default_factory=list, description="Child spans.")

    def add_child_spans(self, spans: Sequence["Span"]) -> None:
        self.spans.extend(spans)

    def add_child_span(self, span: "Span") -> None:
        self.add_child_spans([span])


class BaseWorkflowSpan(BaseStep):
    type: Literal[StepType.workflow] = Field(default=StepType.workflow, description="Type: must be `workflow`")


class WorkflowSpan(BaseWorkflowSpan, StepWithChildSpans):
    pass


class LlmMetrics(Metrics):
    num_input_tokens: Optional[int] = Field(default=None, description="Number of input tokens.")
    num_output_tokens: Optional[int] = Field(default=None, description="Number of output tokens.")
    num_total_tokens: Optional[int] = Field(default=None, description="Total number of tokens.")
    time_to_first_token_ns: Optional[int] = Field(
        default=None, description="Number of seconds until the first token was generated."
    )

    class Config:
        extra = "allow"  # Allows additional arbitrary key-value pairs


class LlmSpan(BaseStep):
    type: Literal[StepType.llm] = Field(default=StepType.llm, description="Type: must be `llm`")
    input: Sequence[Message] = Field(description="Input to the LLM step.")
    output: Message = Field(description="Output of the LLM step.")
    metrics: LlmMetrics = Field(default_factory=LlmMetrics, description="Metrics used by the LLM step.")
    tools: Optional[Sequence[Dict[str, Any]]] = Field(
        default=None, description="List of available tools passed to the LLM on invocation."
    )
    model: Optional[str] = Field(default=None, description="Model used for this step.")
    temperature: Optional[float] = Field(default=None, description="Temperature used for generation.")
    finish_reason: Optional[str] = Field(default=None, description="Reason for finishing.")

    @field_validator("tools", mode="after")
    def validate_tools_serializable(cls, val: Optional[Sequence[Dict[str, Any]]]) -> Optional[Sequence[Dict[str, Any]]]:
        # Make sure we can dump input/output to json string.
        dumps(val, cls=PydanticJsonEncoder)
        return val


class RetrieverSpan(BaseStep):
    type: Literal[StepType.retriever] = Field(default=StepType.retriever, description="Type: must be `retriever`")
    input: str = Field(description="Input query to the retriever.")
    output: List[Document] = Field(description="Documents retrieved from the retriever.")

    @field_validator("output", mode="before")
    def set_output(cls, value: Union[List[Dict[str, str]], List[Document]]) -> List[Document]:
        if isinstance(value, list):
            if all(isinstance(doc, dict) for doc in value):
                parsed = [Document.model_validate(doc) for doc in value]
            elif all(isinstance(doc, Document) for doc in value):
                parsed = [Document.model_validate(doc) for doc in value]
            else:
                raise ValueError("Retriever output must be a list of dicts, or a list of Documents.")
            return parsed
        raise ValueError("Retriever output must be a list of dicts or a list of Documents.")


class ToolSpan(BaseStep):
    type: Literal[StepType.tool] = Field(default=StepType.tool, description="Type: must be `tool`")
    input: str = Field(description="Input to the tool step.")
    output: Optional[str] = Field(default=None, description="Output of the tool step.")
    tool_call_id: Optional[str] = Field(default=None, description="Tool call ID.")


Span = Annotated[Union[WorkflowSpan, LlmSpan, RetrieverSpan, ToolSpan], Field(discriminator="type")]

StepWithChildSpans.model_rebuild()

SpanStepTypes = [step_type.value for step_type in StepType if step_type != StepType.trace]
