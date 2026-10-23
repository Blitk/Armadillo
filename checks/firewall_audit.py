

def run_firewall_checks(target) -> list:
    """Verifica o estado das regras de firewall do sistema."""
    results = []
    
    res_ufw = {
        "category": "Network Security",
        "check": "Status do Firewall UFW (Uncomplicated Firewall)",
        "status": "FAIL",
        "details": ""
    }

    try:
        # Executa o comando para verificar o status do ufw
        output = target.run_command("ufw status")
        
        if "status: active" in output.lower():
            res_ufw["status"] = "PASS"
            res_ufw["details"] = "O firewall UFW está ativo e protegendo o servidor."
        else:
            res_ufw["status"] = "FAIL"
            res_ufw["details"] = "O firewall UFW está inativo. Recomenda-se ativá-lo."
            
    except Exception as e:
        # Se o comando falhar (por exemplo, se o UFW não estiver instalado na distro)
        res_ufw["status"] = "WARNING"
        res_ufw["details"] = f"Não foi possível verificar o UFW (pode não estar instalado): {str(e)}"

    results.append(res_ufw)
    return results
