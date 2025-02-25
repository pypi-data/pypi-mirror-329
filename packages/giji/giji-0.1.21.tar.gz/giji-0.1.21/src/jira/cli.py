import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from .service import JiraService
from src.pr_summary.cli import verify_pr_config
import os

app = typer.Typer(
    name="jira",
    help="🎫 Gestión de Issues de Jira\n\n"
    "Comandos para interactuar con issues de Jira:\n"
    "- Buscar issues\n"
    "- Ver descripciones\n"
    "- Agregar comentarios",
    no_args_is_help=True,
)

console = Console()


def show_config_error(error: str):
    """Muestra un mensaje de error de configuración formateado"""
    panel = Panel(
        f"[red]{error}[/red]\n\n"
        "[yellow]Para configurar Jira, necesitas configurar las siguientes variables de entorno:[/yellow]\n\n"
        "  export JIRA_SERVER_URL='https://your-domain.atlassian.net'\n"
        "  export JIRA_EMAIL='your.email@company.com'\n"
        "  export JIRA_TOKEN='your-api-token'\n\n"
        "[blue]Para instrucciones detalladas:[/blue]\n"
        "  giji jira config",
        title="[red]⚠️  Error de Configuración[/red]",
        border_style="red",
        padding=(1, 2),
    )
    console.print(panel)


def get_jira_service() -> JiraService:
    """Helper function to create a JiraService instance"""
    try:
        return JiraService.from_env()
    except ValueError as e:
        show_config_error(str(e))
        raise typer.Exit(1)


@app.command(name="config", help="⚙️  Configurar conexión con Jira")
def configure():
    """Configurar las credenciales y conexión con Jira"""
    # Show current configuration
    table = Table(title="Current Jira Configuration")
    table.add_column("Variable", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Status", style="yellow")

    # Check each required variable
    variables = {
        "JIRA_SERVER_URL": "Jira server URL",
        "JIRA_EMAIL": "Your email",
        "JIRA_TOKEN": "API Token",
    }

    any_missing = False
    for env_var, description in variables.items():
        value = os.getenv(env_var)
        if value:
            # Mask token for security
            display_value = "***" if env_var == "JIRA_TOKEN" and value else value
            status = "[green]✓ Set[/green]"
        else:
            display_value = "[red]Not set[/red]"
            status = "[red]✗ Missing[/red]"
            any_missing = True

        table.add_row(env_var, display_value, status)

    console.print(table)

    if any_missing:
        console.print(
            "\n[yellow]To configure Jira, add these lines to your shell profile (~/.zshrc, ~/.bashrc, etc.):[/yellow]"
        )
        console.print("\n[blue]# Jira Configuration[/blue]")
        console.print("export JIRA_SERVER_URL='https://your-domain.atlassian.net'")
        console.print("export JIRA_EMAIL='your.email@company.com'")
        console.print("export JIRA_TOKEN='your-api-token'")

        console.print("\n[yellow]How to get your Jira Server URL:[/yellow]")
        console.print("1. Log in to your Jira instance in your browser")
        console.print(
            "2. Look at the URL in your browser, it should be something like:"
        )
        console.print("   [blue]https://your-company.atlassian.net[/blue]")
        console.print(
            "3. If you're using Jira Server/Data Center instead of Jira Cloud,"
        )
        console.print(
            "   use your custom domain, e.g., [blue]https://jira.your-company.com[/blue]"
        )

        console.print("\n[yellow]Email Address:[/yellow]")
        console.print("• This is the email you use to log in to Jira")

        console.print("\n[yellow]How to get your API Token:[/yellow]")
        console.print(
            "1. Go to [link]https://id.atlassian.com/manage-profile/security/api-tokens[/link]"
        )
        console.print("2. Click 'Create API token'")
        console.print("3. Give it a name (e.g., 'giji-cli')")
        console.print(
            "4. Copy the token - it should look like a long string of random characters"
        )
        console.print("5. Make sure to copy the entire token without any extra spaces")

    else:
        console.print("\n[green]✨ Jira is properly configured![/green]")


@app.command(name="describe", help="📖 Ver descripción de un issue")
def get_issue_description(
    issue_key: str = typer.Argument(
        ..., help="Número de issue (ej: 'PROJECT-123')", show_default=False
    ),
    format: bool = typer.Option(
        False, "--format", "-f", help="Mostrar descripción con formato markdown"
    ),
):
    """
    Obtiene la descripción detallada de un issue de Jira.
    La descripción se formatea como markdown por defecto.

    Ejemplos:
      giji jira describe SIS-123      # Ver descripción
      giji jira describe SIS-123 -f   # Ver con formato
    """
    try:
        jira = get_jira_service()
        description = jira.get_issue_description(issue_key)

        if not description:
            console.print(f"[yellow]⚠️  Issue {issue_key} has no description[/yellow]")
            raise typer.Exit(0)

        if format:
            md = Markdown(description)
            console.print(
                Panel(
                    md,
                    title=f"[blue]📝 Description for {issue_key}[/blue]",
                    expand=False,
                    padding=(1, 2),
                )
            )
        else:
            print(description)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@app.command(name="comment", help="💬 Agregar comentario a un issue")
def add_comment(
    issue_key: str = typer.Argument(..., help="Número de issue (ej: 'PROJECT-123')"),
    comment: str = typer.Argument(..., help="Texto del comentario"),
):
    """
    Agrega un comentario a un issue de Jira.

    Ejemplos:
      giji jira comment SIS-123 "Actualizando estado..."
    """
    try:
        jira = get_jira_service()
        jira.add_comment(issue_key, comment)
        console.print(f"[green]Successfully added comment to {issue_key}[/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@app.command(name="analyze-pr", help="🔍 Analyze PR changes and add comment to Jira ticket")
def analyze_pr(
    api_key: str = typer.Option(
        ...,
        "--api-key",
        "-k",
        help="Gemini API key for generating summaries",
        envvar="GEMINI_API_KEY"
    ),
    base: str = typer.Option(
        "master",
        "--base",
        "-b",
        help="Base branch (e.g., main, develop)",
    ),
):
    """
    Analiza los cambios del PR y agrega un comentario en el ticket de Jira.

    Ejemplos:
      giji jira analyze-pr --base main
    """
    try:
        verify_pr_config()
        jira = get_jira_service()
        jira.analyze_pr_and_comment(api_key, base)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@app.command(name="search", help="🔍 Buscar issues en Jira")
def search_issues(
    query: str = typer.Argument(..., help="Texto a buscar en los issues"),
    limit: int = typer.Option(
        10,
        "--limit",
        "-l",
        help="Número máximo de resultados a mostrar",
    ),
):
    """
    Busca issues de Jira que contengan el texto especificado.
    Muestra detalles del issue y PRs vinculados.

    Ejemplos:
      giji jira search "api auth"           # Búsqueda básica
      giji jira search "frontend" -l 5      # Limitar a 5 resultados
    """
    try:
        jira = get_jira_service()
        issues = jira.search_issues(query, max_results=limit)

        if not issues:
            console.print(f"[yellow]No issues found matching: '{query}'[/yellow]")
            return

        # Create results table
        table = Table(
            title=f"[blue]🔍 Issues matching: '{query}'[/blue]",
            show_header=True,
            header_style="bold cyan",
            show_lines=True,  # Add lines to help readability
        )

        # Reorder columns and remove summary truncation
        table.add_column("Summary", no_wrap=False)  # Allow wrapping for long summaries
        table.add_column("URL", style="blue")
        table.add_column("Status", style="yellow")
        table.add_column("Pull Requests", style="magenta")

        for issue in issues:
            # Create clickable URL
            issue_url = f"[link={issue['url']}]{issue['url']}[/link]"

            # Format PR links
            pr_links = []
            if issue["pr_links"]:
                for pr in issue["pr_links"]:
                    pr_title = pr["title"].replace("[", "\\[").replace("]", "\\]")
                    if len(pr_title) > 50:
                        pr_title = pr_title[:47] + "..."
                    pr_links.append(f"• [link={pr['url']}]{pr_title}[/link]")

            # Add row to table with reordered columns
            row = [
                issue["summary"],  # Full summary without truncation
                issue_url,
                issue["status"],
                "\n".join(pr_links) if pr_links else "",
            ]
            table.add_row(*row)

        console.print(table)
        console.print(f"\n[green]Found {len(issues)} matching issues[/green]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
