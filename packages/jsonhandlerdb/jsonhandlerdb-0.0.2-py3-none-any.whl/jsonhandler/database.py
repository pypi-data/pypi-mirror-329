# jsonhandler/database.py
import json
import asyncio
from pathlib import Path
from typing import Type, TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class JSONDatabase(Generic[T]):
    def __init__(self, model: Type[T], file_path: str = 'data.json'):
        """
        model: The Pydantic model class (which should inherit from CustomBase).
        file_path: The JSON file path.
        default_data: Optional dict for initial data if the file is absent.
        """
        self.model = model
        self.file_path = Path(file_path)

        # Instantiate an empty model (which will auto-populate defaults via CustomBase.from_dict)
        self.data: T = model.from_dict({})

    async def load(self) -> T:
        """Asynchronously load data from the JSON file."""
        if self.file_path.exists():
            async with asyncio.Lock():
                with open(self.file_path, 'r') as f:
                    content = json.load(f)
                    # Use from_dict to convert nested dicts into model instances.
                    self.data = self.model.from_dict(content)
        return self.data

    async def save(self):
        """Asynchronously save the current data to the JSON file."""
        async with asyncio.Lock():
            with open(self.file_path, 'w') as f:
                f.write(self.data.model_dump_json(indent=4))

    def to_dict(self) -> dict:
        """Return the data as a dictionary."""
        return self.data.model_dump()

    def from_dict(self, data: dict):
        """Load the database from a dictionary."""
        self.data = self.model.from_dict(data)
