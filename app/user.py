import logging

log = logging.getLogger(__name__)


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.status = {
            "seq": 0,
            "id": self.id,
            "mailbox": [],
        }
        log.debug(f"User {self.id} created")

    def __str__(self):
        return f"{self.id}"

    def update_status(self, new_status):
        log.debug(f"Updating status for user {self.id}")
        # Merge new_status into self.status and increment seq number
        self.status.update(new_status)
        self.status["seq"] += 1

    def send_message(self, from_user, message):
        log.debug(f"Sending message from {from_user} to {self.id}")
        # insert message into mailbox and increment seq number
        self.status["mailbox"].append(f"{from_user}: {message}")
        self.status["seq"] += 1
