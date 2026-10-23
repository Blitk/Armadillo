
def run_sysctl_checks(target) -> list:
    """Audita configurações de segurança do Kernel via sysctl."""
    results = []
    
    # Checagem: Proteção contra IP Spoofing (rp_filter)
    res_rp = {
        "category": "Kernel Hardening",
        "check": "Validação de RPFinder (Proteção contra IP Spoofing)",
        "status": "FAIL",
        "details": ""
    }

    try:
        # Lê o parâmetro do kernel via comando sysctl ou cat direto
        output = target.run_command("sysctl -n net.ipv4.conf.all.rp_filter")
        value = output.strip()
        
        # O valor recomendado para hardening é 1 (strict mode) ou 2 (loose)
        if value in ["1", "2"]:
            res_rp["status"] = "PASS"
            res_rp["details"] = f"Configuração segura encontrada (rp_filter = {value})."
        else:
            res_rp["status"] = "FAIL"
            res_rp:: "details" = f"Inseguro: rp_filter está configurado como {value} (Recomendado: 1)."
            
    except Exception as e:
        # Caso rode em containers Docker isolados onde sysctl é restrito
        res_rp["status"] = "WARNING"
        res_rp["details"] = f"Não foi possível ler o parâmetro do kernel (ambiente restrito?): {str(e)}"

    results.append(res_rp)
    return results
