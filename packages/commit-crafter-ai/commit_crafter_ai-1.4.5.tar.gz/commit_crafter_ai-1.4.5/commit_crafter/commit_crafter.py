import os
import subprocess
import sys
import typer
import pyperclip
from openai import OpenAI
from ollama import chat, ChatResponse

app = typer.Typer(help="AI-powered commit message generator")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_prompt_from_config() -> str:
    """Get custom prompt from craft.config file if it exists"""
    config_path = os.path.join(os.getcwd(), "craft.config")

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading config file: {e}", file=sys.stderr)
            return None
    return None


def get_git_diff() -> str:
    """Get the git diff output for staged changes"""
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--staged"], stderr=subprocess.STDOUT
        ).decode("utf-8")

        if not diff_output:

            diff_output = subprocess.check_output(
                ["git", "diff"], stderr=subprocess.STDOUT
            ).decode("utf-8")

        return diff_output
    except subprocess.CalledProcessError as e:
        print(e, file=sys.stderr)
        print()
        print(
            f"Error getting git diff. If you think this is a bug, please report it to serhatuzbas@gmail.com"
        )
        sys.exit(1)


def generate_commit_message(
    diff: str, ollama: bool = False, model: str = "llama3.2:3b"
) -> str:
    """Generate a commit message and detailed description using the selected AI client"""

    if not ollama and not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable is not set for OpenAI")
        sys.exit(1)

    custom_prompt = get_prompt_from_config()
    default_prompt = """You are a helpful assistant that generates clear and concise git commit messages.
    Follow these rules:
    1. Use the conventional commits format (type: description)
    2. Keep the message under 72 characters
    3. Use present tense
    4. Be specific but concise
    5. Focus on the "what" and "why" rather than "how"
    6. Provide a detailed description of the changes step by step.
    7. Do not use title, subtitle and markdown for the commit message. Example:
    **commit message**
    **detailed description**
    8. When writing the detailed description, write it item by item. You can use markdown to make it more readable at the start of item.
    """

    prompt = f"""{custom_prompt or default_prompt}
        
    Generate a commit message and detailed description for the following git diff:
    {diff}
    """

    if ollama:
        try:
            response: ChatResponse = chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response["message"]["content"].strip()
        except Exception as e:
            print(e, file=sys.stderr)  # Print the error message
            print()  # Print an empty line
            print(
                f"Error generating commit message. If you think this is a bug, please report it to serhatuzbas@gmail.com",
                file=sys.stderr,
            )

            sys.exit(1)
    else:
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(e, file=sys.stderr)  # Print the error message
            print()  # Print an empty line
            print(
                f"Error generating commit message. If you think this is a bug, please report it to serhatuzbas@gmail.com",
                file=sys.stderr,
            )
            sys.exit(1)


def create_commit(message: str):
    """Create a git commit with the generated message"""
    try:
        # Add all changes if nothing is staged
        diff_staged = subprocess.check_output(
            ["git", "diff", "--staged"], stderr=subprocess.STDOUT
        ).decode("utf-8")

        if not diff_staged:
            subprocess.run(["git", "add", "."], check=True)

        # Use the message directly for the commit
        subprocess.run(["git", "commit", "-m", message], check=True)
        print(f"Successfully committed with message: {message}")
    except subprocess.CalledProcessError:
        print(
            f"Error creating commit. If you think this is a bug, please report it to serhatuzbas@gmail.com"
        )
        sys.exit(1)


@app.callback()
def callback():
    """
    Craft commit messages using AI
    """
    pass


@app.command()
def craft(
    copy: bool = typer.Option(
        False, "--copy", help="Copy the commit message to clipboard"
    ),
    ollama: str = typer.Option(
        None,
        "--ollama",
        help="Use Ollama with specified model (e.g., --ollama 'llama3.2:3b')",
    ),
):
    """Craft a commit message and create a commit"""
    try:
        diff = get_git_diff()

        if not diff:
            print("No changes to commit!")
            sys.exit(0)

        # If ollama is provided, use it as the model name, otherwise use OpenAI
        use_ollama = ollama is not None
        model = ollama if use_ollama else None
        commit_message = generate_commit_message(diff, use_ollama, model)

        if copy:
            pyperclip.copy(commit_message)
            print(f"Copied to clipboard: {commit_message}")
        else:
            create_commit(commit_message)
    except Exception:
        print(
            f"Error happened. If you think this is a bug, please report it to serhatuzbas@gmail.com"
        )
        sys.exit(1)


if __name__ == "__main__":
    app()
