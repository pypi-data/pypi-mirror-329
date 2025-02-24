echo "Running Langchain examples using Poetry..."

# Array of Python files to run
files=(
    "chain_metadata.py" # no input 
    "chat_prompt_template.py" # no input for some spans
    "custom_retriever.py" # try for some big document
    "exchange_rate_tool.py"
    "langgraph_agent_supervisor.py"
    "multimodal.py"
    "openai_chat_stream.py"
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