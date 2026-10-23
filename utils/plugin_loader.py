
import importlib
import pkgutil
import checks

def load_all_checks() -> list:
    """Carrega dinamicamente todas as funções de auditoria dentro da pasta checks/."""
    audit_functions = []

    # Percorre todos os módulos dentro do pacote 'checks'
    for _, module_name, _ in pkgutil.iter_modules(checks.__path__):
        # Importa o módulo dinamicamente
        module = importlib.import_module(f"checks.{module_name}")
        
        # Procura por funções dentro do módulo que começam com 'run_'
        for attribute_name in dir(module):
            if attribute_name.startswith("run_"):
                func = getattr(module, attribute_name)
                if callable(func):
                    audit_functions.append(func)
                    
    return audit_functions
