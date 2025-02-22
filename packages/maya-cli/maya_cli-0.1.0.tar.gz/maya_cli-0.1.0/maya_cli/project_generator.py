# project_generator.py 
import os

# Define the AI Project Structure
PROJECT_STRUCTURE = {
    "data_source": {"ingestion": {}, "processing": {}, "storage": {}},
    "knowledge_base": {"models": {}, "training": {}, "evaluation": {}},
    "ai_governance": {"compliance": {}, "fairness": {}, "monitoring": {}},
    "api": {"endpoints": {}, "authentication": {}},
    "tests": {},
    "docs": {},
    "scripts": {},
    "configs": {}
}

# Function to create folders
def create_project_structure(base_path, structure):
    for folder, subfolders in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # Create __init__.py for package folders
        init_file = os.path.join(folder_path, "__init__.py")
        with open(init_file, "w") as f:
            f.write(f"# {folder.replace('_', ' ').title()} package\n")
        
        if isinstance(subfolders, dict):
            create_project_structure(folder_path, subfolders)
