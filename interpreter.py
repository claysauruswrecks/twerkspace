import json
import logging


class Interpreter:
    def __init__(self, world, user):
        self.world = world
        self.user = user
        self.commands = {
            "look": self.look,
        }
        logging.info(
            f"Interpreter created: {self.world.id}:{self.user}:{self.commands.keys()}"
        )

    def look(self):
        response = {}
        try:
            logging.debug("Looking for display_room")
            response["room"] = self.world.display_room()
            logging.debug("Looking for users")
            response["users"] = [u.name for u in self.world.users.values()]
            logging.debug("Looking for objects")
            response["objects"] = self.world.display_objects()
        except Exception as e:
            logging.error(e)
            response["error"] = str(e)
        response["error"] = False
        logging.debug("Done hydrating")
        return json.dumps(response)

    def process_command(self, command):
        logging.info(f"Received command: {command}")
        if command in self.commands:
            logging.info(f"Executing command: {command}")
            try:
                return self.commands[command]()
            except Exception as e:
                return json.dumps({"error": str(e)})
        else:
            logging.info(f"Unknown command: {command}")
            return json.dumps({"error": "Unknown command"})

    def run(self):
        while True:
            logging.info(f"User: {self.user} waiting for command")
            command = input(f"{self.user.name}> ").strip().lower()
            if command == "quit":
                logging.info(f"User {self.user.name} quitting")
                break
            self.process_command(command)
