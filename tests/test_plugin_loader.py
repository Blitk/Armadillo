
from utils.plugin_loader import load_all_checks

def test_load_all_checks():
    """Garante que as funções iniciadas por 'run_' dentro de checks/ são importadas."""
    checks = load_all_checks()
    assert len(checks) > 0
    for func in checks:
        assert callable(func)
        assert func.__name__.startswith("run_")
