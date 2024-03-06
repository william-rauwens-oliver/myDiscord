from Server import Server
class Message(Server):
    def __init__(self, content, author, timestamp):
        self.content = content
        self.author = author
        self.timestamp = timestamp
        self.reactions = {}

    def add_reaction(self, emoji, reactor):
        if emoji in self.reactions:
            self.reactions[emoji].append(reactor)
        else:
            self.reactions[emoji] = [reactor]

    def remove_reaction(self, emoji, reactor):
        if emoji in self.reactions and reactor in self.reactions[emoji]:
            self.reactions[emoji].remove(reactor)

    def get_reaction_count(self, emoji):
        return len(self.reactions.get(emoji, []))

    def to_string(self):
        return f"{self.timestamp} {self.author}: {self.content}"