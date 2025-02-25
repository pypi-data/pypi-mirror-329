import os
import subprocess
import time
from typing import Any, Dict, List

import questionary
import google.generativeai as genai
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.conventional_commits import ConventionalCommitsCz
from commitizen.defaults import Questions
from rich import print


class AIConventionalCz(BaseCommitizen):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        print("[blue]Initializing AI Conventional Commitizen...[/blue]")
        self._setup_gemini()
        self._commit_parts = None
        self._conventional_cz = ConventionalCommitsCz(config)
        self._use_ai = True
        self._current_message = None

    def _setup_gemini(self):
        """Configure Gemini API."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("[red]Error: GEMINI_API_KEY environment variable not found![/red]")
            print("[yellow]Please set your Gemini API key using:[/yellow]")
            print("[yellow]export GEMINI_API_KEY='your-api-key'[/yellow]")
            raise ValueError("GEMINI_API_KEY not found")

        try:
            genai.configure(api_key=api_key)
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
            self.model = genai.GenerativeModel(
                model_name="gemini-pro", generation_config=generation_config
            )
            print("[green]Gemini API configured successfully![/green]")
        except Exception as e:
            print(f"[red]Error configuring Gemini API: {e}[/red]")
            raise

    def _get_git_changes(self, with_print=False) -> str:
        try:
            if with_print:
                print("[blue]Checking git changes...[/blue]")

            if with_print:
                print("[blue]Getting staged changes...[/blue]")
            staged_diff = subprocess.check_output(
                ["git", "diff", "--cached"],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            if not staged_diff:
                if with_print:
                    print(
                        "[yellow]No staged changes found, checking unstaged changes...[/yellow]"
                    )
                staged_diff = subprocess.check_output(
                    ["git", "diff"], stderr=subprocess.STDOUT, universal_newlines=True
                )

            if with_print:
                print("[blue]Checking for new files...[/blue]")
            new_files = subprocess.check_output(
                ["git", "ls-files", "--others", "--exclude-standard"],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            changes = []
            if staged_diff:
                if with_print:
                    print("[blue]Found staged changes[/blue]")
                changes.append("Modified files:\n" + staged_diff)
            if new_files:
                if with_print:
                    print("[blue]Found new files[/blue]")
                changes.append("New files:\n" + new_files)

            if not changes:
                if with_print:
                    print(
                        "[yellow]Warning: No changes detected. Have you added files with 'git add'?[/yellow]"
                    )
                return "No changes detected"

            if with_print:
                print(f"[green]Found {len(changes)} change(s)[/green]")
            return "\n".join(changes)

        except subprocess.CalledProcessError as e:
            if with_print:
                print(f"[red]Error executing git command: {e}[/red]")
            return f"Error getting git changes: {e}"

    def questions(self) -> List[Questions]:
        self._use_ai = questionary.confirm(
            "¿Deseas generar el mensaje de commit usando AI?", default=True
        ).ask()

        if self._use_ai:
            self._current_message = self._generate_full_message(with_print=True)
            question_2 = questionary.confirm(
                "¿Te parece adecuado el mensaje de commit?",
                default=True,
            ).ask()
            if not question_2:
                self._current_message = None
                return self._conventional_cz.questions()
            return [
                {
                    "type": "confirm",
                    "name": "good_msg",
                    "message": "Presiona Y para confirmar o N para salir",
                    "default": True,
                }
            ]

        return self._conventional_cz.questions()

    def _generate_ai_commit_message(self, with_print=False) -> Dict[str, str]:
        if with_print:
            print("[blue]Analyzing changes with Gemini AI...[/blue]")
        changes = self._get_git_changes(with_print)

        if changes == "No changes detected":
            if with_print:
                print(
                    "[yellow]No changes to commit. Please stage your changes first with 'git add'.[/yellow]"
                )
            return None

        if with_print:
            print("[blue]Preparing prompt for Gemini...[/blue]")
        prompt_parts = [
            {
                "text": "You are a helpful assistant that generates conventional commit messages. "
                "Generate ONLY a single line commit message following the format: type[(scope)]: description\n\n"
            },
            {
                "text": "Based on the following git changes, generate a conventional commit message:\n\n"
            },
            {"text": f"Git Changes:\n{changes}\n\n"},
            {
                "text": """Rules for the commit message:
                        1. Start with a type (feat, fix, docs, style, refactor, test, chore)
                        2. Optionally add a scope in parentheses
                        3. Add a colon and space
                        4. Add a very short description (max 50 chars)

                        Example formats:
                        docs: update README
                        feat(auth): add login endpoint
                        fix(api): correct status code

                        Return ONLY the single line commit message, nothing else. Keep it short and concise."""
            },
        ]

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                if with_print:
                    print(
                        f"[blue]Generating commit message with Gemini (attempt {attempt + 1}/{max_retries})...[/blue]"
                    )
                response = self.model.generate_content(prompt_parts)

                if not response.candidates:
                    raise Exception("No response candidates received")

                commit_message = response.text.strip()
                if with_print:
                    print("[green]Commit message generated successfully![/green]")
                    print("[blue]Parsing commit message...[/blue]")

                first_line = commit_message.split("\n")[0]
                type_scope = first_line.split(":")[0].strip()

                if "(" in type_scope:
                    type_ = type_scope[: type_scope.find("(")]
                    scope = type_scope[type_scope.find("(") + 1 : type_scope.find(")")]
                else:
                    type_ = type_scope
                    scope = ""

                message = first_line.split(":", 1)[1].strip()
                body = "\n".join(commit_message.split("\n")[1:]).strip()

                if with_print:
                    print("[green]Commit message parsed successfully[/green]")
                return {
                    "type": type_,
                    "scope": scope,
                    "message": message,
                    "body": body,
                    "breaking": "BREAKING CHANGE" in commit_message,
                }

            except Exception as e:
                if with_print:
                    print(
                        f"[red]Error generating commit message (attempt {attempt + 1}): {e}[/red]"
                    )
                if attempt < max_retries - 1:
                    if with_print:
                        print(f"[yellow]Retrying in {retry_delay} seconds...[/yellow]")
                    time.sleep(retry_delay)
                else:
                    if with_print:
                        print(
                            "[red]Failed to generate commit message after all retries[/red]"
                        )
                    return None

    def _generate_full_message(self, with_print=False):
        commit_parts = self._generate_ai_commit_message(with_print)
        if commit_parts is None:
            if with_print:
                print("[red]No commit message to format[/red]")
            return ""

        first_line = f"{commit_parts['type']}"
        if commit_parts["scope"]:
            first_line += f"({commit_parts['scope']})"
        first_line += f": {commit_parts['message']}"
        if with_print:
            print("\n[bold yellow]📝 COMMIT MESSAGE: [/bold yellow]")
            print("[blue]╭" + "─" * (len(first_line) + 4) + "╮[/blue]")
            print(
                f"[blue]│[/blue] [bold green]{first_line}[/bold green] [blue]│[/blue]"
            )
            print("[blue]╰" + "─" * (len(first_line) + 4) + "╯[/blue]")
            print()  # Add an empty line for better spacing
        return first_line

    def message(self, answers: Dict[str, Any]) -> str:
        print("[blue]Formatting commit message...[/blue]")

        try:
            if answers.get("good_msg") is True:
                if self._current_message:
                    return self._current_message
                return self._generate_full_message()
            else:
                return self._conventional_cz.message(answers)

        except Exception as e:
            print(f"[red]Error in message generation: {e}[/red]")
            return ""
