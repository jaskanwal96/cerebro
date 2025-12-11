import file_reader
# chunks = [
#     {
#         "text": "chunk 1 text",
#         "source_file": "meeting_notes_20251119.txt",
#         "chunk_index": 0,
#         "file_path": "/path/to/meeting_notes_20251119.txt"
#     },
#     {
#         "text": "chunk 2 text", 
#         "source_file": "meeting_notes_20251119.txt",
#         "chunk_index": 1,
#         "file_path": "/path/to/meeting_notes_20251119.txt"
#     }
# ]

def chunk_text(source_file, file_data, file_path=None, chunk_size=500, overlap=50):
    """
    Split text into chunks with metadata
    
    Args:
        source_file: Name of the source file (e.g., "test.txt")
        file_data: The text content to chunk
        file_path: Full path to the file (optional)
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
    
    Returns:
        List of dicts with structure:
        {
            "text": "chunk text",
            "source_file": "test.txt",
            "chunk_index": 0,
            "file_path": "/path/to/test.txt"
        }
    """
    if len(file_data) < chunk_size:
        # Single chunk - no need to split
        return [{
            "text": file_data,
            "source_file": source_file,
            "chunk_index": 0,
            "file_path": file_path or source_file
        }]
    
    # Generate chunks with overlap
    chunk_index = 0
    chunks = []
    for i in range(overlap, len(file_data), chunk_size):
        chunk_text_content = file_data[i-overlap:i+chunk_size]
        
        chunks.append({
            "text": chunk_text_content,
            "source_file": source_file,
            "chunk_index": chunk_index,
            "file_path": file_path or source_file
        })
        chunk_index += 1
    
    return chunks


# files = file_reader.read_files_in_folder('../../assets')
# chunk_text('testing_learning_guide', files['testing_learning_guide.md'])