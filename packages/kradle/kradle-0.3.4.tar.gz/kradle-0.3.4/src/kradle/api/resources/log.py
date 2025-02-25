"""Session-specific API operations."""
from typing import Dict, List, TypedDict, NotRequired
from ..http import HTTPClient

class LogAPI:
    """Log management API endpoints."""
    
    def __init__(self, http: HTTPClient):
        self.http = http

    def create(self, session_id, participant_id, message, level="info"):
        return self.http.post(
            'api/createLog',
            {
                'level': level,
                'message': message,
                'sessionId': session_id,
                'participantId': participant_id
            },
        )