from ..utils.structure import create_project_structure

def create(project_name: str) -> None:
    directories = [
        f"{project_name}/bot/handlers",
        f"{project_name}/bot/keyboards",
        f"{project_name}/bot/middlewares",
        f"{project_name}/bot/filters",
        f"{project_name}/bot/utils",
        f"{project_name}/bot/data",
        f"{project_name}/bot/services",
        f"{project_name}/tests",
    ]
    files = [
        f"{project_name}/bot/__init__.py",
        f"{project_name}/bot/main.py",
        f"{project_name}/bot/handlers/__init__.py",
        f"{project_name}/bot/keyboards/__init__.py",
        f"{project_name}/bot/middlewares/__init__.py",
        f"{project_name}/bot/filters/__init__.py",
        f"{project_name}/bot/utils/__init__.py",
        f"{project_name}/bot/data/__init__.py",
        f"{project_name}/bot/data/config.py",
        f"{project_name}/bot/services/__init__.py",
        f"{project_name}/bot/services/database.py",
        f"{project_name}/tests/__init__.py",
        f"{project_name}/tests/test_main.py",
        f"{project_name}/.env",
        f"{project_name}/.gitignore",
        f"{project_name}/requirements.txt",
        f"{project_name}/README.md",
    ]
    
    dependecies = [
        "aiogram",
        "sqlalchemy[asyncio]",
        "asyncpg",
        "python-dotenv"
    ]
    
    create_project_structure(directories, files, dependecies)
