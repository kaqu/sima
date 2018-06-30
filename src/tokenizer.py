#!/usr/bin/python

from enum import Enum

class TokenType(Enum):
    # extra
    eof = -1
    comment = 0
    # literals
    atom_literal = 100
    declaration_literal = 101
    string_literal = 102
    integer_literal = 103
    float_literal = 104
    # operators and specials
    operator = 200
    separator = 201
    accessor = 202
    # applicator = 303
    # compositor = 304
    function_return = 300 
    function_arrow = 301
    # definition
    definition = 400
    # module_definition = 301
    # function_definition = 302
    # structure_definition = 303
    # enum_definition = 304
    # type_definition = 305
    definition_end = 401
    # scope
    newline = 402
    # identifiers
    identifier = 500
    # brackets
    round_bracket_open = 601
    round_bracket_close = 602
    square_bracket_open = 603
    square_bracket_close = 604
    curly_bracket_open = 605
    curly_bracket_close = 606
     
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

    def next_token(self):
        # check eof
        if self.current_char == None or self.current_char == '':
            return Token(TokenType.eof, None, self.file_name, self.current_line, self.current_column, self.current_column)

        # omit spaces
        while self.current_char == ' ' or self.current_char == '\t':
            self.current_char = self.file_stream.read(1)
            self.current_column += 1

        # merge newlines
        if self.current_char == '\n':
            line_break_line = self.current_line
            line_break_column = self.current_column
            while self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\n':
                if self.current_char == '\n':
                    self.current_line += 1
                    self.current_column = 0
                self.current_char = self.file_stream.read(1)
                self.current_column += 1
            return Token(TokenType.newline, None, self.file_name, line_break_line, line_break_column, line_break_column)
        
        # begin line comment
        if self.current_char == '#':
            word = ''
            start_column = self.current_column
            while self.current_char != '\n' and self.current_char != None and self.current_char != '':
                word += self.current_char
                self.current_char = self.file_stream.read(1)
                self.current_column += 1
            return Token(TokenType.comment, word, self.file_name, self.current_line, start_column, self.current_column)

        # atom_literal
        if self.current_char == ':':
            word = self.current_char
            start_column = self.current_column
            self.current_char = self.file_stream.read(1)
            self.current_column += 1
            if self.current_char.isalnum():
                while self.current_char.isalnum() or self.current_char == '_':
                    word += self.current_char
                    self.current_char = self.file_stream.read(1)
                    self.current_column += 1
                # space after is required
                if self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\n':
                    return Token(TokenType.atom_literal, word, self.file_name, self.current_line, start_column, self.current_column)
                else:
                    raise TokenizerError("Invalid token: " + self.current_char + " in " + self.file_name + ":" + str(self.current_line) + " col:" + str(self.current_column))
            else:
                raise TokenizerError("Invalid token: " + self.current_char + " in " + self.file_name + ":" + str(self.current_line) + " col:" + str(self.current_column))
        
        # try definition, declaration, identifier
        if self.current_char.isalpha():
            word = ''
            start_column = self.current_column
            while self.current_char.isalnum() or self.current_char == '_':
                word += self.current_char
                self.current_char = self.file_stream.read(1)
                self.current_column += 1
                
            if word == 'def':
                # space after is required
                if self.current_char == ' ':
                    return Token(TokenType.definition, None, self.file_name, self.current_line, start_column, self.current_column)
                else:
                    raise TokenizerError("Invalid token: " + self.current_char + " in " + self.file_name + ":" + str(self.current_line) + " col:" + str(self.current_column))
            elif word == 'ret':
                # space after is required
                if self.current_char == ' ' or self.current_char == '\n':
                    return Token(TokenType.function_return, None, self.file_name, self.current_line, start_column, self.current_column)
                else:
                    raise TokenizerError("Invalid token: " + self.current_char + " in " + self.file_name + ":" + str(self.current_line) + " col:" + str(self.current_column))
            elif word == 'end':
                # space after is required
                if self.current_char == ' ' or self.current_char == '\n' or self.current_char == '':
                    return Token(TokenType.definition_end, None, self.file_name, self.current_line, start_column, self.current_column)
                else:
                    raise TokenizerError("Invalid token: " + self.current_char + " in " + self.file_name + ":" + str(self.current_line) + " col:" + str(self.current_column))
            elif word == 'defmodule':
                # space after is required
                if self.current_char == ' ' or self.current_char == '\n':
                    return Token(TokenType.definition, "module", self.file_name, self.current_line, start_column, self.current_column)
                else:
                    raise TokenizerError("Invalid token: " + self.current_char + " in " + self.file_name + ":" + str(self.current_line) + " col:" + str(self.current_column))
            elif self.current_char == ':':
                word += self.current_char
                end_column = self.current_column
                self.current_char = self.file_stream.read(1)
                self.current_column += 1
                # space after is required
                if self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\n':
                    return Token(TokenType.declaration_literal, word, self.file_name, self.current_line, start_column, end_column)
                else:
                    raise TokenizerError("Invalid token: " + self.current_char + " in " + self.file_name + ":" + str(self.current_line) + " col:" + str(self.current_column))
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
        if self.current_char == '.':
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
            if word == '->':
                return Token(TokenType.function_arrow, word, self.file_name, self.current_line, start_column, self.current_column)
            else:
                return Token(TokenType.operator, word, self.file_name, self.current_line, start_column, self.current_column)
        # error - cannot parse token
        raise TokenizerError("Invalid token: " + self.current_char + " in " + self.file_name + ":" + str(self.current_line) + " col:" + str(self.current_column))

    def tokenize(self):
        tokens = []
        while True:
            token = self.next_token()
            if not(token) or token.type == TokenType.eof:
                return tokens
            else:
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