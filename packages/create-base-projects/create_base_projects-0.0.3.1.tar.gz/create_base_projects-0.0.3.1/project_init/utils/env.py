import os
import subprocess
import sys
from rich import print
import shutil

def create_virtual_environment(env_name: str = ".venv") -> None:
    """Создать виртуальное окружение."""
    if os.path.exists(env_name):
        print(f"[yellow]Виртуальное окружение '{env_name}' уже существует. Удаляем его...[/yellow]")
        shutil.rmtree(env_name)
    
    print(f"[blue]Создание виртуального окружения '{env_name}'...[/blue]")
    subprocess.run([sys.executable, '-m', 'venv', env_name], check=True)
    print(f"[green]Виртуальное окружение '{env_name}' создано.[/green]")

def activate_virtual_environment(env_name: str = ".venv") -> None:
    """Показать команду для активации .venv."""
    if os.name == 'nt':
        activation_cmd = f"{env_name}\\Scripts\\activate.bat"
    else:
        activation_cmd = f"source {env_name}/bin/activate"
    
    print(f"[blue]Для активации окружения выполните: {activation_cmd}[/blue]")