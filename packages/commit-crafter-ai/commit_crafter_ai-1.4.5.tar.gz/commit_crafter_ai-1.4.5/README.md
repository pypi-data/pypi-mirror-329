# commit-crafter-ai

An AI-powered commit message generator that uses either OpenAI's GPT models or Ollama's local models to create meaningful git commit messages.

## Installation

```bash
pip install commit-crafter-ai
```

## Setup

1. Export your OpenAI API key:

```bash
# Linux/macOS
export OPENAI_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
```

2. The API key can also be added to your shell configuration file (~/.bashrc, ~/.zshrc, etc.) for persistence:

```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc  # or ~/.zshrc
```

## Usage

### Craft a commit message and directly create a commit

Default client is OpenAI:

```bash
commit-crafter-ai craft
```

If you want to use Ollama with a specific model:

```bash
commit-crafter-ai craft --ollama 'model-name'
```

### Craft a commit message and copy it to clipboard

If you want to copy the commit message to clipboard instead of directly creating a commit:

```bash
commit-crafter-ai craft --copy
```

## Configuration

You can customize the commit message generation prompt by creating a `craft.config` file in your project root directory. If no config file is found, the default prompt will be used.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
