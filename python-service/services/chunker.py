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

def chunk_text(source_file, file_data, chunk_size = 500, overlap = 50):
    chunks_array = [file_data[i - overlap:i+chunk_size] for i in range(overlap, len(file_data), chunk_size)]
    for chunks in chunks_array:
        print(chunks)
        print('\n\n\n')
    return chunks_array


files = file_reader.read_files_in_folder('../../assets')
chunk_text('testing_learning_guide', files['testing_learning_guide.md'])