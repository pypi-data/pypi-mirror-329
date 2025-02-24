echo "Running OpenAI examples using Poetry..."

# Array of Python files to run
files=(
    "chat_completions.py"
    "chat_completions_async_stream.py" # no raw ouptut
    "chat_completions_async_stream_with_raw_response.py" # "raw.output": "<openai.AsyncStream object at 0x15d86a560>"
    "chat_completions_multimodal.py" 
    "chat_completions_stream.py" # no raw ouptut
    "chat_completions_stream_with_raw_response.py" # "raw.output": "<openai.AsyncStream object at 0x15d86a560>"
    "chat_completions_with_function_calling.py"
    "chat_completions_with_raw_response.py"
    "chat_completions_with_streaming_response.py" # no raw ouptut
    "embeddings.py"
    "openai_tool.py"
)

# Loop through each file and run it
for file in "${files[@]}"; do
    echo "----------------------------------------"
    echo "Running $file..."
    echo "----------------------------------------"
    poetry run python3 "$file"
    echo -e "\n"
done

echo "All examples completed!"