import shutil
from pathlib import Path

def clean_cache():
    """Limpia archivos de caché de Python"""
    print("🧹 Limpiando caché...")
    
    # Directorios a limpiar
    cache_dirs = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        ".pytest_cache",
        ".coverage",
        ".mypy_cache",
        ".ruff_cache",
    ]
    
    root_dir = Path(__file__).parent.parent
    
    for pattern in cache_dirs:
        for path in root_dir.glob(pattern):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"Eliminado: {path}")
    
    print("✅ Limpieza de caché completada!")

if __name__ == "__main__":
    clean_cache() 