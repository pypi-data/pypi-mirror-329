from config import choose_config
from generator import generate_project_structure
from setup_env import setup_virtualenv

def main():
    print("🚀 Добро пожаловать в Project Init!")
    project_type = choose_config()
    
    if not project_type:
        print("❌ Выбор не сделан. Выход...")
        return
    
    generate_project_structure(project_type)
    setup_virtualenv()

if __name__ == "__main__":
    main()