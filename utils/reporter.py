
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def display_results(results: list, export_format: str = None, target_name: str = "local"):
    """Exibe os resultados da auditoria no terminal e opcionalmente exporta para arquivo."""
    
    table = Table(title="Relatório de Auditoria de Hardening - Armadillo", show_lines=True)
    
    table.add_column("Categoria", style="cyan", no_wrap=True)
    table.add_column("Item Auditado", style="magenta")
    table.add_column("Status", justify="center", style="bold")
    table.add_column("Detalhes / Recomendações", style="white")

    passed_count = 0
    total_count = len(results)

    for res in results:
        status = res["status"]
        
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
    score = (passed_count / total_count) * 100 if total_count > 0 else 0.0
    score_color = "green" if score >= 80 else "yellow" if score >= 50 else "red"
    
    summary_text = f"\n[bold]Total de Checagens:[/bold] {total_count}\n[bold]Aprovadas:[/bold] {passed_count}\n[bold]Score de Conformidade:[/bold] [{score_color}]{score:.1f}%[/{score_color}]"
    console.print(Panel(summary_text, title="Resumo Executivo", expand=False))

    # Exportação de Relatório se solicitada
    if export_format:
        _export_report(results, score, passed_count, total_count, export_format, target_name)


def _export_report(results: list, score: float, passed: int, total: int, fmt: str, target: str):
    """Função interna para lidar com a gravação do relatório no disco."""
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"reports/armadillo_report_{target}_{timestamp}"

    if fmt == "json":
        filename = f"{filename_base}.json"
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "summary": {
                "total_checks": total,
                "passed_checks": passed,
                "compliance_score": round(score, 2)
            },
            "results": results
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        console.print(f"[+] Relatório JSON exportado com sucesso para: [bold green]{filename}[/bold green]", style="cyan")

    elif fmt == "markdown":
        filename = f"{filename_base}.md"
        md_content = f"""# Relatório de Auditoria de Hardening - Armadillo

- **Data/Hora:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
- **Alvo:** `{target}`
- **Score de Conformidade:** **{score:.1f}%** ({passed}/{total} checagens aprovadas)

## Resultados Detalhados

| Categoria | Item Auditado | Status | Detalhes / Recomendações |
| :--- | :--- | :---: | :--- |
"""
        for res in results:
            status_emoji = "✅ PASS" if res["status"] == "PASS" else "❌ FAIL" if res["status"] == "FAIL" else "⚠️ WARNING"
            md_content += f"| {res['category']} | {res['check']} | {status_emoji} | {res['details']} |\n"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(md_content)
        console.print(f"[+] Relatório Markdown exportado com sucesso para: [bold green]{filename}[/bold green]", style="cyan")
