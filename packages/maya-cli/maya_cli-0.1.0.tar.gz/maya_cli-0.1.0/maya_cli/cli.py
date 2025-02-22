# cli.py 
import os
import click
from project_generator import create_project_structure, PROJECT_STRUCTURE

@click.group()
def maya():
    "Maya CLI - AI Project Generator"
    pass

@click.command()
@click.argument("project_name")
def create(project_name):
    "Create a new AI project structure"
    base_path = os.path.join(os.getcwd(), project_name)
    if os.path.exists(base_path):
        click.echo(f"Error: Project '{project_name}' already exists.")
        return
    os.makedirs(base_path, exist_ok=True)
    create_project_structure(base_path, PROJECT_STRUCTURE)
    click.echo(f"✅ AI project '{project_name}' created successfully!")

# Add commands to CLI
maya.add_command(create)

if __name__ == "__main__":
    maya()
