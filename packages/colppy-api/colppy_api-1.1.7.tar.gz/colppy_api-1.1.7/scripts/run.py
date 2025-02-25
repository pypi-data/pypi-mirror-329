import sys
from publish import publish
from clean_cache import clean_cache
from clean import clean_project

def show_help():
    print("""
🛠️  Herramientas de desarrollo disponibles:

    publish     - Publica el paquete en PyPI
    clean-cache - Limpia archivos de caché de Python
    clean       - Limpia archivos temporales del proyecto
    all         - Ejecuta clean, clean-cache y luego publish
    
Uso: python scripts/run.py [comando]
    """)

def main():
    if len(sys.argv) != 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "publish":
        publish()
    elif command == "clean-cache":
        clean_cache()
    elif command == "clean":
        clean_project()
    elif command == "all":
        clean_project()
        clean_cache()
        publish()
    else:
        print(f"❌ Comando desconocido: {command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 