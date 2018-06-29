#!/usr/bin/python

from enum import Enum

class TokenType(Enum):
    comment = -3
    # structure
    #newline = -2
    eof = -1
    # definition
    definition = 1
    private_definition = 2
    # scope
    scope_begin = 3
    scope_end = 4
    # basic operations
    assignment = 5
    application = 6
    composition = 7
    # literals
    string_literal = 201
    integer_literal = 202
    float_literal = 203
    # identifiers
    atom = 200
    identifier = 300
    type_anotation = 301
    # control
    operator = 100
    round_bracket_open = 101
    round_bracket_close = 102
    square_bracket_open = 103
    square_bracket_close = 104
    curly_bracket_open = 105
    curly_bracket_close = 106
    separator = 110
    accessor = 111
    
operator_allowed_chars = ['+','-','*','/','%','&','>','<','\\','|','~','!','=']

class Token:
    def __init__(self, type, value, file_name, line, start_column, end_column):
        self.type = type
        self.value = value
        self.file_name = file_name
        self.line = line
        self.start_column = start_column
        self.end_column = end_column
    
    def __str__(self):
        return str(self.type) + " value: \"" + str(self.value) + "\" in " + self.file_name + ":" + str(self.line) + " col:" + str(self.start_column) + "-" + str(self.end_column)


class TokenizerError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason

class FileTokenizer:
    def __init__(self, file_name, file_stream):
        self.file_name = file_name
        self.file_stream = file_stream
        self.current_char = ' '
        self.current_line = 1
        self.current_column = 0

    def next_token(self, previous_token):
        # omit spaces
        while self.current_char == ' ' or self.current_char == '\n':
            if self.current_char == '\n':
                self.current_line += 1
                self.current_column = 0
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
        # check eof
        if self.current_char == None or self.current_char == '':
            return Token(TokenType.eof, None, self.file_name, self.current_line, self.current_column, self.current_column)
        # begin line comment
        if self.current_char == '#':
            word = ''
            start_column = self.current_column
            while self.current_char != '\n' and self.current_char != None and self.current_char != '':
                word += self.current_char
                self.current_char = self.file_stream.read(1)
                self.current_column += 1
            return Token(TokenType.comment, word, self.file_name, self.current_line, start_column, self.current_column)
        # begin scope or atom
        if self.current_char == ':':
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            if self.current_char.isalnum():
                word = ''
                while self.current_char.isalnum():
                    word += self.current_char
                    self.current_char = self.file_stream.read(1)
                    self.current_column += 1
                return Token(TokenType.atom, word, self.file_name, self.current_line, start_column, self.current_column)
            else:
                return Token(TokenType.scope_begin, None, self.file_name, self.current_line, self.current_column, self.current_column)
        # try keyword, identifier or reversed atom
        if self.current_char.isalpha():
            word = ''
            start_column = self.current_column
            while self.current_char.isalnum():
                word += self.current_char
                self.current_char = self.file_stream.read(1)
                self.current_column += 1
                
            if 'defp' in word:
                return Token(TokenType.private_definition, None, self.file_name, self.current_line, start_column, self.current_column)
            elif 'def' in word:
                return Token(TokenType.definition, None, self.file_name, self.current_line, start_column, self.current_column)
            elif 'end' in word:
                return Token(TokenType.scope_end, None, self.file_name, self.current_line, start_column, self.current_column)
            else:
                return Token(TokenType.identifier, word, self.file_name, self.current_line, start_column, self.current_column)
        # try number literal
        if self.current_char.isdigit():
            word = ''
            start_column = self.current_column
            while self.current_char.isdigit():
                word += self.current_char
                self.current_char = self.file_stream.read(1)
                self.current_column += 1
                
            if self.current_char == '.':
                word += self.current_char
                self.current_char = self.file_stream.read(1)
                self.current_column += 1
                while self.current_char.isdigit():
                    word += self.current_char
                    self.current_char = self.file_stream.read(1)
                    self.current_column += 1
                return Token(TokenType.float_literal, word, self.file_name, self.current_line, start_column, self.current_column)
            else:
                return Token(TokenType.integer_literal, word, self.file_name, self.current_line, start_column, self.current_column)
        # try string literal
        if self.current_char == "\"":
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            word = ''
            # TODO: escaping quotes
            while self.current_char != "\"" and self.current_char != '\n' and self.current_char != None and self.current_char != '':
                word += self.current_char
                self.current_char = self.file_stream.read(1)
                self.current_column += 1
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            return Token(TokenType.string_literal, word, self.file_name, self.current_line, start_column, self.current_column)
        # check brackets
        if self.current_char == '(':
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            return Token(TokenType.round_bracket_open, '(', self.file_name, self.current_line, start_column, self.current_column)
        if self.current_char == ')':
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            return Token(TokenType.round_bracket_close, ')', self.file_name, self.current_line, start_column, self.current_column)
        if self.current_char == '[':
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            return Token(TokenType.square_bracket_open, '[', self.file_name, self.current_line, start_column, self.current_column)
        if self.current_char == ']':
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            return Token(TokenType.square_bracket_close, ']', self.file_name, self.current_line, start_column, self.current_column)
        if self.current_char == '{':
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            return Token(TokenType.curly_bracket_open, '{', self.file_name, self.current_line, start_column, self.current_column)
        if self.current_char == '}':
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            return Token(TokenType.curly_bracket_close, '}', self.file_name, self.current_line, start_column, self.current_column)   
        # try separator
        if self.current_char == ',':
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            return Token(TokenType.separator, ',', self.file_name, self.current_line, start_column, self.current_column) 
        # try accessor
        if self.current_char == '.' and previous_token == TokenType.identifier:
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            return Token(TokenType.accessor, '.', self.file_name, self.current_line, start_column, self.current_column) 
        # try operator
        if self.current_char in operator_allowed_chars:
            word = ''
            start_column = self.current_column
            while self.current_char in operator_allowed_chars:
                word += self.current_char
                self.current_char = self.file_stream.read(1) 
                self.current_column += 1   
            return Token(TokenType.operator, word, self.file_name, self.current_line, start_column, self.current_column)
        # error - cannot parse token
        raise TokenizerError("Invalid token: " + self.current_char + " in " + self.file_name + ":" + str(self.current_line) + " col:" + str(self.current_column))

    def tokenize(self):
        tokens = []
        previous_token = None
        while True:
            token = self.next_token(previous_token)
            if not(token) or token.type == TokenType.eof:
                return tokens
            else:
                previous_token = token.type
                tokens.append(token)
        return tokens

if __name__ == "__main__":
    import sys
    file_name = sys.argv[1]
    tokenizer = FileTokenizer(file_name, open(file_name, "r"))
    try:
        tokens = tokenizer.tokenize()
        for t in tokens:
            print(str(t))
    except TokenizerError as e:
        print(str(e))