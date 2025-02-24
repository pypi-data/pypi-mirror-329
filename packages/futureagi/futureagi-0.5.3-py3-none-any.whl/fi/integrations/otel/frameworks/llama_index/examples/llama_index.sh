echo "Running Llamaindex examples using Poetry..."

# Array of Python files to run
files=(
    "agent_calculator_tools.py"
    "chat_engine_stream.py"
    "chroma_query_engine.py"
    "ingestion_pipeline.py"
    "multimodal_stream_chat.py"
    "openai_stream_chat.py"
    "text_to_sql.py"
    "workflow.py"
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