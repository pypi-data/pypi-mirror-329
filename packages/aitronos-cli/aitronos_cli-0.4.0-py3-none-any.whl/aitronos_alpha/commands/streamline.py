import os
import shutil
import sys


def clone_sample_project(project_name):
    """
    Clones the sample project structure to a new project with the given project name.
    """
    sample_project_path = "sample_project"  # Directory with pre-configured structure and files

    if not os.path.exists(sample_project_path):
        print(f"Error: 'sample_project' folder does not exist. Please create and customize it first.")
        sys.exit(1)

    # Define destination path for the new project
    destination_path = os.path.join(os.getcwd(), project_name)

    try:
        # Copy entire sample_project to the destination path
        shutil.copytree(sample_project_path, destination_path)

        print(f"Project '{project_name}' created successfully from sample_project.")
    except Exception as e:
        print(f"Error: {str(e)}")


def handle_streamLine_command(args):
    """
    Processes the streamLine command.
    """
    if len(args) < 1:
        print("Usage: aitronos streamLine init <project_name>")
        return

    subcommand = args[0]

    if subcommand == "init":
        if len(args) < 2:
            print("Please provide a project name.")
        else:
            clone_sample_project(args[1])
    else:
        print(f"Unknown subcommand: {subcommand}")