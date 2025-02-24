echo "Running Anthropic examples using Poetry..."

# Array of Python files to run
files=(
    "anthropic_examples.py"
    "chat_completions.py"
    "end_to_end_tool_use.py"
    "multiple_tool_calling.py"
    "sync_completions.py"
    "sync_messages.py"
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