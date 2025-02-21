# Aitronos-CLI

A command-line interface tool for streamlining AI development workflows.

## For Users

### Installation

You can install Aitronos-CLI directly from PyPI:

```bash
pip install aitronos-cli
```

Or from GitHub:

```bash
pip install git+https://github.com/Freddy-Development/Aitronos-CLI.git
```

### Usage

After installation, you can use the `aitronos` command in your terminal:

```bash
# Initialize a basic project structure
aitronos streamline init my-project

# Create a hello world example project
aitronos streamline hello-world my-hello-project

# Create a hello world with parameters
aitronos streamline hello-world-parameter my-param-project

# Create a template project
aitronos streamline template my-template-project
```

### Project Structure

After initialization, your project structure will look like this:

```
my-project/
├── .aitronos/
│   └── config.yaml
├── src/
│   └── main.py
└── requirements.txt
```

## For Developers

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aitronos-alpha.git
cd aitronos-alpha
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
```

### Development Workflow

1. Make changes to the code in the `aitronos_alpha` directory

2. Test your changes locally:
```bash
# Test the CLI
aitronos streamline init test-project

# If the command is not found, you can also use:
python -m aitronos_alpha streamline init test-project
```

3. Run tests:
```bash
python -m pytest
```

### Project Structure for Developers

```
aitronos_alpha/
├── commands/
│   ├── hello_world_project/
│   ├── hellow_world_to_perameter/
│   ├── template/
│   └── streamline.py
├── cli.py
├── utils.py
└── __init__.py
```

### Adding New Commands

1. Create a new command module in the `commands` directory
2. Update `cli.py` to include your new command
3. Add tests for your command
4. Update documentation

## Requirements

- Python 3.8 or higher
- pip package manager

## Available Commands

- `aitronos streamline init <project-name>` - Initialize a basic project structure
- `aitronos streamline hello-world <project-name>` - Create a hello world example project
- `aitronos streamline hello-world-parameter <project-name>` - Create a hello world with parameters
- `aitronos streamline template <project-name>` - Create a template project

## License

This project is licensed under the MIT License - see the LICENSE file for details

