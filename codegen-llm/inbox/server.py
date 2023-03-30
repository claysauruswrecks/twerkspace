import argparse
import logging

import yaml
from flask import Flask, request, jsonify

from interpreter import Interpreter
from user import User
from world import World

app = Flask(__name__)


class MUDServer:
    def __init__(self, world):
        self.world = world

    def handle_command(self, user_id, command, args=None):
        user = self.world.get_user(user_id)
        if not user:
            user = User(user_id, f"User_{len(self.world.users) + 1}")
            self.world.add_user(user_id, user)
        interpreter = Interpreter(self.world, user)
        return interpreter.process_command(command, args)


def load_config(config_path):
    logging.info(f"Loading config from {config_path}")
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config
    logging.info(f"Config loaded")


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    user_id = data["user_id"]
    command = data["command"]
    args = data.get("args", None)

    try:
        response = server.handle_command(user_id, command, args)
    except Exception as e:
        logging.error(f"Error processing command: {e}")
        response = {"error": str(e)}

    return jsonify(response)


def main(args):
    # Load the configuration
    config = load_config(args.config)

    # Create the world
    logging.info("Creating world")
    initial_room = config["room"]
    initial_objects = config.get("objects")
    world = World(initial_room, initial_objects)
    logging.info("World created")

    # Start the server
    global server
    server = MUDServer(world)
    logging.info(f"Starting server on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port)


# Define the parser
parser = argparse.ArgumentParser(description="Description of your app.")

# Define the commands and their options
parser.add_argument(
    "command", choices=["start", "command2"], help="Choose a command to run."
)
parser.add_argument("--config", help="MUD server configuration file.")
parser.add_argument("--host", help="Host address to listen on.")
parser.add_argument("--port", help="Host port to listen on.")
parser.add_argument("--log", default="INFO", help="Log level to use.")

# Parse the arguments
args = parser.parse_args()

# Setup logging
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % args.log)
logging.basicConfig(level=numeric_level)

# Execute the chosen command with the specified options
if args.command == "start":
    logging.info("Starting MUD server...")
    main(args)
