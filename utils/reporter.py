
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def display_results(results: list):
    """Exibe os resultados da auditoria de forma elegante usando a biblioteca Rich."""
    
    # Cria a tabela de resultados
    table = Table(title="Relatório de Auditoria de Hardening - Armadillo", show_lines=True)
    
    table.add_column("Categoria", style="cyan", no_wrap=True)
    table.add_column("Item Auditado", style="magenta")
    table.add_column("Status", justify="center", style="bold")
    table.add_column("Detalhes / Recomendações", style="white")

    passed_count = 0
    total_count = len(results)

    for res in results:
        status = res["status"]
        
        # Define cores e ícones baseados no status
        if status == "PASS":
            status_display = "[green]✅ PASS[/green]"
            passed_count += 1
        elif status == "FAIL":
            status_display = "[red]❌ FAIL[/red]"
        elif status == "WARNING":
            status_display = "[yellow]⚠️ WARNING[/yellow]"
        else:
            status_display = "[blue]ℹ️ ERROR[/blue]"

        table.add_row(
            res["category"],
            res["check"],
            status_display,
            res["details"]
        )

    console.print(table)

    # Cálculo do Compliance Score
    if total_count > 0:
        score = (passed_count / total_count) * 100
    else:
        score = 0.0

    # Define a cor do painel de score baseado na porcentagem
    score_color = "green" if score >= 80 else "yellow" if score >= 50 else "red"
    
    summary_text = f"\n[bold]Total de Checagens:[/bold] {total_count}\n[bold]Aprovadas:[/bold] {passed_count}\n[bold]Score de Conformidade:[/bold] [{score_color}]{score:.1f}%[/{score_color}]"
    
    console.print(Panel(summary_text, title="Resumo Executivo", expand=False))
