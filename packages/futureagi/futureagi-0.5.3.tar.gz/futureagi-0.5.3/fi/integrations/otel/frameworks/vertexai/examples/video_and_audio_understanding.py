import vertexai
from vertexai.generative_models import GenerativeModel, Part

from fi.integrations.otel import VertexAIInstrumentor, register
from fi.integrations.otel.types import (
    EvalName,
    EvalSpanKind,
    EvalTag,
    EvalTagType,
    ProjectType,
)

# Configure trace provider with custom evaluation tags
eval_tags = [
    EvalTag(
        eval_name=EvalName.DETERMINISTIC_EVALS,
        value=EvalSpanKind.TOOL,
        type=EvalTagType.OBSERVATION_SPAN,
        config={
            "multi_choice": False,
            "choices": ["Yes", "No"],
            "rule_prompt": "Evaluate if the response is correct",
        },
        custom_eval_name="<custom_eval_name>",
    )
]

# Configure trace provider with custom evaluation tags
trace_provider = register(
    project_type=ProjectType.EXPERIMENT,
    eval_tags=eval_tags,
    project_name="FUTURE_AGI",
    project_version_name="v1",
)

# Initialize the VertexAI instrumentor
VertexAIInstrumentor().instrument(tracer_provider=trace_provider)

vertexai.init(
    project="project_name",
)
model = GenerativeModel("gemini-1.5-flash")
prompt = """Provide a description of the video.
The description should also contain anything important which people say in the video.
"""
video_file_uri = "gs://cloud-samples-data/generative-ai/video/pixel8.mp4"
video_file = Part.from_uri(video_file_uri, mime_type="video/mp4")
contents = [video_file, prompt]

if __name__ == "__main__":
    response = model.generate_content(contents)
    print(response)
