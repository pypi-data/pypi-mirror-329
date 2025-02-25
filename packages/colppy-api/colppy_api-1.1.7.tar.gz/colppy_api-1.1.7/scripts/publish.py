import subprocess
import sys
from pathlib import Path

def run_command(command: str) -> None:
    """Ejecuta un comando y maneja errores"""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando: {command}")
        print(f"Error: {e}")
        sys.exit(1)

def publish():
    """Publica el paquete en PyPI"""
    print("🚀 Iniciando proceso de publicación...")
    
    # Instalar dependencias necesarias
    print("📦 Instalando dependencias...")
    run_command("pip install --upgrade build twine")
    
    # Limpiar distribuciones anteriores
    print("🧹 Limpiando distribuciones anteriores...")
    run_command("rm -rf dist/ build/ *.egg-info")
    
    # Construir el paquete
    print("🔨 Construyendo el paquete...")
    run_command("python -m build")
    
    # Verificar el paquete
    print("🔍 Verificando el paquete...")
    run_command("twine check dist/*")
    
    # Subir a PyPI
    print("📤 Subiendo a PyPI...")
    run_command("python -m twine upload dist/*")
    
    print("✅ Publicación completada exitosamente!")

if __name__ == "__main__":
    publish() 