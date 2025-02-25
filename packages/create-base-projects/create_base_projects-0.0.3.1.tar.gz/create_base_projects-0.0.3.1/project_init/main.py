import typer
import subprocess
import os

from rich import print
from InquirerPy import prompt
from InquirerPy.base.control import Choice

from typing import List, Optional

from .templates.aiogram import create as create_aiogram
from .templates.pyqt import create as create_pyqt
from .styles.colors import get_random_color

from .utils.env import create_virtual_environment, activate_virtual_environment

app = typer.Typer(
    name="create-base-project",
    help="CLI tool for creating base projects and managing virtual environments."
)

VALID_VENV_NAMES = (".venv", "venv", ".env", "env")


@app.command(name="init-project")
def init_project(
    project_type: str = typer.Option(
        None, "--type", "-t", help="Specify the project type (pyqt or aiogram)"
    ),
    project_name: str = typer.Argument(
        None, help="Project name"
    )
) -> None:
    """
    Initializes a new project of the specified type.
    If the project type is not specified, a choice will be presented.
    """
    if not project_type:
        answer = prompt(
            [
                {
                    "type": "list",
                    "name": "project_type",
                    "message": "Choose a project type:",
                    "choices": [
                        Choice("PyQt"),
                        Choice("aiogram"),
                    ],
                    "qmark": "🚀",
                }
            ],
            style={
                "question": "cyan",
                "answer": get_random_color(),
                "pointer": get_random_color(),
                "highlighted": "yellow",
            }
        )
        project_type = answer["project_type"].lower()
    else:
        project_type = project_type.lower()
        if project_type not in ("pyqt", "aiogram"):
            print("[red]Invalid project type! Choose 'PyQt' or 'aiogram'.[/red]")
            raise typer.Exit(1)

    if not project_name:
        project_name = typer.prompt("Enter project name")

    create_project(project_type, project_name)


@app.command(name="init-venv")
def init_venv(
    venv_name: str = typer.Argument(".venv", help="Virtual environment name"),
    activate: bool = typer.Option(
        False, "--activate", "-a", help="Activate the virtual environment after creation"
    )
) -> None:
    """
    Creates a virtual environment with the specified name.
    If the --activate flag is provided, the environment will be activated immediately after creation.
    """
    if venv_name not in VALID_VENV_NAMES:
        print(f"[red]Invalid virtual environment name! Choose one of {VALID_VENV_NAMES}[/red]")
        raise typer.Exit(1)
    
    create_virtual_environment(venv_name)
    if activate:
        activate_virtual_environment(venv_name)


@app.command()
def install(dependencies: Optional[List[str]] = typer.Argument(None, help="Dependencies to install (optional)")) -> None:
    """
    Installs the specified dependencies or all dependencies from requirements.txt if no arguments are provided.
    """
    if not dependencies:
        if os.path.exists("requirements.txt"):
            subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        else:
            print("[red]requirements.txt file is missing.[/red]")
            return
    else:
        for dependency in dependencies:
            subprocess.run(["pip", "install", dependency], check=True)
        update_requirements()
    print("[green]Dependencies installed successfully.[/green]")


@app.command()
def uninstall(dependencies: Optional[List[str]] = typer.Argument(None, help="Dependencies to uninstall(optional)")) -> None:
    """
    Uninstalls the specified dependencies or all dependencies from requirements.txt if no arguments are provided.
    """
    if dependencies:
        for dependency in dependencies:
            subprocess.run(["pip", "uninstall", dependency, "-y"], check=True)
        update_requirements()
    else:
        if os.path.exists("requirements.txt"):
            subprocess.run(["pip", "uninstall", "-r", "requirements.txt", "-y"], check=True)
        else:
            print("[red]requirements.txt file is missing.[/red]")
            return
    print("[green]Dependencies uninstalled successfully.[/green]")


@app.command()
def freeze() -> None:
    update_requirements()

def update_requirements() -> None:
    """
    Updates the requirements.txt file with the current list of installed packages.
    """
    subprocess.run(["pip", "freeze", ">", "requirements.txt"], check=True)
        

def create_project(project_type: str, project_name: str) -> None:
    """
    Creates a new project based on the selected type and given name.
    """
    if project_type == "aiogram":
        create_aiogram(project_name)
    elif project_type == "pyqt":
        create_pyqt(project_name)
    else:
        print("[red]Unsupported project type.[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
