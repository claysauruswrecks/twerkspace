import asyncio


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

            interpreter.process_command(command)

        self.world.remove_user(user_id)
        writer.close()
        await writer.wait_closed()

    async def start(self, host, port):
        server = await asyncio.start_server(self.handle_connection, host, port)
        async with server:
            await server.serve_forever()
