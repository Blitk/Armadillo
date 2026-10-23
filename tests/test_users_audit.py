
from unittest.mock import MagicMock
from checks.users_audit import run_user_checks

def test_user_checks_no_extra_uid0():
    """Garante aprovação quando apenas o usuário 'root' tem UID 0."""
    mock_target = MagicMock()
    mock_target.read_file.return_value = """root:x:0:0:root:/root:/bin/bash
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
"""

    results = run_user_checks(mock_target)
    assert len(results) == 1
    assert results[0]["status"] == "PASS"

def test_user_checks_backdoor_uid0_found():
    """Garante reprovação (FAIL) quando existe outro usuário além do root com UID 0."""
    mock_target = MagicMock()
    # Simula uma conta backdoor 'hacker' com UID 0
    mock_target.read_file.return_value = """root:x:0:0:root:/root:/bin/bash
hacker:x:0:0:Hacked Account:/home/hacker:/bin/bash
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
"""

    results = run_user_checks(mock_target)
    assert len(results) == 1
    assert results[0]["status"] == "FAIL"
    assert "hacker" in results[0]["details"]
