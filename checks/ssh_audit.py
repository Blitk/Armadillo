

def run_ssh_checks(target) -> list:
    """Executa todas as checagens relacionadas ao SSH."""
    results = []
    config_path = "/etc/ssh/sshd_config"

    # Checagem 1: PermitRootLogin desativado
    res_root = {
        "category": "SSH Security",
        "check": "Desativar Login Direto de Root (PermitRootLogin)",
        "status": "FAIL",
        "details": ""
    }

    try:
        file_content = target.read_file(config_path)
        found = False
        for line in file_content.splitlines():
            clean_line = line.strip()
            # Ignora linhas comentadas
            if clean_line.startswith("#"):
                continue
            
            if clean_line.lower().startswith("permitrootlogin"):
                found = True
                if "no" in clean_line.lower():
                    res_root["status"] = "PASS"
                    res_root["details"] = f"Configuração segura encontrada: '{clean_line}'"
                else:
                    res_root["status"] = "FAIL"
                    res_root["details"] = f"Inseguro: '{clean_line}' (Recomendado: 'PermitRootLogin no')"
                break
        
        if not found:
            res_root["status"] = "WARNING"
            res_root["details"] = "Parâmetro PermitRootLogin não explícito (padrão do sistema pode ser inseguro)."
            
    except Exception as e:
        res_root["status"] = "ERROR"
        res_root["details"] = f"Não foi possível ler o arquivo SSH: {str(e)}"

    results.append(res_root)
    return results
