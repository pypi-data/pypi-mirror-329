from prompt_toolkit.shortcuts import radiolist_dialog

def choose_config():
    """Функция для выбора типа проекта"""
    result = radiolist_dialog(
        title="🔧 Project Init",
        text="Выберите тип проекта:",
        values=[
            ("pyside6", "📦 PySide6 (Графический интерфейс)"),
            ("aiogram3", "🤖 Aiogram3 (Telegram Бот)"),
        ],
    ).run()

    return result
