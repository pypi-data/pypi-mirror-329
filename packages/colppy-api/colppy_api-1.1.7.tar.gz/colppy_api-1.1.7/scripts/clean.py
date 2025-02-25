import shutil
from pathlib import Path

def clean_project():
    """Limpia archivos temporales y builds del proyecto"""
    print("🧹 Limpiando proyecto...")
    
    # Directorios a limpiar
    dirs_to_clean = [
        "dist",
        "build",
        "*.egg-info",
        ".venv",
        ".tox",
        "htmlcov",
    ]
    
    root_dir = Path(__file__).parent.parent
    
    for pattern in dirs_to_clean:
        for path in root_dir.glob(pattern):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"Eliminado: {path}")
    
    print("✅ Limpieza del proyecto completada!")

if __name__ == "__main__":
    clean_project() 