# checks/ssh_audit.py

def run_ssh_checks(target) -> list:
    """Executa checagens avançadas de hardening no arquivo de configuração do SSH (/etc/ssh/sshd_config)."""
    results = []
    config_path = "/etc/ssh/sshd_config"

    # Define as regras que queremos auditar
    # Formato: (Parâmetro do SSH, Valor esperado, Categoria de severidade, Mensagem de falha)
    expected_rules = [
        {
            "param": "permitrootlogin",
            "expected": "no",
            "check_name": "Desativar Login Direto de Root (PermitRootLogin)",
            "fail_msg": "Inseguro: O login direto de root está permitido ou mal configurado."
        },
        {
            "param": "passwordauthentication",
            "expected": "no",
            "check_name": "Desativar Autenticação por Senha (PasswordAuthentication)",
            "fail_msg": "Inseguro: A autenticação por senha está ativa. Recomenda-se uso exclusivo de chaves SSH."
        },
        {
            "param": "x11forwarding",
            "expected": "no",
            "check_name": "Desativar Encaminhamento X11 (X11Forwarding)",
            "fail_msg": "Alerta: O redirecionamento X11 está ativo, o que pode expor o servidor a riscos gráficos."
        },
        {
            "param": "maxauthtries",
            "expected": "4",
            "check_name": "Limitar Tentativas de Autenticação (MaxAuthTries)",
            "fail_msg": "Inseguro: O limite de tentativas de login por conexão está alto ou padrão (Recomendado: <= 4)."
        }
    ]

    try:
        file_content = target.read_file(config_path)
        
        # Mapeia as configurações encontradas no arquivo (removendo comentários)
        configured_values = {}
        for line in file_content.splitlines():
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            
            parts = clean_line.split(maxsplit=1)
            if len(parts) == 2:
                key, val = parts[0].lower(), parts[1].strip().lower()
                configured_values[key] = val

        # Valida cada regra esperada
        for rule in expected_rules:
            param = rule["param"]
            expected = rule["expected"]
            
            res = {
                "category": "SSH Security",
                "check": rule["check_name"],
                "status": "FAIL",
                "details": ""
            }

            if param in configured_values:
                current_val = configured_values[param]
                # Para MaxAuthTries, aceitamos valores menores ou iguais ao esperado
                if param == "maxauthtries":
                    try:
                        if int(current_val) <= int(expected):
                            res["status"] = "PASS"
                            res["details"] = f"Configuração segura encontrada: {param} {current_val}"
                        else:
                            res["status"] = "FAIL"
                            res["details"] = f"{rule['fail_msg']} (Atual: {current_val}, Recomendado: <= {expected})"
                    except ValueError:
                        res["status"] = "WARNING"
                        res["details"] = f"Valor inválido para {param}: '{current_val}'"
                else:
                    # Regras de texto (ex: yes/no)
                    if current_val == expected:
                        res["status"] = "PASS"
                        res["details"] = f"Configuração segura encontrada: {param} {current_val}"
                    else:
                        res["status"] = "FAIL"
                        res["details"] = f"{rule['fail_msg']} (Atual: {current_val}, Esperado: {expected})"
            else:
                res["status"] = "WARNING"
                res["details"] = f"Parâmetro '{param}' não está explicitamente declarado no sshd_config (padrão do sistema)."

            results.append(res)

    except Exception as e:
        results.append({
            "category": "SSH Security",
            "check": "Leitura do Arquivo sshd_config",
            "status": "ERROR",
            "details": f"Não foi possível ler o arquivo SSH: {str(e)}"
        })

    return results
