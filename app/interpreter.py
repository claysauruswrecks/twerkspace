import json
import logging
from app import settings

log = logging.getLogger(__name__)


class Interpreter:
    def __init__(self, world, user):
        self.world = world
        self.user = user
        self.commands = {
            "help": self.help,
            "look": self.look,
            "inspect": self.inspect,
            "protocol_connect": self.protocol_connect,
            "say": self.say,
            "whisper": self.whisper,
        }
        self.commands_help = {
            "look": "Look around the room",
            "inspect": {
                "info": "Inspect <object_id> in the room",
                "usage": "inspect <object_id>",
            },
            "say": {
                "info": "Broadcast <message> to the room",
                "usage": "say <message>",
            },
            "whisper": {
                "info": "Send private <message> to <user_id>",
                "usage": "whisper <user_id> <message>",
            },
        }
        log.info(
            f"Interpreter created: {self.world.id}:{self.user}:{self.commands.keys()}"
        )

    def whisper(self, args):
        to_user, message = args.split(" ", 1)
        log.debug(f"Whispering {self.user.name} => {to_user}: {message}")
        self.world.send_message(self.user.name, to_user, message)

    def say(self, args):
        message = args
        log.debug(
            f"Sending message {self.user.name} => {self.world.id}: {message}"
        )
        self.world.broadcast_message(self.user.name, message)
        log.debug("Done sending message")

    def protocol_connect(self, args=None):
        log.debug("Sending connection prompt")
        response = self.return_prompt("protocol_connect")
        log.debug("Done sending connection prompt")
        return response

    def return_prompt(self, prompt_id):
        log.debug(f"Returning prompt: {prompt_id}")
        with open(
            f"{settings.PROMPT_PATH}/{settings.PROTOCOL}/protocol/{prompt_id}.json",
            "r",
        ) as f:
            response = json.load(f)
        response["error"] = False
        log.debug("Done returning prompt")
        return response

    def help(self, args=None):
        log.info("Displaying help")
        response = {}
        response["error"] = False
        response["commands"] = (self.commands_help,)
        return response

    def inspect(self, object_id):
        log.info(f"Inspecting object: {object_id}")
        response = {}
        response["error"] = False
        try:
            response["object"] = self.world.get_object(int(object_id))
        except Exception as e:
            log.error(e)
            response["error"] = str(e)
        log.debug("Done inspecting")
        return response

    def look(self, args=None):
        response = {}
        response["error"] = False
        try:
            log.debug("Looking for display_room")
            response["room"] = self.world.display_room()
            log.debug("Looking for users")
            response["user_ids"] = [u.name for u in self.world.users.values()]
            log.debug("Looking for objects")
            response["object_ids"] = self.world.display_objects()
            response["messages"] = self.world.display_messages()
        except Exception as e:
            log.error(e)
            response["error"] = str(e)
        log.debug("Done hydrating")
        return response

    def process_command(self, command, args=None):
        response = {}
        response["error"] = False
        try:
            log.info(f"Received command: {command, args}")
            if command in self.commands:
                log.info(f"Executing command: {command}")
                response = self.commands[command](args)
                if response is None:
                    response = self.look()
            else:
                log.info(f"Unknown command: {command}")
                return json.dumps({"error": "Unknown command"})
        except Exception as e:
            log.error(e)
            return json.dumps({"error": str(e)})
        # add user status to every successful response
        response["self"] = self.user.status
        return json.dumps(response)

    def run(self):
        while True:
            log.info(f"User: {self.user} waiting for command")
            command = input(f"{self.user.name}> ").strip().lower()
            if command == "quit":
                log.info(f"User {self.user.name} quitting")
                break
            self.process_command(command)
