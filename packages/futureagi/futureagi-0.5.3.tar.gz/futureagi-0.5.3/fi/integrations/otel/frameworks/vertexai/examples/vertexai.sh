echo "Running Vertex AI examples using Poetry..."

# Array of Python files to run
files=(
    "audio_transcription.py"
    "audio_understanding.py"
    "basic_generation.py"
    "chat.py"
    "document_understanding.py"
    "function_calling.py"
    "image_from_cloud_storage.py"
    "system_instructions.py"
    "vertexai.model.count_tokens.py"
    "vertexai.model.generate_content.py"
    "video_and_audio_understanding.py"
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