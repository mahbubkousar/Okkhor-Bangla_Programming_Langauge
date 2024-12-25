class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f'Token({self.type}, "{self.value}", line={self.line}, col={self.column})'

    def __repr__(self):
        return self.__str__()
