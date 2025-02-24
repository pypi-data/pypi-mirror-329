from opentelemetry.sdk.resources import Resource

from .frameworks.anthropic import AnthropicInstrumentor
from .frameworks.bedrock import BedrockInstrumentor
from .frameworks.crewai import CrewAIInstrumentor
from .frameworks.dspy import DSPyInstrumentor
from .frameworks.groq import GroqInstrumentor
from .frameworks.haystack import HaystackInstrumentor
from .frameworks.instructor import InstructorInstrumentor
from .frameworks.langchain import LangChainInstrumentor
from .frameworks.litellm import LiteLLMInstrumentor
from .frameworks.llama_index import LlamaIndexInstrumentor
from .frameworks.mistralai import MistralAIInstrumentor
from .frameworks.openai import OpenAIInstrumentor
from .frameworks.vertexai import VertexAIInstrumentor
from .otel import (
    PROJECT_NAME,
    PROJECT_TYPE,
    PROJECT_VERSION_NAME,
    BatchSpanProcessor,
    HTTPSpanExporter,
    SimpleSpanProcessor,
    TracerProvider,
    register,
)

__all__ = [
    "TracerProvider",
    "SimpleSpanProcessor",
    "BatchSpanProcessor",
    "HTTPSpanExporter",
    "Resource",
    "PROJECT_NAME",
    "PROJECT_TYPE",
    "PROJECT_VERSION_NAME",
    "register",
    "LangChainInstrumentor",
    "OpenAIInstrumentor",
    "AnthropicInstrumentor",
    "BedrockInstrumentor",
    "CrewAIInstrumentor",
    "DSPyInstrumentor",
    "GroqInstrumentor",
    "HaystackInstrumentor",
    "InstructorInstrumentor",
    "LiteLLMInstrumentor",
    "LlamaIndexInstrumentor",
    "MistralAIInstrumentor",
    "VertexAIInstrumentor",
]
