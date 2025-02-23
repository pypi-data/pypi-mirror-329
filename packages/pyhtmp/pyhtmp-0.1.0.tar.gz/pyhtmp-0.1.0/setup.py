from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README.md
long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

# Define package dependencies
dependencies = [
    "websockets>=10.0",  # WebSocket support
    "Jinja2>=3.0.0",    # Template rendering for Flask/Django
    "Django>=3.0",      # Django integration (optional)
    "Flask>=2.0",       # Flask integration (optional)
    "typing-extensions>=4.0.0",  # Type hints support
]

# Define development dependencies
dev_dependencies = [
    "pytest>=7.0",      # Testing framework
    "pytest-asyncio>=0.20.0",  # Async testing support
    "black>=22.0",      # Code formatting
    "mypy>=0.900",      # Static type checking
    "sphinx>=4.0",      # Documentation generation
]

setup(
    name="pyhtmp",
    version="0.1.0",
    author="Kunaal Gadhalay",
    author_email="kunaalgadhalay93@gmail.com",
    description="A Python framework for building dynamic HTML interfaces with component-based architecture and real-time communication.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kunaalgadhalay/pyhtmp",
    packages=find_packages(include=["pyhtmp", "pyhtmp.*"]),
    package_data={
        "pyhtmp": ["py.typed"],  # Include type hints
    },
    install_requires=dependencies,
    extras_require={
        "dev": dev_dependencies,
        "django": ["Django>=3.0"],  # Optional Django integration
        "flask": ["Flask>=2.0"],    # Optional Flask integration
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    keywords=[
        "html",
        "components",
        "virtual-dom",
        "websockets",
        "django",
        "flask",
        "templating",
    ],
    project_urls={
        "Source": "https://github.com/kunaalgadhalay/pyhtmp",
        "Bug Reports": "https://github.com/kunaalgadhalay/pyhtmp/issues",
        "Documentation": "https://github.com/kunaalgadhalay/pyhtmp#readme",
    },
    entry_points={
        "console_scripts": [
            "pyhtmp-cli=pyhtmp.cli:main",  # Optional CLI tool
        ],
    },
)