"""Shared configuration utilities"""

from dataclasses import dataclass
from typing import Dict, List
from rich.console import Console
from rich.table import Table
import os

console = Console()


@dataclass
class ToolConfig:
    name: str
    description: str
    env_vars: Dict[str, str]
    help_url: str = ""
    setup_instructions: List[str] = None

    def check_env_vars(self) -> Dict[str, bool]:
        """Check if required environment variables are set"""
        return {var: bool(os.getenv(var)) for var in self.env_vars}


# Define configurations by module
TOOL_CONFIGS = {
    "pr": ToolConfig(
        name="Pull Requests",
        description="Generación de PRs con IA",
        env_vars={
            "GEMINI_API_KEY": "API Key para generar descripciones de PRs",
        },
        help_url="https://aistudio.google.com/app/apikey",
        setup_instructions=[
            "1. Visita [link]https://aistudio.google.com/app/apikey[/link]",
            "2. Crea una nueva API key",
            "3. Copia la key y configúrala en tu entorno:",
            "   export GEMINI_API_KEY='your-api-key'",
        ],
    ),
    "commit": ToolConfig(
        name="Smart Commits",
        description="Commits inteligentes con IA",
        env_vars={
            "GEMINI_API_KEY": "API Key para generar mensajes de commit",
        },
        help_url="https://aistudio.google.com/app/apikey",
        setup_instructions=[
            "1. Visita [link]https://aistudio.google.com/app/apikey[/link]",
            "2. Crea una nueva API key",
            "3. Copia la key y configúrala en tu entorno:",
            "   export GEMINI_API_KEY='your-api-key'",
        ],
    ),
    "jira": ToolConfig(
        name="Jira Integration",
        description="Integración con Jira",
        env_vars={
            "JIRA_SERVER_URL": "URL del servidor Jira",
            "JIRA_EMAIL": "Email de tu cuenta",
            "JIRA_TOKEN": "API Token de Jira",
        },
        help_url="https://id.atlassian.com/manage-profile/security/api-tokens",
        setup_instructions=[
            "1. Visita [link]https://id.atlassian.com/manage-profile/security/api-tokens[/link]",
            "2. Crea un nuevo API token",
            "3. Configura las variables en tu entorno:",
            "   export JIRA_SERVER_URL='https://your-domain.atlassian.net'",
            "   export JIRA_EMAIL='your.email@company.com'",
            "   export JIRA_TOKEN='your-api-token'",
        ],
    ),
}


def check_tool_config(tool_name: str) -> bool:
    """Check configuration for a specific tool"""
    if tool_name not in TOOL_CONFIGS:
        console.print(f"[red]Error: Herramienta desconocida '{tool_name}'[/red]")
        return False

    tool = TOOL_CONFIGS[tool_name]
    env_status = tool.check_env_vars()

    # Show tool name and description
    console.print(f"\n[blue]{tool.name}[/blue]")
    console.print(f"[cyan]{tool.description}[/cyan]\n")

    # Create status table
    table = Table(title="Estado de Configuración")
    table.add_column("Variable", style="cyan")
    table.add_column("Descripción", style="white")
    table.add_column("Estado", style="yellow")

    all_set = True
    for var, desc in tool.env_vars.items():
        status = (
            "[green]✓ Configurado[/green]"
            if env_status[var]
            else "[red]✗ No configurado[/red]"
        )
        table.add_row(var, desc, status)
        all_set = all_set and env_status[var]

    console.print(table)

    if not all_set and tool.setup_instructions:
        console.print("\n[yellow]Instrucciones de configuración:[/yellow]")
        for instruction in tool.setup_instructions:
            console.print(instruction)

    return all_set


def check_all_configs() -> bool:
    """Check configuration for all tools"""
    all_configured = True
    for tool_name in TOOL_CONFIGS:
        console.print(f"\n{'=' * 20} {tool_name.upper()} {'=' * 20}")
        tool_configured = check_tool_config(tool_name)
        all_configured = all_configured and tool_configured

    return all_configured
