import sys
import importlib.util
import os
from fastapi import FastAPI
from dataclasses import dataclass
from hexopy.database import DatabaseManager

BASE_DIR = os.getcwd()

sys.path.append(BASE_DIR)

@dataclass(frozen=True, slots=True)
class ConfigInit:
    http: FastAPI


class HexoServer:
    def __init__(self, port=8000):
        self.host = "0.0.0.0"
        self.port = port
        self.http = FastAPI()
        self.config = ConfigInit(http=self.http)
        self.installed_apps = self._load_installed_apps()
        self.environment = os.getenv("ENVIRONMENT", "development") 
        self.reload = self.environment == "development"  
        self.workers = 1 if self.reload else 4  
        

    def _load_installed_apps(self):
        """Carga `INSTALLED_APPS` desde `internal/settings.py` si existe."""
        settings_path = os.path.join(BASE_DIR, "internal", "settings.py")
        
        if not os.path.exists(settings_path):
            print("⚠️ Advertencia: No se encontró `internal/settings.py`. INSTALLED_APPS estará vacío.")
            return []
        
        spec = importlib.util.spec_from_file_location("internal.settings", settings_path)
        settings = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(settings)

        return set(getattr(settings, "INSTALLED_APPS", []))
    
    async def init_db(self):
        """Inicializa la base de datos usando Tortoise ORM."""

        if self.installed_apps:
            database = DatabaseManager(INSTALLED_APPS=self.installed_apps)
            await database.init_db()

        print("✅ Base de datos inicializada correctamente.")       


def create_app(port=8000) -> HexoServer:
    """Crea y retorna una instancia del servidor."""
    return HexoServer(port=port)
