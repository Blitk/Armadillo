# checks/permissions_audit.py

def run_permission_checks(target) -> list:
    """Executa checagens de permissões em arquivos sensíveis do Linux."""
    results = []

    # Checagem: Permissões do /etc/shadow (não deve ter permissão de leitura global)
    res_shadow = {
        "category": "File Permissions",
        "check": "Permissões restritas no arquivo /etc/shadow",
        "status": "FAIL",
        "details": ""
    }

    try:
        # Usa o comando stat para pegar as permissões em formato octal (ex: 000, 640)
        output = target.run_command("stat -c '%a' /etc/shadow")
        perms = output.strip()
        
        # O shadow idealmente deve ter permissão 000 ou 600 (apenas root)
        if perms in ["000", "600", "400"]:
            res_shadow["status"] = "PASS"
            res_shadow["details"] = f"Permissões seguras encontradas para /etc/shadow: {perms}"
        else:
            res_shadow["status"] = "FAIL"
            res_shadow["details"] = f"Inseguro: /etc/shadow possui permissões muito abertas ({perms}). Recomendado: 000 ou 600."
            
    except Exception as e:
        res_shadow["status"] = "ERROR"
        res_shadow["details"] = f"Erro ao verificar /etc/shadow: {str(e)}"

    results.append(res_shadow)
    return results
