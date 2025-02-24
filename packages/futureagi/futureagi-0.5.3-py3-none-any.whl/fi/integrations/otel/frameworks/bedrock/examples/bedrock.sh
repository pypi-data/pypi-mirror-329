echo "Running Bedrock examples using Poetry..."

files=(
    "bedrock_converse.py"
    "bedrock_multimodal.py"
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