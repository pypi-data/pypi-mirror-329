"""Agent-specific API operations."""
from typing import Dict, Any
from ..http import HTTPClient

class AgentAPI:
    """Agent management API endpoints."""
    
    def __init__(self, http: HTTPClient):
        self.http = http

    def list(self) -> Dict:
        """Get all agents."""
        return self.http.get("api/agents")

    def get(self, username: str) -> Dict:
        """Get agent details by username."""
        return self.http.get(f"api/agents/{username}")

    def create(self, username: str, name: str, description: str = None, url: str = None, visibility: str = "private") -> Dict:
        """Create a new agent."""
        # required
        # TODO: slug needs to be renamed to username on API 
        data = {"slug": username, "name": name, "visibility": visibility}
        # optional
        if description is not None:
            data["description"] = description
        if url is not None:
            data["url"] = url
        return self.http.post("api/agents", data)

    def update(self, username: str, name: str = None, description: str = None, url: str = None, visibility: str = None) -> Dict:
        """Update an existing agent."""
        data = {}
        # optional
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if url is not None:
            data["url"] = url
        if visibility is not None:
            data["visibility"] = visibility
        return self.http.put(f"api/agents/{username}", data)


    def delete(self, username: str) -> Dict:
        """Delete an agent."""
        return self.http.delete(f"api/agents/{username}") 



    # TODO: remove this or just return this in the GET /api/agents/{username} endpoint
    def get_agent_behavior(self, username: str) -> Dict:
        """
        Internal: Used to get the behavior of a no-code agent.
        """
        return self.http.get("api/getAgentBehavior", {
            'agentSlug': username,
        })