import argparse
import logging

import redis
import yaml
from flask import Flask, g, jsonify, request

from . import settings
from .interpreter import Interpreter
from .user import User
from .world import World

log = logging.getLogger(__name__)

r = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)


class MUDServer:
    def __init__(self, world):
        self.world = world

    def handle_command(self, user_id, command, command_args=None):
        log.debug(
            f"Handling command {command} for user {user_id} with args {command_args}"
        )
        if not user_id:
            user = User(f"User_{len(self.world.get_users()) + 1}")
            self.world.add_user(user.id, user)
        else:
            user = self.world.get_user(user_id)
            if not user:
                log.error(f"User {user_id} not found")
                return {"error": f"User {user_id} not found, please connect"}
        interpreter = Interpreter(self.world, user)
        return interpreter.process_command(command, command_args)


def load_config(config_path):
    # Load the configuration
    log.info(f"Loading config from {root_dir}]{config_path}")
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def create_app(config=None):
    app = Flask(__name__)

    @app.before_request
    def before_request():
        if not hasattr(g, "server"):
            world = World(config, r)
            g.world_id = world.id
            g.server = MUDServer(world)

    @app.route("/command", methods=["POST"])
    def command():
        data = request.get_json()
        user_id = data.get("user_id")
        command = data["command"]
        args = data.get("args", None)

        try:
            response = g.server.handle_command(user_id, command, args)
        except Exception as e:
            log.error(f"Error processing command: {e}")
            response = {"error": str(e)}

        return response

    @app.route("/users", methods=["GET"])
    def users():
        users = r.get(f"{g.world_id}:users")

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
    numeric_level = getattr(log, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % args.log)
    log.basicConfig(level=numeric_level)

    # Execute the chosen command with the specified options
    if args.command == "start":
        log.info("Starting MUD server...")
        main(args)
