#!/usr/bin/env python3
import argparse
import sys
from target.local_target import LocalTarget
from target.remote_target import RemoteTarget
from checks.ssh_audit import run_ssh_checks
from checks.permissions_audit import run_permission_checks
from checks.users_audit import run_user_checks
from checks.firewall_audit import run_firewall_checks
from utils.reporter import display_results
from rich.console import Console

console = Console()

def print_banner():
    banner = r"""
     _    ____  __  __    _    ____  ___ _      _     _____
    / \  |  _ \|  \/  |  / \  |  _ \|_ _| |    | |   |  _  |
   / _ \ | |_) | |\/| | / _ \ | | | || || |    | |   | | | |
  / ___ \|  _ <| |  | |/ ___ \| |_| || || |___ | |___| |_| |
 /_/   \_\_| \_\_|  |_/_/   \_\____/|___|_____||_____|_____|
    [ Armadillo - Server Hardening Auditor v1.0 ]
    """
    console.print(banner, style="bold bright_cyan")

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="Armadillo - Auditor de Hardening e Conformidade de Servidores")
    parser.add_argument("--target", choices=["local", "remote"], required=True, help="Define se o alvo é local ou remoto.")
    parser.add_argument("--export", choices=["json", "markdown"], help="Exporta o relatório gerado para JSON ou Markdown.")
    
    # Argumentos para conexão remota
    parser.add_argument("--host", help="Endereço IP ou hostname do servidor remoto.")
    parser.add_argument("--port", type=int, default=22, help="Porta SSH (padrão: 22).")
    parser.add_argument("--user", default="root", help="Usuário SSH (padrão: root).")
    parser.add_argument("--key", help="Caminho para a chave privada SSH (ex: ~/.ssh/id_rsa).")
    parser.add_argument("--password", help="Senha SSH (opcional, prefira chaves).")

    args = parser.parse_args()

    target = None
    all_results = []

    try:
        if args.target == "local":
            console.print("[*] Iniciando auditoria no ambiente [bold green]LOCAL[/bold green]...", style="yellow")
            target = LocalTarget()
        elif args.target == "remote":
            if not args.host:
                console.print("[!] Erro: O parâmetro --host é obrigatório para auditorias remotas.", style="bold red")
                sys.exit(1)
            console.print(f"[*] Conectando ao alvo remoto [bold cyan]{args.host}:{args.port}[/bold cyan]...", style="yellow")
            target = RemoteTarget(
                host=args.host,
                port=args.port,
                username=args.user,
                key_path=args.key,
                password=args.password
            )
        
        target.connect()
        console.print("[+] Conexão estabelecida com sucesso!\n", style="bold green")

        # Executando todas as baterias de checagens de segurança
        console.print("[*] Executando módulos de auditoria...", style="yellow")
        
        # Coleta resultados do SSH
        all_results.extend(run_ssh_checks(target))
        
        # Coleta resultados de Permissões
        all_results.extend(run_permission_checks(target))

        #Coleta resultados do usuario
        all_results.extend(run_user_checks(target))

        #Coleta resultados do firewall
        all_results.extend(run_firewall_checks(target))

        target_name = "local" if args.target == "local" else args.host

        console.print("\n[+] Auditoria concluída com sucesso! Gerando relatório...\n", style="bold green")
        
        # Exibe e exporta o relatório formatado
        display_results(all_results, export_format=args.export, target_name=target_name)


    except Exception as e:
        console.print(f"\n[!] Erro crítico durante a execução do Armadillo: {str(e)}", style="bold red")
    finally:
        if target:
            target.close()

if __name__ == "__main__":
    main()
