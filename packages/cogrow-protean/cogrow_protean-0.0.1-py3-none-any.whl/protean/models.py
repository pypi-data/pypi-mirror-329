from enum import Enum
from typing import Optional, Dict, Type, TypeVar, Literal

from pydantic import BaseModel, TypeAdapter, ConfigDict, Field
from pydantic.alias_generators import to_camel

ModelT = TypeVar('ModelT', bound=BaseModel)


def cast_to_base_model(data: str, expected_type: Type[ModelT]):
    return TypeAdapter(expected_type).validate_json(data, strict=True)


class ProteanBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
        frozen=True,
    )


class ToolDefinition(ProteanBaseModel):
    name: str
    description: str
    input_schema: Dict[str, object]


class ClientTools(ProteanBaseModel):
    parallel_calls: bool
    definitions: list[ToolDefinition]


class QuestionRequest(ProteanBaseModel):
    user_message: str
    """The user prompt to generate response for."""

    assistant_id: Optional[str] = None
    """The assistant ID to use when generating the response."""

    model_id: Optional[str] = None
    """The ID of the model to use when generating the response."""

    system_message: Optional[str] = None
    """The system message to use when generating the response."""

    datasets: Optional[list[str]] = None
    """
    The datasets to be used for RAG purposes during generation. Expected values are either dataset GUID or '*', where 
    '*' implies to use all datasets that are available to you. 
    """

    limit: Optional[int] = Field(3, gt=0)
    """The maximum number of dataset chunks to include into the context during generation."""

    relevance_threshold: Optional[float] = Field(0.8, gt=0.0, le=1.0)
    """
    Cut off point for the relevance of dataset chunks to the provided user_message. Accepts values from 0.1 to 1.0 where 
    higher value implies higher level of relevance of the dataset chunks to the provided user_message. 
    """

    temperature: Optional[float] = Field(0.1, ge=0.0, le=1.0)
    """
    Affects the level of creativity that should be applied when generating response. Accepts values from 0.0 to 1.0 
    where higher value implies higher level of creativity applied during generation.
    """

    client_tools: Optional[ClientTools] = None
    """List of functions the model may generate JSON inputs for."""


class ClientToolCall(ProteanBaseModel):
    name: str
    arguments: str


class QuestionResponse(ProteanBaseModel):
    assistant_message: Optional[str] = None
    dataset_ids: Optional[list[str]] = None
    client_tool_calls: Optional[list[ClientToolCall]] = None


class ResourceType(Enum):
    CONVERSATION = 'CONVERSATION'
    DATASET = 'DATASET'
    APIKEY = 'APIKEY'
    ASSISTANT = 'ASSISTANT'
    MODEL = 'MODEL'


class VectorSearchRequest(ProteanBaseModel):
    query: str
    """The query to search against the vector datasets."""

    limit: Optional[int] = Field(3, gt=0)
    """The maximum number of dataset chunks to return for the query."""

    resource_type: Literal[ResourceType.DATASET] = ResourceType.DATASET.value
    """The type of the resource to run the query against. At this point it is hardcoded to DATASET."""

    resource_ids: Optional[list[str]] = None
    """The dataset IDs to run the query against."""

    relevance_threshold: Optional[float] = Field(0.8, gt=0.0, le=1.0)
    """
    Cut off point for the relevance of dataset chunks to the provided user_message. Accepts values from 0.1 to 1.0 where
    higher value implies higher level of relevance of the dataset chunks to the provided user_message.
    """


class VectorDocument(ProteanBaseModel):
    id: str
    text: str
    metadata: dict[str, object]
    score: float


class VectorSearchResponse(ProteanBaseModel):
    documents: list[VectorDocument] = None
