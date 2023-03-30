import argparse
import logging

import yaml
from flask import Flask, request, jsonify, g

from app.interpreter import Interpreter
from app.user import User
from app.world import World
from app import settings


class MUDServer:
    def __init__(self, world):
        self.world = world

    def handle_command(self, user_id, command, args=None):
        try:
            user = self.world.get_user(user_id)
            if not user:
                user = User(user_id, f"User_{len(self.world.users) + 1}")
                self.world.add_user(user_id, user)
            interpreter = Interpreter(self.world, user)
            return interpreter.process_command(command, args)
        except Exception as e:
            logging.error(f"Error processing command: {e}")
            return {"error": str(e)}


def load_config(config_path):
    # Load the configuration
    logging.info(f"Loading config from {root_dir}]{config_path}")
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def create_app(config=None):
    app = Flask(__name__)

    @app.before_request
    def before_request():
        if not hasattr(g, "server"):
            initial_room = config["room"]
            initial_objects = config.get("objects")
            world = World(initial_room, initial_objects)
            g.server = MUDServer(world)

    @app.route("/command", methods=["POST"])
    def command():
        data = request.get_json()
        user_id = data["user_id"]
        command = data["command"]
        args = data.get("args", None)

        try:
            response = g.server.handle_command(user_id, command, args)
        except Exception as e:
            logging.error(f"Error processing command: {e}")
            response = {"error": str(e)}

        return jsonify(response)

    return app


def main(args):
    # Load the configuration
    config = load_config(args.config)

    # Create the Flask app
    app = create_app(config)

    # Run the app
    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description="Description of your app.")

    # Define the commands and their options
    parser.add_argument(
        "command", choices=["start"], help="Choose a command to run."
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
