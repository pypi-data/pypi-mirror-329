import os
import subprocess
from PyInquirer import prompt
from pygen_cli.generator import create_project_structure

def ask_user():
    """Ask user for project details interactively."""
    questions = [
        {
            'type': 'input',
            'name': 'project_name',
            'message': 'Enter project name:',
        },
        {
            'type': 'confirm',
            'name': 'venv',
            'message': 'Do you want to create a virtual environment (Python only)?',
            'default': True
        },
        {
            'type': 'input',
            'name': 'structure',
            'message': 'Enter folder structure (comma-separated, e.g., app.py, templates/, static/):',
        }
    ]
    return prompt(questions)

def create_project():
    """Main function to create project."""
    user_input = ask_user()

    project_name = user_input['project_name']
    venv = user_input['venv']
    structure = user_input['structure'].split(',') if user_input['structure'] else []

    # Create the main project folder
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"✅ Created project: {project_name}")
    else:
        print("⚠️ Project already exists!")
        return

    # Create virtual environment if selected
    if venv:
        venv_path = os.path.join(project_name, "venv")
        subprocess.run(["python", "-m", "venv", venv_path])
        print("✅ Virtual environment created.")

    # Generate the folder & file structure
    create_project_structure(project_name, structure)
    print("✅ Project structure created successfully!")

if __name__ == '__main__':
    create_project()
