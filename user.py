import logging


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.status = {
            "seq": 0,
            "id": self.name,
            "mailbox": [],
        }
        logging.debug(f"User {self.name} created")

    def __str__(self):
        return f"{self.name}"

    def update_status(self, new_status):
        logging.debug(f"Updating status for user {self.name}")
        # Merge new_status into self.status and increment seq number
        self.status.update(new_status)
        self.status["seq"] += 1

    def send_message(self, from_user, message):
        logging.debug(f"Sending message from {from_user} to {self.name}")
        # insert message into mailbox and increment seq number
        self.status["mailbox"].append(f"{from_user}: {message}")
        self.status["seq"] += 1
