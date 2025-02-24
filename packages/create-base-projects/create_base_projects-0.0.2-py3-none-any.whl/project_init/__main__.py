from project_init.config import choose_config
from project_init.generator import generate_project_structure
from project_init.setup_env import setup_virtualenv

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