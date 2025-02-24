echo "Running Mistral AI examples using Poetry..."

# Array of Python files to run
files=(
    "agent_completions.py"
    "chat_completions.py"
    "chat_completions_async.py"
    "chat_completions_async_streaming.py"
    "chat_completions_streaming.py"
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