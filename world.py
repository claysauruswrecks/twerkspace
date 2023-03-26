import logging
from uuid import uuid4

from room import Room


class World:
    def __init__(self, config):
        self.id = uuid4()
        self.room = config["room"]
        self.users = {}
        # TODO: support multiple objects
        self.objects = config["object"] or []
        logging.info(f"Created world {self.id}")

    def parse_element(element_type, input_string):
        logging.debug(f"Parsing element {element_type}")
        if element_type == "room":
            logging.debug(f"Parsing room {input_string}")
            return Room(input_string).parse()
        # Other element types can be added here

    def add_element(self, element_type, input_string):
        logging.debug(f"Adding element {element_type}")
        parsed_element = self.parse_element(element_type, input_string)
        if isinstance(parsed_element, Room):
            logging.debug(f"Adding room {input_string}")
            self.room = parsed_element
        # Add other element types to the world as necessary

    def display_room(self):
        logging.debug(f"Displaying room {self.room}")
        return self.room

    def add_user(self, user_id, user):
        logging.debug(f"Adding user {user_id}")
        self.users[user_id] = user

    def remove_user(self, user_id):
        logging.debug(f"Removing user {user_id}")
        del self.users[user_id]

    def set_room(self, room):
        logging.debug(f"Setting room {room}")
        self.room = room

    def display_user(self):
        logging.debug(f"Displaying user {self.users}")
        if self.user:
            print(f"User: {self.user.name}")
            print(f"Description: {self.user.description}")
        else:
            print("User information not available.")

    def display_objects(self):
        logging.debug(f"Displaying objects {self.objects}")
        return self.objects
