
class Group:

    def __init__(self, name=None, header=None, footer=None, id=None):
        self.name = name
        self.header = header
        self.footer = footer
        self.id = id

    def __repr__(self):
        return "%s:%s;%s;%s" % (self.id, self.name, self.header, self.footer)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def __gt__(self, other):
        if self.id is None:
            return True
        elif other.id is None:
            return False
        else:
            return int(self.id) > int(other.id)

    def __lt__(self, other):
        if self.id is None:
            return False
        elif other.id is None:
            return True
        else:
            return int(self.id) < int(other.id)

    def __add__(self, other):
        self.name = other.name if other.name is not None else self.name
        self.header = other.header if other.header is not None else self.header
        self.footer = other.footer if other.footer is not None else self.footer
        self.id = other.id if other.id is not None else self.id
        return self
