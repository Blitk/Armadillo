
from unittest.mock import MagicMock
from checks.ssh_audit import run_ssh_checks

def test_ssh_checks_secure_config():
    """Testa se a auditoria de SSH identifica uma configuração 100% segura."""
    mock_target = MagicMock()
    # Simula o conteúdo de um sshd_config seguro
    mock_target.read_file.return_value = """
    PermitRootLogin no
    PasswordAuthentication no
    X11Forwarding no
    MaxAuthTries 3
    """

    results = run_ssh_checks(mock_target)
    
    # Verifica se todas as 4 checagens foram aprovadas (PASS)
    assert len(results) == 4
    for res in results:
        assert res["status"] == "PASS"

def test_ssh_checks_vulnerable_config():
    """Testa se a auditoria de SSH identifica parâmetros inseguros."""
    mock_target = MagicMock()
    # Simula o conteúdo de um sshd_config vulnerável
    mock_target.read_file.return_value = """
    PermitRootLogin yes
    PasswordAuthentication yes
    X11Forwarding yes
    MaxAuthTries 10
    """

    results = run_ssh_checks(mock_target)
    
    assert len(results) == 4
    for res in results:
        assert res["status"] == "FAIL"
