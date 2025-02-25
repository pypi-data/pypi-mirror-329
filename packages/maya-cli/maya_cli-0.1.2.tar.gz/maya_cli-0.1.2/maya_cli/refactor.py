import os
import click
import openai
import logging

# Setup logging
LOG_FILE = "maya_refactor.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# OpenAI API Key (Ensure it's set as an environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_file(file_path):
    """Reads the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        logging.info(f"Successfully read file: {file_path}")
        return content
    except FileNotFoundError:
        error_msg = f"❌ Error: File not found - {file_path}"
    except PermissionError:
        error_msg = f"❌ Error: Permission denied - {file_path}"
    except Exception as e:
        error_msg = f"❌ Error reading {file_path}: {str(e)}"
    
    logging.error(error_msg)
    click.echo(error_msg)
    return None

def write_file(file_path, content):
    """Writes content back to the file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        success_msg = f"✅ Refactored and updated: {file_path}"
        logging.info(success_msg)
        click.echo(success_msg)
    except PermissionError:
        error_msg = f"❌ Error: Permission denied - {file_path}"
    except Exception as e:
        error_msg = f"❌ Error writing {file_path}: {str(e)}"
    
    logging.error(error_msg)
    click.echo(error_msg)

def refactor_code_with_openai(code):
    """Sends code to OpenAI for best-practices refactoring."""
    prompt = f"""
    Refactor the following Python code following best practices for AI API development:
    - Clean code structure
    - Improve readability & maintainability
    - Optimize performance & scalability
    - Ensure proper exception handling
    - Secure API keys and authentication

    Code:
    \"\"\"{code}\"\"\"

    Optimized Code:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert AI code reviewer."},
                {"role": "user", "content": prompt}
            ]
        )
        optimized_code = response["choices"][0]["message"]["content"].strip()
        logging.debug(f"OpenAI API response received successfully.")
        return optimized_code
    except openai.error.OpenAIError as e:
        error_msg = f"❌ OpenAI API Error: {str(e)}"
    except Exception as e:
        error_msg = f"❌ Unexpected Error: {str(e)}"
    
    logging.error(error_msg)
    click.echo(error_msg)
    return code  # Return original code if API call fails

def process_directory(directory, filename=None):
    """Scans the given directory and refactors specified files."""
    if not os.path.exists(directory):
        click.echo(f"❌ Error: Directory '{directory}' not found.")
        logging.error(f"Directory '{directory}' does not exist.")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            if filename and file != filename:
                continue  # Skip files that don't match
            
            file_path = os.path.join(root, file)
            if file.endswith(".py"):  # Only process Python files
                click.echo(f"🔍 Checking: {file_path}")
                logging.info(f"Processing file: {file_path}")
                
                code = read_file(file_path)
                if code:
                    refactored_code = refactor_code_with_openai(code)
                    write_file(file_path, refactored_code)

    click.echo("✅ Best practices check completed!")
    logging.info("Best practices check completed successfully.")
