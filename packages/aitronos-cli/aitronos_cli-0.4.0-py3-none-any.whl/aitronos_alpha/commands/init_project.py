from pathlib import Path
import os
import shutil
import json
import aitronos_logger
from resources import CurrentUser

logger = aitronos_logger.Logger()

def create_project_structure(project_name: str):
    """Creates a new project with the standard Aitronos project structure."""
    try:
        # Start time estimation for the whole process
        logger.info("Starting project initialization", component="ProjectInit", progress=0, remaining_time_seconds=10)
        
        # Get current working directory
        base_path = Path.cwd()
        project_path = base_path / project_name
        
        # Create main project directory
        project_path.mkdir(exist_ok=True)
        logger.info(f"Created project directory: {project_name}", component="ProjectInit", progress=20, remaining_time_seconds=8)
        
        # Create project structure
        src_path = project_path / "src"
        src_path.mkdir(exist_ok=True)
        
        main_path = src_path / "main"
        main_path.mkdir(exist_ok=True)
        
        tests_path = src_path / "tests"
        tests_path.mkdir(exist_ok=True)
        
        resources_path = project_path / "resources"
        resources_path.mkdir(exist_ok=True)
        
        # Create main Python file
        main_file = main_path / f"{project_name}.py"
        create_main_file(main_file, project_name)
        logger.info("Created main project file", component="ProjectInit", progress=40, remaining_time_seconds=6)
        
        # Create test file
        test_file = tests_path / "test_script.py"
        create_test_file(test_file)
        
        # Create resources files
        create_resources_files(resources_path)
        logger.info("Created resource files", component="ProjectInit", progress=60, remaining_time_seconds=4)
        
        # Create config and documentation files
        create_config_file(project_path)
        create_documentation_file(project_path)
        create_execution_log(project_path)
        
        # Create requirements.txt
        requirements_file = project_path / "requirements.txt"
        with open(requirements_file, "w") as f:
            f.write("aitronos>=0.1.0\n")
        
        logger.info("Project initialization completed successfully", component="ProjectInit", progress=100, remaining_time_seconds=0)
        return f"Successfully initialized project: {project_name}"
        
    except Exception as e:
        logger.error(f"Project initialization failed: {str(e)}", component="ProjectInit", severity=4, exc=e)
        raise

def create_main_file(file_path: Path, project_name: str):
    """Creates the main Python file with boilerplate code."""
    template = f'''from Aitronos import Aitronos, MessageRequestPayload, Message
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
import aitronos_logger
from resources import CurrentUser

logger = aitronos_logger.Logger()

def main():
    try:
        # Start time estimation for the whole process
        logger.info("Starting {project_name} execution", component="{project_name}", progress=0, remaining_time_seconds=5)
        
        # Initialize user
        current_user = CurrentUser()
        user = current_user.user
        logger.info(f"User authenticated: {{user.full_name}}", component="UserManagement", progress=20, remaining_time_seconds=4)
        
        # Initialize Aitronos
        assistant_messaging = Aitronos(api_key=user.user_token).AssistantMessaging
        logger.info("Aitronos assistant messaging initialized", component="AitronosSetup", progress=40, remaining_time_seconds=3)
        
        # Add your custom code here
        
        logger.info("Project execution completed", component="{project_name}", progress=100, remaining_time_seconds=0)
        return "Project execution successful"
        
    except Exception as e:
        logger.error(f"Project execution failed: {{str(e)}}", component="{project_name}", severity=4, exc=e)
        raise

if __name__ == "__main__":
    print(main())
'''
    with open(file_path, "w") as f:
        f.write(template)

def create_test_file(file_path: Path):
    """Creates a basic test file."""
    content = '''import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

class TestScript(unittest.TestCase):
    def test_example(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
'''
    with open(file_path, "w") as f:
        f.write(content)

def create_resources_files(resources_path: Path):
    """Creates the resources directory with necessary files."""
    # Create __init__.py
    init_file = resources_path / "__init__.py"
    init_file.touch()
    
    # Create current_user.py
    current_user_content = '''from pathlib import Path
import json

class User:
    def __init__(self, user_data):
        self.user_id = user_data.get('user_id')
        self.full_name = user_data.get('full_name')
        self.user_token = user_data.get('user_token')
        self.current_organization_id = user_data.get('current_organization_id')

class CurrentUser:
    def __init__(self):
        self.user = self._load_user()
    
    def _load_user(self):
        user_data_path = Path(__file__).parent / 'user_data.json'
        with open(user_data_path) as f:
            user_data = json.load(f)
        return User(user_data)
'''
    with open(resources_path / "current_user.py", "w") as f:
        f.write(current_user_content)
    
    # Create helpers.py
    helpers_content = '''# Add helper functions here
'''
    with open(resources_path / "helpers.py", "w") as f:
        f.write(helpers_content)
    
    # Create user_data.json
    user_data = {
        "user_id": "default_user",
        "full_name": "Default User",
        "user_token": "your_token_here",
        "current_organization_id": "default_org"
    }
    with open(resources_path / "user_data.json", "w") as f:
        json.dump(user_data, f, indent=4)
    
    # Create org_data.json
    org_data = {
        "organization_id": "default_org",
        "name": "Default Organization"
    }
    with open(resources_path / "org_data.json", "w") as f:
        json.dump(org_data, f, indent=4)

def create_config_file(project_path: Path):
    """Creates the config.freddy.json file."""
    config = {
        "version": "1.0.0",
        "environment": "development",
        "settings": {
            "logging_level": "INFO"
        }
    }
    with open(project_path / "config.freddy.json", "w") as f:
        json.dump(config, f, indent=4)

def create_documentation_file(project_path: Path):
    """Creates the documentation.txt file."""
    content = '''Project Documentation

This project was created using the Aitronos CLI tool.

Project Structure:
├── config.freddy.json
├── documentation.txt
├── execution_log.json
├── requirements.txt
├── resources/
│   ├── __init__.py
│   ├── current_user.py
│   ├── helpers.py
│   ├── org_data.json
│   └── user_data.json
└── src/
    ├── main/
    │   └── main.py
    └── tests/
        └── test_script.py
'''
    with open(project_path / "documentation.txt", "w") as f:
        f.write(content)

def create_execution_log(project_path: Path):
    """Creates the execution_log.json file."""
    log = {
        "executions": []
    }
    with open(project_path / "execution_log.json", "w") as f:
        json.dump(log, f, indent=4)

def init_project(project_name: str):
    """Main function to initialize a new Aitronos project."""
    return create_project_structure(project_name) 