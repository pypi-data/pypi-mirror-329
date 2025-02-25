from ..utils.structure import create_project_structure

def create(project_name: str) -> None:
    directories = [
        f"{project_name}/src/components",
        f"{project_name}/src/widgets",
        f"{project_name}/src/assets",
        f"{project_name}/src/pages",
        f"{project_name}/src/utils",
        f"{project_name}/src/services",
        f"{project_name}/tests",
    ]
    files = [
        f"{project_name}/src/main.py",
        f"{project_name}/src/components/__init__.py",
        f"{project_name}/src/widgets/__init__.py",
        f"{project_name}/src/assets/__init__.py",
        f"{project_name}/src/pages/__init__.py",
        f"{project_name}/src/utils/__init__.py",
        f"{project_name}/src/services/__init__.py",
        f"{project_name}/tests/__init__.py",
        f"{project_name}/tests/test_main.py",
        f"{project_name}/.gitignore",
        f"{project_name}/README.md",
        f"{project_name}/requirements.txt"
    ]
    
    dependecies = [
        "PySide6",
        "pytest"
    ]
    
    create_project_structure(directories, files, dependecies)
    