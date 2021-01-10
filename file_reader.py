class FilerReader():
    def __init__(self, path):
        self.path = path
        self.loc = 0
        with open(path, "rb") as file:
            self.lines = file.read().decode().splitlines()

    def read(self):
        with open(path, "rb") as file:
            return file.read().decode()

    def next_line(self):
        if self.loc < len(self.lines):
            line = self.lines[self.loc]
            self.loc += 1
            return line

        else:
            return None

    def has_next_line(self):
        return self.loc < len(self.lines)

    def get_line(self, loc):
        return self.lines[loc]

    def readlines(self):
        return self.lines
