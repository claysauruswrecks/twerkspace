import logging
from uuid import uuid4

from .room import Room

log = logging.getLogger(__name__)


class World:
    def __init__(self, initial_room, initial_objects=None):
        self.id = uuid4()
        self.room = initial_room
        self.users = {}
        self.users_by_name = {}
        self.messages = []
        self.objects = initial_objects or []
        log.info(f"Created world {self.id}")

    def parse_element(element_type, input_string):
        log.debug(f"Parsing element {element_type}")
        if element_type == "room":
            log.debug(f"Parsing room {input_string}")
            return Room(input_string).parse()
        # Other element types can be added here

    def add_element(self, element_type, input_string):
        log.debug(f"Adding element {element_type}")
        parsed_element = self.parse_element(element_type, input_string)
        if isinstance(parsed_element, Room):
            log.debug(f"Adding room {input_string}")
            self.room = parsed_element
        # Add other element types to the world as necessary

    # Broadcast a message by adding it to the messages list
    def broadcast_message(self, from_user, message):
        log.debug(f"Broadcasting message {from_user}")
        self.messages.append(f"{from_user}: {message}")

    def send_message(self, from_user, to_user, message):
        log.debug(f"Sending message from {from_user} to {to_user}")
        self.users_by_name[to_user].send_message(from_user, message)

    def display_messages(self):
        log.debug(f"Displaying messages {self.messages}")
        return self.messages

    def display_room(self):
        log.debug(f"Displaying room {self.room}")
        return self.room

    def add_user(self, user_id, user):
        log.debug(f"Adding user {user_id}")
        self.users[user_id] = user
        self.users_by_name[user.name.lower()] = user

    def get_user(self, user_id):
        log.debug(f"Getting user {user_id}")
        return self.users.get(user_id)

    def remove_user(self, user_id):
        log.debug(f"Removing user {user_id}")
        user = self.users[user_id]
        del self.users_by_name[user.name.lower()]
        del self.users[user_id]
        return True

    def set_room(self, room):
        log.debug(f"Setting room {room}")
        self.room = room

    def display_user(self):
        log.debug(f"Displaying user {self.users}")
        if self.user:
            print(f"User: {self.user.name}")
            print(f"Description: {self.user.description}")
        else:
            print("User information not available.")

    def display_objects(self):
        log.debug(f"Displaying objects {self.objects}")
        # Return list of objects by keys
        return list(self.objects.keys())

    def get_object(self, object_id):
        log.debug(f"Getting object {object_id}")
        # Return object from dict by id
        return self.objects[object_id]
