echo "Running haystack examples using Poetry..."

# Array of Python files to run
files=(
    "building_fallbacks_with_conditional_routing.py"
    "cohere_reranker.py"
    "filtering_documents_with_metadata.py"
    "haystack_rag_pipeline.py"
    "qa_rag_pipeline.py"
    "tool_calling.py"
    "web_questions.py"
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