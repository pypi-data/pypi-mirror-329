echo "Running Groq examples using Poetry..."

# Array of Python files to run
files=(
    "async_chat_completions.py"
    "chat_completions.py"
    "chat_completions_with_tool.py"
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