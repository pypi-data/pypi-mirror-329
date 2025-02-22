# Aitronos Python Package

A Python package for interacting with the Aitronos API, providing both a library interface and a command-line tool.

## Installation

### From PyPI (Recommended)
```bash
pip install aitronos
```

### From Source
```bash
git clone https://github.com/Freddy-Development/aitronos-python-package.git
cd aitronos-python-package
pip install -e .
```

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
