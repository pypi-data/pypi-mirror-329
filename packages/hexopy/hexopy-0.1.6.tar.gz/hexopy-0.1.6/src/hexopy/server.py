import uvicorn
import importlib.util
import os
from fastapi import FastAPI
from dataclasses import dataclass
from hexopy.database import DatabaseManager


@dataclass(frozen=True, slots=True)
class ConfigInit:
    http: FastAPI


class HexoServer:
    def __init__(self, port=8000, reload=False):
        self.modules = []
        self.host = "0.0.0.0"
        self.port = port
        self.reload = reload
        self.http = FastAPI()
        self.config = ConfigInit(http=self.http)
        self.installed_apps = self._load_installed_apps()

    def _load_installed_apps(self):
        """Carga `INSTALLED_APPS` desde `internal/settings.py` si existe."""
        settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "internal", "settings.py")
        
        if not os.path.exists(settings_path):
            print("⚠️ Advertencia: No se encontró `internal/settings.py`. INSTALLED_APPS estará vacío.")
            return []
        
        spec = importlib.util.spec_from_file_location("internal.settings", settings_path)
        settings = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(settings)

        return getattr(settings, "INSTALLED_APPS", [])

    def add_module(self, module):
        """Añade un módulo y lo inicializa si tiene `init()`."""
        if module:
            self.modules.append(module)

    def init(self):
        """Inicializa la base de datos y los módulos agregados."""
        if self.installed_apps:
            database = DatabaseManager(INSTALLED_APPS=self.installed_apps)
            database.init_db()

        for module in self.modules:
            if hasattr(module, "init"):
                module.init()

        print("✅ Servidor inicializado con los módulos cargados.")

    def run(self):
        """Ejecuta el servidor FastAPI con Uvicorn."""
        print(f"🚀 Iniciando servidor en {self.host}:{self.port} ...")
        uvicorn.run(self.http, host=self.host, port=self.port, reload=self.reload)


def create_app(port=8000, reload=False) -> HexoServer:
    """Crea y retorna una instancia del servidor."""
    return HexoServer(port=port, reload=reload)
