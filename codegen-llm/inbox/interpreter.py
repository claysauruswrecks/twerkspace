class Interpreter:
    def __init__(self, world, user):
        self.world = world
        self.user = user
        self.commands = {
            "look": self.look,
        }

    def look(self):
        self.world.display_room()
        print(
            f"Users present: {', '.join([str(u) for u in self.world.users.values()])}"
        )
        self.world.display_objects()

    def process_command(self, command):
        if command in self.commands:
            self.commands[command]()
        else:
            print("Unknown command")

    def run(self):
        while True:
            command = input(f"{self.user.name}> ").strip().lower()
            if command == "quit":
                break
            self.process_command(command)
