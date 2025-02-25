"""Giji CLI - Git tools powered by AI"""

from src.pr_summary.utils import extract_ticket_from_branch
import typer
import os
import subprocess
import tempfile
from typing import Optional, Tuple
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.status import Status
from .git_utils import (
    get_branch_changes,
    has_uncommitted_changes,
    commit_changes,
    get_branch_name,
    push_branch,
)
from .gemini_utils import generate_pr_summary
from ..config import check_tool_config
from src.jira.service import JiraService
from src.jira.gemini_utils import generate_jira_comment

app = typer.Typer(
    help="""
Giji - Herramientas Git potenciadas por IA

Crea commits inteligentes y pull requests con descripciones generadas por IA.

Comandos:
  commit    Crea commits inteligentes [--help, -k]
  pr        Crea pull requests [--help, -b, -t, -d, -n, -k]
  examples  Muestra ejemplos de uso

Ejemplos básicos:
  giji commit              # Crear commits inteligentes
  giji pr -b main         # Crear PR a rama main
  giji examples           # Ver más ejemplos
""",
    short_help="Herramientas Git potenciadas por IA",
)
console = Console()


def build_pr_command(body_content: str, base_branch: str) -> Tuple[str, str]:
    """Build the GitHub CLI command for creating a PR"""
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md")
    temp_file.write(body_content)
    temp_file.close()

    # Get branch name for PR title
    branch = get_branch_name()

    # Build the gh cli command with only required options
    command = (
        f"gh pr create "
        f'--title "feat: {branch}" '
        f"--body-file {temp_file.name} "
        f"--base {base_branch} "
    )

    return command, temp_file.name


def show_command_panel(command: str):
    """Display a nice panel with the command"""
    panel = Panel(
        f"[bold white]{command}[/bold white]",
        title="[bold blue]Run this command to create your PR[/bold blue]",
        border_style="green",
        padding=(1, 2),
    )
    print("\n")
    console.print(panel)
    print("\n")


def prepare_pr(
    api_key: str,
    base_branch: str,
    jira_number: Optional[str] = None,
    auto_commit: bool = False,
) -> Tuple[str, str, str]:
    """Prepare PR by handling commits and generating summary"""
    # Try to detect JIRA ticket from branch name if not provided
    if not jira_number:
        branch_name = get_branch_name()
        detected_ticket = extract_ticket_from_branch(branch_name)
        if detected_ticket:
            print(f"[green]✓ Detected JIRA ticket: {detected_ticket}[/green]")
            jira_number = detected_ticket

    # Handle uncommitted changes if auto_commit is True
    if auto_commit and has_uncommitted_changes():
        print("[yellow]ℹ Found uncommitted changes[/yellow]")
        with Status("[bold blue]Creating commits...[/bold blue]"):
            try:
                commit_changes(api_key)
            except Exception as e:
                print(f"[bold red]Error: {str(e)}[/bold red]")
                raise typer.Exit(1)

    # Push changes to remote
    with Status("[bold blue]Pushing changes to remote...[/bold blue]"):
        try:
            push_branch()
        except Exception as e:
            print(f"[bold red]Error: {str(e)}[/bold red]")
            raise typer.Exit(1)

    # Get and analyze changes
    with Status("[bold blue]Analyzing changes...[/bold blue]"):
        diff = get_branch_changes(base_branch)
        if not diff.strip():
            print(
                "[bold yellow]Advertencia: No se encontraron cambios en la rama para generar resumen[/bold yellow]"
            )
            raise typer.Exit(1)

    # Generate PR summary
    with Status("[bold blue]Generating PR summary...[/bold blue]"):
        try:
            summary = generate_pr_summary(diff, api_key, jira_number)
            command, temp_file = build_pr_command(summary, base_branch)
            return summary, command, temp_file
        except Exception as e:
            print(f"[bold red]Error generando resumen: {str(e)}[/bold red]")
            raise typer.Exit(1)


@app.command(
    name="examples",
    help="Muestra ejemplos de uso de los comandos",
    short_help="Muestra ejemplos",
)
def show_examples():
    """Muestra ejemplos detallados de uso de los comandos."""
    examples = """
[bold blue]Ejemplos de Uso de Giji[/bold blue]

[bold yellow]Configuración:[/bold yellow]
  # Configurar API key de Gemini (recomendado)
  export GEMINI_API_KEY='your-api-key'

[bold yellow]Commits Inteligentes:[/bold yellow]
  # Commit básico
  giji commit

  # Commit especificando API key
  giji commit -k your-api-key

[bold yellow]Pull Requests:[/bold yellow]
  # PR básico a main
  giji pr -b main

  # PR como borrador
  giji pr -b main -d

  # PR especificando ticket JIRA
  giji pr -b main -t SIS-123

  # PR sin auto-commit
  giji pr -b main -n

  # PR completo
  giji pr -b main -d -t SIS-123 -k your-api-key

[bold yellow]Formatos de Rama Soportados:[/bold yellow]
  SIS-123                    ✓  # Número de ticket directo
  SIS-123/mi-feature        ✓  # Con descripción
  feature/SIS-123           ✓  # Con tipo
  fix/SIS-123-bug-fix       ✓  # Tipo y descripción
  feature/SIS-123/new-feat  ✓  # Formato completo

[bold yellow]Opciones Disponibles:[/bold yellow]
  -k, --api-key  API key de Gemini
  -b, --base     Rama base (default: master)
  -t, --ticket   Número de ticket JIRA
  -d, --draft    Crear PR como borrador
  -n, --no-commit  No hacer commit automático
  --help        Mostrar ayuda del comando
    """
    console.print(examples)


def verify_gemini_config():
    """Verify Gemini configuration before running commands"""
    if not check_tool_config("gemini"):
        raise typer.Exit(1)


def verify_pr_config():
    """Verify PR configuration before running commands"""
    if not check_tool_config("pr"):
        raise typer.Exit(1)


def verify_commit_config():
    """Verify commit configuration before running commands"""
    if not check_tool_config("commit"):
        raise typer.Exit(1)


@app.command(
    name="commit",
    help="Crea commits inteligentes para tus cambios usando IA",
    short_help="Crea commits inteligentes",
)
def commit_changes_command(
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help="API key de Gemini (o usar variable GEMINI_API_KEY)",
        envvar="GEMINI_API_KEY",
    ),
):
    """
    Crea commits inteligentes para tus cambios usando IA.

    El comando analizará tus cambios y creará uno o más commits con
    mensajes convencionales generados por IA.

    Ejemplos:
      giji commit              # Usando GEMINI_API_KEY
      giji commit -k api-key   # Especificando API key

    Ver más ejemplos:
      giji examples
    """
    verify_commit_config()
    if not api_key:
        print(
            "[bold red]Error: GEMINI_API_KEY not found. Please provide it as an argument (-k) or set it as an environment variable.[/bold red]"
        )
        raise typer.Exit(1)

    if not has_uncommitted_changes():
        print("[yellow]No changes to commit[/yellow]")
        raise typer.Exit(0)

    try:
        with Status("[bold blue]Creating smart commits...[/bold blue]"):
            commit_changes(api_key)
        print("[bold green]✨ Changes committed successfully![/bold green]")
    except Exception as e:
        print(f"[bold red]Error: {str(e)}[/bold red]")
        raise typer.Exit(1)


@app.command(
    name="pr",
    help="Crea un Pull Request con descripción generada por IA",
    short_help="Crea pull requests",
)
def create_pr_command(
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help="API key de Gemini (o usar variable GEMINI_API_KEY)",
        envvar="GEMINI_API_KEY",
    ),
    base: str = typer.Option(
        "master",
        "--base",
        "-b",
        help="Rama base (ej: main, develop)",
    ),
    ticket: Optional[str] = typer.Option(
        None,
        "--ticket",
        "-t",
        help="Número de ticket JIRA (ej: SIS-290). Se detecta automáticamente de la rama",
    ),
    draft: bool = typer.Option(
        False,
        "--draft",
        "-d",
        help="Crear PR como borrador",
    ),
    no_commit: bool = typer.Option(
        False,
        "--no-commit",
        "-n",
        help="Omitir auto-commit de cambios",
    ),
    comment: bool = typer.Option(
        False,
        "--comment",
        "-c",
        help="Agregar comentario en Jira",
    ),
):
    """
    Crea un Pull Request con descripción generada por IA.

    Este comando:
    1. Hace commit de los cambios pendientes (a menos que se use -n/--no-commit)
    2. Sube los cambios al remoto
    3. Genera una descripción detallada del PR
    4. Crea y abre el PR en tu navegador

    El número de ticket JIRA se detecta automáticamente del nombre de la rama.
    Formatos soportados:
    - SIS-123
    - SIS-123/description
    - type/SIS-123-description
    - feature/SIS-123/new-feature
    - fix/SIS-123

    Ejemplos:
      giji pr -b main         # PR básico
      giji pr -b main -d      # PR como borrador
      giji pr -b main -t SIS-123  # Con ticket
      giji pr -b main -n      # Sin auto-commit

    Ver más ejemplos:
      giji examples
    """
    verify_pr_config()
    if not api_key:
        print(
            "[bold red]Error: GEMINI_API_KEY no encontrado. Por favor proporcionalo como argumento (-k) o establecelo como variable de entorno.[/bold red]"
        )
        raise typer.Exit(1)

    try:
        summary, command, temp_file = prepare_pr(
            api_key, base, ticket, auto_commit=not no_commit
        )

        with Status("[bold blue]Creating PR...[/bold blue]"):
            try:
                # Add draft flag if requested
                if draft:
                    command += " --draft"

                # Create the PR
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True
                )

                # Clean up temp file
                os.unlink(temp_file)

                if result.returncode == 0:
                    print("\n[bold green]✨ PR creado exitosamente![/bold green]")
                    pr_url = result.stdout.strip()
                    print(f"[bold white]URL del PR: {pr_url}[/bold white]")

                    # Add comment to Jira if requested
                    if comment:
                        print("[blue]Agregando comentario en Jira...[/blue]")
                        try:
                            jira = JiraService.from_env()
                            jira_key = (
                                ticket
                                if ticket
                                else extract_ticket_from_branch(get_branch_name())
                            )
                            if not jira_key:
                                print(
                                    "[yellow]⚠️  No se pudo encontrar el número de ticket de Jira. Omitiendo comentario.[/yellow]"
                                )
                            else:
                                jira_description = jira.get_issue_description(jira_key)
                                comment = generate_jira_comment(
                                    summary, jira_description, api_key
                                )
                                jira.add_comment(jira_key, comment)
                                print(
                                    "[green]✨ Comentario agregado exitosamente en Jira[/green]"
                                )
                        except Exception as e:
                            print(
                                f"[yellow]⚠️  No se pudo agregar el comentario en Jira: {str(e)}[/yellow]"
                            )
                            print(
                                "[yellow]El PR se creó correctamente, pero hubo un problema al agregar el comentario.[/yellow]"
                            )

                    subprocess.run(["open", pr_url], check=True)
                else:
                    print("\n[bold red]Error al crear el PR:[/bold red]")
                    print(f"[red]{result.stderr}[/red]")
                    raise typer.Exit(1)

            except Exception as e:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                raise e

    except Exception as e:
        print(f"[bold red]Error: {str(e)}[/bold red]")
        raise typer.Exit(1)


def main():
    app()
