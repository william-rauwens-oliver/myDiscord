class Message:
    def __init__(self, content, author, timestamp, reactions=None):
        self.content = content
        self.author = author
        self.timestamp = timestamp
        self.reactions = reactions if reactions is not None else []

    def add_reaction(self, emoji, reactor):
        self.reactions.append((emoji, reactor))

    def text():
        pass