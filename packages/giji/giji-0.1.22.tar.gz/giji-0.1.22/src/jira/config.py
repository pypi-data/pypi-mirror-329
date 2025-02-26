from dataclasses import dataclass
from typing import Optional

@dataclass
class JiraConfig:
    server_url: str
    email: str
    token: str
    project_key: Optional[str] = None

    def __post_init__(self):
        if not self.server_url:
            raise ValueError("Server URL is required")
        if not self.email:
            raise ValueError("Email is required")
        if not self.token:
            raise ValueError("API Token is required")

    @classmethod
    def from_env(cls):
        """
        Create JiraConfig from environment variables:
        - JIRA_SERVER_URL (required): Your Jira instance URL
        - JIRA_EMAIL (required): Your Atlassian account email
        - JIRA_TOKEN (required): Your API token from https://id.atlassian.com/manage-profile/security/api-tokens
        - JIRA_PROJECT_KEY (optional): Default project key
        """
        import os
        
        server_url = os.getenv('JIRA_SERVER_URL')
        if not server_url:
            raise ValueError("Missing required environment variable: JIRA_SERVER_URL")

        email = os.getenv('JIRA_EMAIL')
        if not email:
            raise ValueError("Missing required environment variable: JIRA_EMAIL")

        token = os.getenv('JIRA_TOKEN')
        if not token:
            raise ValueError("Missing required environment variable: JIRA_TOKEN")
            
        project_key = os.getenv('JIRA_PROJECT_KEY')
            
        return cls(
            server_url=server_url,
            email=email,
            token=token,
            project_key=project_key
        ) 