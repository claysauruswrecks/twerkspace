from room import Room


class World:
    def __init__(self):
        self.room = None
        self.users = {}

    def parse_element(element_type, input_string):
        if element_type == "room":
            return Room(input_string).parse()
        # Other element types can be added here

    def add_element(self, element_type, input_string):
        parsed_element = self.parse_element(element_type, input_string)
        if isinstance(parsed_element, Room):
            self.room = parsed_element
        # Add other element types to the world as necessary

    def display_room(self):
        print(f"Room: {self.room.name}")
        print(f"Description: {self.room.description}")
        print(f"Size: {self.room.size.name.lower()}")
        print(f"Exits: {', '.join([exit.name.lower() for exit in self.room.exits])}")

    def add_user(self, user_id, user):
        self.users[user_id] = user

    def remove_user(self, user_id):
        del self.users[user_id]

    def set_room(self, room):
        self.room = room

    def display_user(self):
        if self.user:
            print(f"User: {self.user.name}")
            print(f"Description: {self.user.description}")
        else:
            print("User information not available.")

    def display_objects(self):
        if self.objects:
            for obj in self.objects:
                print(f"Object: {obj.name}")
                print(f"Description: {obj.description}")
                print(f"Size: {obj.size.name.lower()}")
        else:
            print("No objects in the room.")
