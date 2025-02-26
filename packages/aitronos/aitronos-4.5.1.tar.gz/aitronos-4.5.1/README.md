# Aitronos Python Package

A Python package for interacting with the Freddy API and other Aitronos services. This package provides a command-line interface (CLI) for managing Aitronos projects and services.

## Installation

```bash
pip install aitronos
```

## CLI Commands

The `aitronos` CLI provides several commands for project initialization:

### Basic Project Initialization

```bash
aitronos init <project_name>
```

Creates a new project with the standard Aitronos project structure:
- `src/` - Source code directory
- `resources/` - Project resources
- `config.freddy.json` - Configuration file
- `requirements.txt` - Python dependencies
- `documentation.txt` - Project documentation
- `execution_log.json` - Execution logs

### Hello World Example Project

```bash
aitronos init-hello-world <project_name>
```

Creates a basic Hello World example project that includes:
- Basic project structure
- Simple Click-based CLI example in `src/main.py`
- Pre-configured `requirements.txt` with Click dependency
- Example README.md with usage instructions

### Hello World with Parameters Example

```bash
aitronos init-hello-world-params <project_name>
```

Creates an advanced Hello World example that demonstrates CLI parameter handling:
- Complete project structure
- Advanced Click-based CLI example with parameter handling
- Example of using command-line options and arguments
- Detailed README.md with usage examples

### Interactive Hello World Command

```bash
aitronos hello [OPTIONS]
```

A simple interactive command to demonstrate CLI parameter handling.

Options:
- `--name, -n TEXT`: Name to greet (default: "World")
- `--count, -c INTEGER`: Number of times to greet (default: 1)

Example usage:
```bash
# Basic usage
aitronos hello

# Custom name
aitronos hello --name Alice

# Multiple greetings
aitronos hello --name Bob --count 3
```

## Development

To set up the development environment:

1. Clone the repository:
```bash
git clone https://github.com/Freddy-Development/aitronos-python-package.git
cd aitronos-python-package
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## Support

For support, please open an issue on the GitHub repository or contact the development team.

## Library Usage

```python
from Aitronos import Aitronos, Message, MessageRequestPayload

# Initialize with API key (recommended)
client = Aitronos(api_key="your_api_key")

# Or with username/password
client = Aitronos(username="your_username", password="your_password")

# Use the assistant messaging
messaging = client.assistant_messaging
response = messaging.execute_run(
    MessageRequestPayload(
        organization_id=123,
        assistant_id=456,
        messages=[Message(content="Hello!", role="user")]
    )
)
```

## Command Line Interface (CLI)

The Aitronos package includes a powerful CLI for common operations and project management.

### Configuration

Before using the CLI, set up your configuration:

1. Create a `config.json` file in your project root:
```json
{
    "test_key": "your_api_key",
    "test_org_id": your_organization_id,
    "test_assistant_id": your_assistant_id,
    "test_username": "your_username",
    "test_password": "your_password"
}
```

2. Add `config.json` to your `.gitignore` to keep credentials secure:
```bash
echo "config.json" >> .gitignore
```

### Available Commands

1. Initialize a new project:
```bash
aitronos init my_project
```
This creates a new project with the following structure:
```
my_project/
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
    │   └── my_project.py
    └── tests/
        └── test_script.py
```

2. Run the hello world example:
```bash
aitronos hello
```
Tests your setup with a simple hello world example using the Aitronos API.

3. Use StreamLine functionality:
```bash
# Interactive mode
aitronos streamline

# Process a file
aitronos streamline --input input.txt --output output.txt
```

### Project Templates

When initializing a new project with `aitronos init`, you get:
- Basic project structure
- Configuration files
- Example code
- Resource templates
- Test setup

The generated project includes:
- Logging setup
- Error handling
- User management
- API integration
- Basic test structure

### Development Workflow

1. Initialize a new project:
```bash
aitronos init my_aitronos_project
cd my_aitronos_project
```

2. Update the configuration:
```bash
# Edit config.json with your credentials
vim config.json
```

3. Install project dependencies:
```bash
pip install -r requirements.txt
```

4. Start developing:
```bash
# Your main code is in src/main/my_aitronos_project.py
# Tests are in src/tests/
```

## Development

To contribute or modify the package:

1. Clone the repository:
```bash
git clone https://github.com/Freddy-Development/aitronos-python-package.git
cd aitronos-python-package
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
- Open an [issue](https://github.com/Freddy-Development/aitronos-python-package/issues)
- Contact us at support@aitronos.com

## Security

To report security vulnerabilities, please email security@aitronos.com 
