

def run_user_checks(target) -> list:
    """Verifica configurações críticas de contas e usuários do sistema."""
    results = []
    
    # Checagem: Contas com UID 0 (além do root)
    res_uid0 = {
        "category": "User Management",
        "check": "Verificar contas com UID 0 (Privilégios de Root)",
        "status": "PASS",
        "details": ""
    }

    try:
        content = target.read_file("/etc/passwd")
        uid_zero_users = []
        
        for line in content.splitlines():
            parts = line.split(":")
            if len(parts) >= 3:
                username = parts[0]
                uid = parts[2]
                # Verifica se o UID é 0, mas ignora o usuário padrão 'root'
                if uid == "0" and username != "root":
                    uid_zero_users.append(username)
        
        if uid_zero_users:
            res_uid0["status"] = "FAIL"
            res_uid0["details"] = f"Alerta Crítico! Usuários secundários com UID 0 encontrados: {', '.join(uid_zero_users)}"
        else:
            res_uid0["status"] = "PASS"
            res_uid0["details"] = "Apenas o usuário 'root' possui privilégios totais (UID 0)."
            
    except Exception as e:
        res_uid0["status"] = "ERROR"
        res_uid0["details"] = f"Erro ao analisar o arquivo /etc/passwd: {str(e)}"

    results.append(res_uid0)
    return results
