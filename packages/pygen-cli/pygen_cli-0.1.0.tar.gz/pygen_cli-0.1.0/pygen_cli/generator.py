import os

def create_project_structure(root, structure_list):
    """Create folders and files based on user input."""
    for path in structure_list:
        full_path = os.path.join(root, path.strip())

        if path.endswith("/"):  # If it ends with `/`, it's a folder
            os.makedirs(full_path, exist_ok=True)
        else:  # Otherwise, it's a file
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                pass  # Create an empty file

    print("📂 Project structure applied.")
