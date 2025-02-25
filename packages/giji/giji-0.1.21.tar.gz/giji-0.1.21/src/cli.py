import typer
from rich.console import Console
from rich import print
from src.pr_summary.cli import commit_changes_command, create_pr_command
from src.jira.cli import app as jira_cli
from .config import check_tool_config, check_all_configs

# Create console for rich output
console = Console()

# Create main app with better help
app = typer.Typer(
    name="giji",
    help="🛠️  Giji - Herramientas de Desarrollo\n\n"
    "Colección de herramientas para el flujo de desarrollo:\n"
    "- 🤖 Commits inteligentes\n"
    "- 📝 Generación de PRs\n"
    "- 🎫 Integración con Jira",
    no_args_is_help=True,
)

# Add PR command directly
app.command(name="pr", help="📝 Genera y gestiona PRs")(create_pr_command)

# Add commit command
app.command(name="commit", help="🤖 Crea commits inteligentes")(commit_changes_command)

# Add Jira commands as a group
app.add_typer(jira_cli, name="jira", help="🎫 Interactúa con issues de Jira")


@app.command(name="config", help="⚙️ Verificar y configurar herramientas")
def check_config(
    tool: str = typer.Option(
        None,
        "--tool",
        "-t",
        help="Herramienta específica a verificar (pr, commit, jira)",
    ),
):
    """
    Verifica la configuración de las herramientas.

    Si no se especifica una herramienta, verifica todas.

    Ejemplos:
      giji config              # Verificar toda la configuración
      giji config -t pr        # Verificar configuración de PRs
      giji config -t commit    # Verificar configuración de commits
      giji config -t jira      # Verificar configuración de Jira
    """
    if tool:
        check_tool_config(tool.lower())
    else:
        check_all_configs()


def main():
    """Punto de entrada principal para el CLI"""
    try:
        app()
    except Exception as e:
        print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)
