import logging
from uuid import uuid4


class World:
    def __init__(self, initial_room, initial_objects=None):
        self.id = uuid4()
        self.room = initial_room
        self.users = {}
        self.users_by_name = {}
        self.messages = []
        self.objects = initial_objects or []
        logging.info(f"Created world {self.id}")

    # ... (rest of the methods remain unchanged) ...
