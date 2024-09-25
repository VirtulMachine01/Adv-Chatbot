import os
import glob

def manage_chat_sessions_folder(folder_path="chat_sessions", max_files=10):
    # Get all the JSON files in the folder
    json_files = glob.glob(os.path.join(folder_path, "*.json"))

    # Sort the files by creation time (oldest first)
    json_files.sort(key=os.path.getctime)

    # Check if the number of files exceeds the max_files limit
    if len(json_files) > max_files:
        # Delete the oldest files (those that came first)
        for file_to_delete in json_files[:-max_files]:
            try:
                os.remove(file_to_delete)
                print(f"Deleted old chat file: {file_to_delete}")
            except Exception as e:
                print(f"Error deleting file {file_to_delete}: {e}")
