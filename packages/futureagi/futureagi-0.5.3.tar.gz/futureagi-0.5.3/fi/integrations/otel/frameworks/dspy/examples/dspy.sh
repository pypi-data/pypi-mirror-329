echo "Running DSpy examples using Poetry..."

# Array of Python files to run
files=(
    "dspy_basic_qa.py"
    "lm.py"
    "rag_module.py"
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