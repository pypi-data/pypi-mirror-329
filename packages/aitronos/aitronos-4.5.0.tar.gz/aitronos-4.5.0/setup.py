from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="aitronos",
    version="4.5.0",
    packages=find_packages(exclude=[
        'tests*',
        '*.tests',
        '*.tests.*',
        'venv*',
        '*venv*',
        '*.venv*',
        '*egg-info*',
        'dist*',
        'build*',
        '**/__pycache__',
        # Add more specific exclusions for virtual environments
        '**/venv/**',
        '**/env/**',
        '**/.env/**',
        '**/.venv/**',
        '**/template/venv/**',
        '**/templates/venv/**',
        '**/template/env/**',
        '**/templates/env/**',
    ]),
    package_data={
        'aitronos': [
            'cli/commands/*/config.freddy.json',
            'cli/commands/*/requirements.txt',
            'cli/commands/*/resources/*.json',
            'cli/commands/*/resources/*.py',
            'cli/commands/*/src/main/*.py',
        ],
    },
    exclude_package_data={
        '': [
            'venv/*',
            '*venv/*',
            '.venv/*',
            '__pycache__/*',
            '*.pyc',
            '.DS_Store',
            '.idea/*',
            # Add more specific exclusions
            '**/venv/**/*',
            '**/env/**/*',
            '**/.env/**/*',
            '**/.venv/**/*',
        ],
    },
    include_package_data=False,
    install_requires=[
        'click>=8.0.0',
        'requests>=2.25.0',
        'typing-extensions>=4.0.0',
        'setuptools>=68.2.0',
        'tqdm>=4.66.5',
        'urllib3>=2.2.2',
        'certifi>=2024.7.4',
        'idna>=3.7',
        'optional>=0.0.1',
        'httpx>=0.27.2',
        'regex>=2024.5.15',
        'pytest>=8.3.3',
        'aitronos-logger>=0.1.6'
    ] + requirements,
    entry_points={
        "console_scripts": [
            "aitronos=aitronos.cli.main:cli",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "mypy>=0.900",
        ],
    },
    author="Phillip Loacker",
    author_email="phillip.loacker@aitronos.com",
    description="A Python package for interacting with the Freddy API and other Aitronos services",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Freddy-Development/aitronos-python-package",
    project_urls={
        "Bug Tracker": "https://github.com/Freddy-Development/aitronos-python-package/issues",
        "Documentation": "https://github.com/Freddy-Development/aitronos-python-package#readme",
        "Source Code": "https://github.com/Freddy-Development/aitronos-python-package",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    keywords='aitronos, freddy, api, machine learning, ai',
)
