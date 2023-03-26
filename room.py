import re
from base import Element, Size, Direction


class Room(Element):
    def validate_size(self, size):
        try:
            return Size[size.upper()]
        except KeyError:
            raise ValueError(
                f"Invalid room size: '{size}', must be one of {', '.join([s.name.lower() for s in Size])}"
            )

    def validate_exits(self, exits):
        valid_exits = []
        for exit in exits:
            try:
                valid_exits.append(Direction[exit.upper()])
            except KeyError:
                raise ValueError(
                    f"Invalid room exit: '{exit}', must be one of {', '.join([d.name.lower() for d in Direction])}"
                )
        return valid_exits

    def parse(self):
        room_pattern = r"Room\((.+)\)"
        room_match = re.match(room_pattern, self.input_string)
        if room_match:
            room_properties = room_match.group(1).split(",")
            self.name = room_properties[0].strip()
            self.description = room_properties[1].strip()
            self.size = self.validate_size(room_properties[2].strip())
            self.exits = self.validate_exits(
                [exit.strip() for exit in room_properties[3].split(";")]
            )
        else:
            raise ValueError("Invalid room element syntax")
