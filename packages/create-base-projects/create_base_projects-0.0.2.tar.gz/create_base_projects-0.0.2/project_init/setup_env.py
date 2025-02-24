import os
import subprocess
import sys

def setup_virtualenv():
    """Создаёт виртуальное окружение и устанавливает зависимости"""
    
    print("🔧 Создаём виртуальное окружение...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

    pip_path = "venv/bin/pip" if os.name != "nt" else "venv\\Scripts\\pip.exe"

    print("📦 Устанавливаем зависимости...")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)

    print("✅ Виртуальное окружение настроено! Активируйте его командой:")
    print("   source venv/bin/activate" if os.name != "nt" else "   venv\\Scripts\\activate.bat")
