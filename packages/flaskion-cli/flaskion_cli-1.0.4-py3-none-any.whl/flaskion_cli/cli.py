import os
import sys
import shutil
import subprocess

# Correct path reference
FLASKION_TEMPLATE = os.path.join(os.path.dirname(__file__), "flaskion_template")

def create_project():
    if len(sys.argv) < 3 or sys.argv[1] != "new":
        print("❌ Usage: flaskion new {projectname}")
        sys.exit(1)

    project_name = sys.argv[2]
    project_path = os.path.join(os.getcwd(), project_name)

    if os.path.exists(project_path):
        print(f"❌ The folder '{project_name}' already exists.")
        sys.exit(1)

    # Ensure the template path exists
    if not os.path.exists(FLASKION_TEMPLATE):
        print(f"❌ Template folder not found: {FLASKION_TEMPLATE}")
        sys.exit(1)

    print(f"📁 Creating Flaskion project: {project_name}")
    shutil.copytree(FLASKION_TEMPLATE, project_path)

    print("📜 Initializing Git repository...")
    subprocess.run(["git", "init"], cwd=project_path)

    print("🐍 Setting up virtual environment...")
    subprocess.run(["python3", "-m", "venv", "venv"], cwd=project_path)

    print(f"✅ Flaskion project '{project_name}' created successfully!")
    print(f"🚀 Next steps:\n   cd {project_name}\n   source venv/bin/activate\n   pip install -r requirements.txt\n   flask run")

if __name__ == "__main__":
    create_project()