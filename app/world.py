import logging
import redis
from uuid import uuid4
import json

from .room import Room
from . import settings

log = logging.getLogger(__name__)


class World:
    def __init__(self, config):
        self.id = str(config.get("world_id") or uuid4())
        # self.users = {}
        # self.users_by_name = {}
        # self.messages = []
        # self.objects = initial_objects or []
        # connect to redis
        self.redis = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True,
        )
        log.info(
            f"Connected to redis {settings.REDIS_HOST}:{settings.REDIS_PORT}:{self.redis.ping()}"
        )
        self.redis.set(f"{self.id}:room", config.get("room"))
        self.redis.set(
            f"{self.id}:room:objects", json.dumps(config.get("objects"))
        )
        self.redis.set(f"{self.id}:users", json.dumps([]))
        self.redis.set(f"{self.id}:users_by_name", json.dumps([]))
        self.redis.set(f"{self.id}:messages", json.dumps([]))

        # self.r.set("world", self.world.serialize())
        # self.r.set("users", [user.serialize() for user in self.world.users.values()])
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
        # Update the users list in redis
        users = json.loads(self.redis.get(f"{self.id}:users"))
        users.append(user_id)
        self.redis.set(f"{self.id}:users", json.dumps(users))
        # Update the users_by_name list in redis
        users_by_name = json.loads(self.redis.get(f"{self.id}:users_by_name"))
        users_by_name.append(user.id)
        self.redis.set(f"{self.id}:users_by_name", json.dumps(users_by_name))

    def get_user(self, user_id):
        log.debug(f"Getting user {user_id}")
        # Get the user from redis
        users = json.loads(self.redis.get(f"{self.id}:users"))
        for user in users:
            if user == user_id:
                return user
        return None

    def get_users(self):
        log.debug(f"Getting users from redis...")
        # Get all users from redis
        users = json.loads(self.redis.get(f"{self.id}:users"))
        return users

    def remove_user(self, user_id):
        log.debug(f"Removing user {user_id}")
        # remove user from the users list in redis
        users = json.loads(self.redis.get(f"{self.id}:users"))
        users.remove(user_id)
        self.redis.set(f"{self.id}:users", json.dumps(users))
        # remove user from the users_by_name list in redis
        users_by_name = json.loads(self.redis.get(f"{self.id}:users_by_name"))
        users_by_name.remove(user.id)
        self.redis.set(f"{self.id}:users_by_name", json.dumps(users_by_name))
        return True

    def set_room(self, room):
        log.debug(f"Setting room {room}")
        self.room = room

    def display_user(self):
        log.debug(f"Displaying user {self.users}")
        if self.user:
            print(f"User: {self.user.id}")
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
