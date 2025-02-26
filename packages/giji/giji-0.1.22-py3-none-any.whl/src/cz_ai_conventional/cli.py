"""CLI commands for cz_ai_conventional"""

import os
import typer
from rich import print
from .version import VERSION

app = typer.Typer(help="Cometa Git Tools CLI")


def setup_global_config():
    """Setup global configuration for commitizen"""
    try:
        home = os.path.expanduser("~")
        config_dir = os.path.join(home, ".commitizen")
        config_file = os.path.join(config_dir, "config.toml")

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        config_content = f"""
                [settings]
                name = "cz_ai_conventional"
                version = "{VERSION}"

                [commitizen]
                name = "cz_ai_conventional"
                version = "{VERSION}"
                tag_format = "v$version"
            """
        with open(config_file, "w") as f:
            f.write(config_content.strip())

        print(
            "[green]✓ Configuración global de commitizen instalada correctamente[/green]"
        )
        return True
    except Exception as e:
        print(f"[red]✗ Error al configurar commitizen global: {e}[/red]")
        return False


def setup_project_config():
    """Setup project configuration in pyproject.toml"""
    try:
        if not os.path.exists("pyproject.toml"):
            project_config = f"""
                    [tool.commitizen]
                    name = "cz_ai_conventional"
                    version = "{VERSION}"
                    tag_format = "v$version"
            """
            with open("pyproject.toml", "w") as f:
                f.write(project_config.strip())
            print("[green]✓ Archivo pyproject.toml creado correctamente[/green]")
        else:
            with open("pyproject.toml", "r") as f:
                content = f.read()

            if "[tool.commitizen]" not in content:
                # Agregamos la configuración al final del archivo
                with open("pyproject.toml", "a") as f:
                    f.write(f"""
                        [tool.commitizen]
                        name = "cz_ai_conventional"
                        version = "{VERSION}"
                        tag_format = "v$version"
                        """)
                print(
                    "[green]✓ Configuración de commitizen agregada a pyproject.toml[/green]"
                )
            else:
                print(
                    "[yellow]! La configuración de commitizen ya existe en pyproject.toml[/yellow]"
                )

        return True
    except Exception as e:
        print(f"[red]✗ Error al configurar pyproject.toml: {e}[/red]")
        return False


@app.command()
def setup(
    global_config: bool = typer.Option(
        True, "--global/--no-global", help="Configurar commitizen globalmente"
    ),
    project_config: bool = typer.Option(
        True,
        "--project/--no-project",
        help="Configurar commitizen en el proyecto actual",
    ),
):
    """Configurar commitizen para usar cz_ai_conventional"""
    if global_config:
        setup_global_config()

    if project_config:
        setup_project_config()

    if not global_config and not project_config:
        print("[yellow]! No se seleccionó ninguna configuración para instalar[/yellow]")


def main():
    """Entry point for the CLI"""
    app()
