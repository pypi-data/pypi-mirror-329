from pathlib import Path
import os
import shutil
import json
import aitronos_logger

logger = aitronos_logger.Logger()

def create_project_structure(project_name: str, template_type: str = "default"):
    """Creates a new project with the standard Aitronos project structure."""
    try:
        # Get current working directory and template directory
        base_path = Path.cwd()
        project_path = base_path / project_name
        template_path = Path(__file__).parent / "template"
        
        if template_type == "hello_world":
            template_path = Path(__file__).parent / "hello_world_project"
        elif template_type == "hello_world_params":
            template_path = Path(__file__).parent / "hello_world_with_parameters"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template directory not found at {template_path}")
        
        # Create main project directory
        project_path.mkdir(exist_ok=True)
        
        # Copy template directory contents to new project
        def copy_template(src_dir, dst_dir):
            """Helper function to copy template directory while skipping __pycache__ and .DS_Store"""
            for item in src_dir.iterdir():
                if item.name in ['__pycache__', '.DS_Store']:
                    continue
                    
                dst_path = dst_dir / item.name
                if item.is_dir():
                    dst_path.mkdir(exist_ok=True)
                    copy_template(item, dst_path)
                else:
                    shutil.copy2(item, dst_path)
        
        copy_template(template_path, project_path)
        
        # If it's a hello world project, create additional files
        if template_type == "hello_world":
            # Create src directory if it doesn't exist
            src_dir = project_path / "src"
            src_dir.mkdir(exist_ok=True)
            
            # Create main.py with hello world example
            main_py = src_dir / "main.py"
            with open(main_py, "w") as f:
                f.write("""import click

@click.command()
@click.option('--name', '-n', default='World', help='Name to greet')
@click.option('--count', '-c', default=1, type=int, help='Number of times to greet')
def hello(name, count):
    \"\"\"Simple Hello World program with parameters.\"\"\"
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == '__main__':
    hello()
""")
            
            # Create requirements.txt
            requirements_txt = project_path / "requirements.txt"
            with open(requirements_txt, "w") as f:
                f.write("click>=8.0.0\n")
            
            # Create README.md
            readme_md = project_path / "README.md"
            with open(readme_md, "w") as f:
                f.write(f"""# {project_name}

A simple Hello World example project using Click for command-line interface.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic usage
python src/main.py

# With custom name
python src/main.py --name Alice

# With custom count
python src/main.py --name Bob --count 3
```
""")
        
        return f"Successfully initialized project: {project_name}"
        
    except Exception as e:
        logger.error(f"Project initialization failed: {str(e)}", component="ProjectInit", severity=4, exc=e)
        raise

def init_project(project_name: str):
    """Main function to initialize a new Aitronos project."""
    return create_project_structure(project_name)

def init_hello_world_project(project_name: str):
    """Initialize a new Hello World example project."""
    return create_project_structure(project_name, template_type="hello_world") 