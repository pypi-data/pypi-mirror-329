# Jedai Core

**Jedai Core** is a modular, reusable AI library that provides the foundational components for various AI use cases. It’s designed to be easily integrated into multiple projects, enabling rapid development and deployment of AI-driven features.

## Features

- **AI Module**:
  - **Generate Social Content**: Create social media content (e.g., LinkedIn posts) using customizable prompts.
  - **Extract Information from Documents**: Parse and extract key information from documents based on predefined extraction formats.
- **Common Module**: Shared utilities, exceptions, and helper functions used across the library.

## Repository Structure

```
jedai-core/
├── README.md
├── pyproject.toml
└── src/
    └── jedai_core/
        ├── __init__.py
        ├── common/
        │   └── __init__.py
        ├── generate_social_content/
        │   └── __init__.py
        └── .../
            └── __init__.py
```

## Installation

### Local Development (Editable Mode)

Clone the repository and navigate to the project root, then run:

```bash
pip install -e .
```

This installs the library in "editable" mode. Any changes you make to the source code will be reflected immediately in your environment.

### Installing from Git

To install the latest version directly from GitHub, run:

```bash
pip install git+git@github.com:cads-ai/core.git
```

## Usage

After installation, you can import and use the library in your projects:

```python
from jedai_core.ai.generate_social_content import SocialContentGenerator
from jedai_core.ai.extract_info_from_document import DocumentInfoExtractor
from jedai_core.common import utils

# Example: Generate social content
generator = SocialContentGenerator()
content = generator.generate(prompt="Your prompt here")
print(content)

# Example: Extract document information
extractor = DocumentInfoExtractor()
info = extractor.extract(document_path="path/to/document.pdf")
print(info)
```

## Development Workflow

For local development and testing:

1. **Clone Repositories Side-by-Side**:
   Organize your code like this:
   ```
   codes/
   ├── jedai-core/          # Core library repository
   └── marketing-project/   # Project that consumes jedai-core
   ```
2. **Install in Editable Mode**:
   In your virtual environment used by the consuming project, run:
   ```bash
   cd /path/to/jedai-core
   pip install -e .
   ```
3. **Edit and Test**:
   Open both repositories in your VSCode workspace. Any changes you make in the `jedai-core` repository will be available immediately in the `marketing-project` (after a server restart if necessary).
4. **Versioning and Updating**:
   - When you complete new features or bug fixes, update the version in `pyproject.toml` following semantic versioning.
   - Commit and push the changes to the `jedai-core` GitHub repository.
   - In your consuming projects, update the dependency via pip:
     ```bash
     pip install --upgrade jedai-core
     ```

## Contributing

Contributions to **Jedai Core** are welcome! To contribute:

- Fork the repository.
- Create a feature branch and commit your changes.
- Ensure tests pass (if applicable) and add new tests as needed.
- Submit a pull request with a detailed description of your changes.
