from typing import Any, Optional
import json
from enum import Enum
from kradle.memory.abstract_memory import AbstractMemoryStore, Memory


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore




class FirestoreMemory(AbstractMemoryStore):
    collection_name = ""
    service_account_path = ""
    _db = None  # Class variable to store the database instance

    @classmethod
    def initialize_firebase(cls):
        """Initialize Firebase app and database connection if not already initialized"""
        if not cls._db:
            if not cls.collection_name:
                raise ValueError("Collection name is not set")
            if not cls.service_account_path:   
                raise ValueError("Service account path is not set")
            try:
                # Use a service account.
                cred = credentials.Certificate(cls.service_account_path)
                firebase_admin.initialize_app(cred)
                cls._db = firestore.client()
                print(f"Firebase initialized with service account from {cls.service_account_path}")
            except Exception as e:
                print(f"Error initializing Firestore memory store: {str(e)}")
                raise e

    def __init__(self, participant_id: Optional[str] = None):
        """Initialize Firestore memory store"""
        print(f"Initializing Firestore memory store for participant {participant_id}")
        self.initialize_firebase()
        object.__setattr__(
            self, "doc_ref", self._db.collection(self.collection_name).document(participant_id)
        )


    def save_memory(self, key: str, data: Any) -> None:
        """Save data as a field in the Firestore document"""
        try:
            # Serialize data to JSON-compatible format
            serialized_data = json.dumps(data, default=self._serialize_object)
            # Only use json.loads if the data was actually serialized to a string
            if isinstance(data, (list, dict)):
                print(f"Attempting to save {key, data} to Firestore...")
                self.doc_ref.set({key: data}, merge=True)
                print(f"Successfully saved {key} to Firestore")
            else:
                print(f"Attempting to save {key} to Firestore...")
                self.doc_ref.set({key: json.loads(serialized_data)}, merge=True)
                print(f"Successfully saved {key} to Firestore")
        except Exception as e:
            print(f"Error saving to Firestore: {str(e)}")
            print(f"Document reference: {self.doc_ref.path}")
            print(f"Data being saved: {key}: {data}")
            raise

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