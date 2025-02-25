"""Session-specific API operations."""
from typing import Dict, List, TypedDict, NotRequired
from ..http import HTTPClient

class SessionAgent(TypedDict):
    """Deprecated session agent object."""
    agentSlug: str
    agentUrl: str

# TODO: switch to this class when /api/session is ready
# class SessionParticipant(TypedDict):
#     """A participant in a session."""
#     username: str
#     role: NotRequired[str]


class SessionAPI:
    """Session management API endpoints."""
    
    def __init__(self, http: HTTPClient):
        self.http = http

    def create(self, 
            challenge_slug: str,
            participants: List[SessionAgent]
        ) -> Dict:
        """Create a new session."""

        # TODO: change this to use /api/session when that's ready
        return self.http.post("api/createSession", {
            "challengeSlug": challenge_slug,
            "agents": participants,
        }) 

    # TODO: switch to this method when /api/session is ready
    # def create(self, 
    #         challenge_slug: str,
    #         participants: List[SessionParticipant]
    #     ) -> Dict:
    #     """Create a new session."""

    #     # TODO: change this to use /api/session when that's ready
    #     return self.http.post("api/sessions", {
    #         "challengeSlug": challenge_slug,
    #         "participants": participants,
    #     }) 

    # TODO: add get method when /api/session is ready
    # def get(self, session_id: str) -> Dict:
    #     """Get session details by ID."""
    #     return self.http.get(f"api/sessions/{session_id}")
