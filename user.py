class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.status = {"seq": 0}

    def __str__(self):
        return f"{self.name}"

    def update_status(self, new_status):
        # Merge new_status into self.status and increment seq number
        self.status.update(new_status)
        self.status["seq"] += 1
