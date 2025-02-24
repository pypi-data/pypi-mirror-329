import os

def generate_project_structure(project_type):
    """Создаёт базовую структуру проекта"""
    
    structure = {
        "pyside6": {
            "folders": ["src", "resources", "ui"],
            "files": {
                "src/main.py": 'from PySide6.QtWidgets import QApplication, QMainWindow\n\n'
                               'app = QApplication([])\n'
                               'window = QMainWindow()\n'
                               'window.show()\n'
                               'app.exec()',
                "requirements.txt": "pyside6",
            },
        },
        "aiogram3": {
            "folders": ["bot", "config", "handlers"],
            "files": {
                "bot/bot.py": 'from aiogram import Bot, Dispatcher\nimport asyncio\n\n'
                              'TOKEN = "your-bot-token"\n'
                              'bot = Bot(token=TOKEN)\n'
                              'dp = Dispatcher()\n\n'
                              'async def main():\n'
                              '    print("🚀 Бот запущен!")\n'
                              '    await dp.start_polling(bot)\n\n'
                              'asyncio.run(main())',
                "requirements.txt": "aiogram",
            },
        },
    }

    config = structure.get(project_type, {})
    for folder in config.get("folders", []):
        os.makedirs(folder, exist_ok=True)

    for file, content in config.get("files", {}).items():
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"✅ Структура проекта '{project_type}' создана!")
