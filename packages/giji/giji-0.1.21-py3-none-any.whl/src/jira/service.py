from jira import JIRA
from .config import JiraConfig
from .gemini_utils import generate_jira_comment
from typing import Optional
from src.pr_summary.git_utils import get_branch_changes, has_uncommitted_changes
from src.pr_summary.gemini_utils import generate_pr_summary
from src.pr_summary.utils import extract_ticket_from_branch, get_branch_name
import requests
from rich import print


class JiraService:
    def __init__(self, config: JiraConfig):
        self.config = config
        try:
            self.client = JIRA(
                server=config.server_url,
                basic_auth=(config.email, config.token),
                options={"verify": True, "headers": {"Accept": "application/json"}},
            )

            # Test the connection by making a simple API call
            self.client.server_info()

        except requests.exceptions.ConnectionError as e:
            raise ValueError(
                f"Could not connect to Jira server at {config.server_url}. Please check the URL and your internet connection."
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError(
                    "Authentication failed. Please check your email and API token."
                )
            elif e.response.status_code == 403:
                raise ValueError(
                    "Permission denied. Please check your email and API token have the correct permissions."
                )
            else:
                raise ValueError(
                    f"HTTP Error {e.response.status_code}: {e.response.text}"
                )
        except Exception as e:
            raise ValueError(f"Failed to initialize Jira client: {str(e)}")

    def get_issue_description(self, issue_key: str) -> str:
        """
        Get the description of a Jira issue.

        Args:
            issue_key: The Jira issue key (e.g., 'PROJECT-123')

        Returns:
            str: The description of the issue

        Raises:
            ValueError: If there's an error accessing the issue
        """
        try:
            issue = self.client.issue(issue_key)
            return issue.fields.description or ""
        except Exception as e:
            raise ValueError(f"Could not get issue {issue_key}: {str(e)}")

    def update_issue(self, issue_key: str, fields: dict) -> None:
        """
        Update a Jira issue with the provided fields.

        Args:
            issue_key: The Jira issue key (e.g., 'PROJECT-123')
            fields: Dictionary of fields to update

        Raises:
            ValueError: If there's an error updating the issue
        """
        try:
            issue = self.client.issue(issue_key)
            issue.update(fields=fields)
        except Exception as e:
            raise ValueError(f"Could not update issue {issue_key}: {str(e)}")

    def add_comment(self, issue_key: str, comment: str) -> None:
        """
        Add a comment to a Jira issue.

        Args:
            issue_key: The Jira issue key (e.g., 'PROJECT-123')
            comment: The comment text to add

        Raises:
            ValueError: If there's an error adding the comment
        """
        try:
            self.client.add_comment(issue_key, comment)
        except Exception as e:
            raise ValueError(f"Could not add comment to issue {issue_key}: {str(e)}")

    def search_issues(self, query: str, max_results: int = 10) -> list:
        """
        Search for Jira issues using JQL.

        Args:
            query: Text to search in issue summary or description
            max_results: Maximum number of results to return (default: 10)

        Returns:
            list: List of matching issues with their details
        """
        try:
            jql = f'text ~ "{query}" ORDER BY updated DESC'
            issues = self.client.search_issues(jql, maxResults=max_results)

            results = []
            for issue in issues:
                # Get PR links from issue
                pr_links = []

                # Check remote links (GitHub PRs)
                remote_links = self.client.remote_links(issue)
                for link in remote_links:
                    if (
                        "github" in link.object.url.lower()
                        and "pull" in link.object.url.lower()
                    ):
                        pr_links.append(
                            {"title": link.object.title, "url": link.object.url}
                        )

                # Build issue URL
                issue_url = f"{self.config.server_url}/browse/{issue.key}"

                results.append(
                    {
                        "key": issue.key,
                        "summary": issue.fields.summary,
                        "status": issue.fields.status.name,
                        "url": issue_url,
                        "pr_links": pr_links,
                    }
                )

            return results
        except Exception as e:
            raise ValueError(f"Error searching issues: {str(e)}")

    def analyze_pr_and_comment(
        self, api_key: str, base_branch: str = "master", jira_key: Optional[str] = None
    ) -> bool:
        """
        Analiza los cambios del PR y agrega un comentario en el ticket de Jira.

        Args:
            api_key: API key de Gemini para generar resúmenes
            base_branch: Rama base contra la que comparar (por defecto: "master")
            jira_key: Número de ticket de Jira opcional. Si no se proporciona, se intentará extraer del nombre de la rama

        Returns:
            bool: True si el proceso se completó exitosamente, False si hay cambios sin commitear

        Raises:
            ValueError: Si hay un error en el proceso
        """
        try:
            # Check for uncommitted changes first
            if has_uncommitted_changes():
                print("[red]⚠️  Atención: Hay cambios sin commitear[/red]")
                print(
                    "\n[yellow]Para continuar con el análisis del PR, primero necesitas hacer commit de tus cambios:[/yellow]"
                )
                print("\n[blue]Pasos a seguir:[/blue]")
                print("  1. Revisa los cambios pendientes:")
                print("     git status")
                print("  2. crea el commit y el pr :")
                print("     giji pr - <rama a comparar>")
                print(
                    "\n[yellow]Una vez que hayas hecho el commit, puedes volver a ejecutar este comando.[/yellow]"
                )
                return False

            # Get Jira ticket key from branch if not provided
            if not jira_key:
                branch_name = get_branch_name()
                print(f"[blue]Rama actual: {branch_name}[/blue]")
                jira_key = extract_ticket_from_branch(branch_name)
                if not jira_key:
                    raise ValueError(
                        "No se pudo extraer el número de ticket de Jira del nombre de la rama. Por favor, proporciónalo explícitamente."
                    )

            print(
                f"[blue]Obteniendo cambios entre la rama actual y {base_branch}...[/blue]"
            )
            diff = get_branch_changes(base_branch)

            # Debug information
            if not diff.strip():
                print(
                    "[yellow]⚠️  Advertencia: No se detectaron cambios. Esto puede deberse a:[/yellow]"
                )
                print("  • La rama base especificada no es correcta")
                print("  • No hay diferencias entre las ramas")
                print("\n[blue]Sugerencias para solucionar:[/blue]")
                print(f"  1. Verifica que la rama {base_branch} existe:")
                print(f"     git show-ref {base_branch}")
                print("  2. Verifica las diferencias manualmente:")
                print(f"     git diff {base_branch}...HEAD")
                raise ValueError(
                    "No se encontraron cambios para analizar entre las ramas"
                )

            print(f"[green]✓ Se encontraron cambios para analizar[/green]")
            pr_summary = generate_pr_summary(diff, api_key)

            jira_description = self.get_issue_description(jira_key)
            if not jira_description:
                print(
                    f"[yellow]Aviso: El ticket {jira_key} no tiene descripción. Continuando con descripción vacía.[/yellow]"
                )
                jira_description = ""

            comment = generate_jira_comment(pr_summary, jira_description, api_key)
            self.add_comment(jira_key, comment)
            print(
                f"[green]✨ Comentario agregado exitosamente al ticket {jira_key}[/green]"
            )
            return True

        except Exception as e:
            raise ValueError(f"Error al analizar el PR y comentar en Jira: {str(e)}")

    @classmethod
    def from_env(cls):
        """
        Create a JiraService instance using environment variables for configuration.
        """
        config = JiraConfig.from_env()
        return cls(config)
