from typing import Any, Optional
import json
from enum import Enum
from google.cloud import firestore
from google.cloud.firestore import Client
from kradle.memory.abstract_memory import AbstractMemoryStore, Memory

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firebase-credentials.json"


class FirestoreMemory(AbstractMemoryStore):
    def __init__(self, document_path: str, client: Optional[Client] = None):
        """Initialize Firestore memory store
        
        Args:
            document_path: Full path to the Firestore document (e.g. 'memories/user1')
            client: Optional Firestore client. If not provided, creates a new one
        """
        # Use object.__setattr__ to bypass our custom __setattr__ for initialization
        object.__setattr__(self, 'db', client or firestore.Client())
        
        # Split path into collection/document parts and create document reference
        path_parts = document_path.split('/')
        if len(path_parts) % 2 != 0:
            raise ValueError("Document path must have an even number of segments (collection/document pairs)")
        object.__setattr__(self, 'doc_ref', self.db.document(document_path))

    def save_memory(self, key: str, data: Any) -> None:
        """Save data as a field in the Firestore document"""
        # Serialize data to JSON-compatible format
        serialized_data = json.dumps(data, default=self._serialize_object)
        # Only use json.loads if the data was actually serialized to a string
        if isinstance(data, (list, dict)):
            self.doc_ref.set({key: data}, merge=True)
        else:
            self.doc_ref.set({key: json.loads(serialized_data)}, merge=True)

    def load_memory(self, key: str) -> Optional[Any]:
        """Load specific field from the Firestore document"""
        doc = self.doc_ref.get()
        if not doc.exists:
            return None
        value = doc.get(key)
        return json.loads(json.dumps(value)) if value is not None else None

    def _serialize_object(self, obj):
        """Helper method to serialize special objects"""
        if isinstance(obj, Enum):
            return {"__enum__": str(obj)}
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    def load_all_memory(self) -> Memory:
        """Load all fields from the Firestore document"""
        memory = Memory()
        doc = self.doc_ref.get()
        if doc.exists:
            memory.data = doc.to_dict() or {}
        return memory

    def flush_all_memory(self, participant_id: Optional[str] = None) -> None:
        self.doc_ref.delete()

    def __getattr__(self, name: str) -> Any:
        if name in ('db', 'doc_ref') or name.startswith('_'):
            return object.__getattribute__(self, name)
            # raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return self.load_memory(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ('db', 'doc_ref') or name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            self.save_memory(name, value)