import argparse
import asyncio
import logging

import yaml

from interpreter import Interpreter
from user import User
from world import World


class MUDServer:
    def __init__(self, world):
        self.world = world

    async def handle_connection(self, reader, writer):
        user_id = writer.transport.get_extra_info("peername")
        user = User(user_id, f"User_{len(self.world.users) + 1}")
        self.world.add_user(user_id, user)
        interpreter = Interpreter(self.world, user)

        while True:
            command = await reader.readline()
            if not command:
                break

            command = command.decode().strip().lower()
            if command == "quit":
                break

            try:
                logging.debug("Processing command.")
                if len(command.split(" ", 1)) == 1:
                    args = None
                else:
                    command, args = command.split(" ", 1)
                response = interpreter.process_command(command, args)
                logging.debug(f"Encoding: {response}")
                encoded_response = response.encode() + b"\n"
                logging.debug("Sending response.")
                print(encoded_response)
            except Exception as e:
                logging.error(f"Error processing command: {e}")
                response = {"error": str(e)}
                encoded_response = response.encode() + b"\n"
            writer.write(encoded_response)
            await writer.drain()

        self.world.remove_user(user_id)
        writer.close()
        await writer.wait_closed()

    async def start(self, host, port):
        server = await asyncio.start_server(self.handle_connection, host, port)
        async with server:
            await server.serve_forever()


def load_config(config_path):
    logging.info(f"Loading config from {config_path}")
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config
    logging.info(f"Config loaded")


def main(args):
    # Load the configuration
    config = load_config(args.config)

    # Create the world
    logging.info("Creating world")
    world = World(config)
    logging.info("World created")

    # Start the server
    server = MUDServer(world)
    logging.info(f"Starting server on {args.host}:{args.port}")
    asyncio.run(server.start(args.host, args.port))


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
