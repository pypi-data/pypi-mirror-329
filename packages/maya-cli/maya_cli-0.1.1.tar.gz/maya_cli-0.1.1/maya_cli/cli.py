import os
import click
import logging
from .project_generator import create_project_structure, PROJECT_STRUCTURE

# Setup logging
logging.basicConfig(filename="maya_cli.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@click.group()
def maya():
    """Maya CLI - AI Project Generator"""
    pass

@click.command()
@click.argument("project_name")
def create(project_name):
    """Create a new AI project structure"""
    try:
        base_path = os.path.join(os.getcwd(), project_name)
        if os.path.exists(base_path):
            click.echo(f"Error: Project '{project_name}' already exists.")
            logging.error(f"Project '{project_name}' already exists.")
            return
        
        os.makedirs(base_path, exist_ok=True)
        create_project_structure(base_path, PROJECT_STRUCTURE)
        click.echo(f"✅ AI project '{project_name}' created successfully!")
        logging.info(f"Project '{project_name}' created successfully at {base_path}")
    
    except Exception as e:
        logging.error(f"Error while creating project: {str(e)}")
        click.echo(f"❌ An error occurred: {str(e)}")

maya.add_command(create)

if __name__ == "__main__":
    maya()
