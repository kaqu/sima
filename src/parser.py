from src.tokenizer import *
from src.syntax import *

class TokenParser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = -1

    def parse_tokens(self):
        nodes = []
        while self.current_index < len(self.tokens):
            try:
                nodes.append(self.parse_next())
            except SyntaxError as syntax_error:
                print(str(syntax_error))
                raise syntax_error
            except:
                break

        return RootNode(nodes)
    
    def ignore_comments(self):
        while self.current_index < len(self.tokens) and self.tokens[self.current_index].type == TokenType.comment:
            self.current_index += 1
            print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))

    def parse_next(self):
        self.current_index += 1
        print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
        self.ignore_comments()
        if self.current_index >= len(self.tokens):
            raise Exception()
        token = self.tokens[self.current_index]
        if token.type == TokenType.atom_literal:
            return AtomLiteralNode(token.value)
        elif token.type == TokenType.integer_literal:
            return IntegerLiteralNode(token.value)
        elif token.type == TokenType.float_literal:
            return FloatLiteralNode(token.value)
        elif token.type == TokenType.string_literal:
            return StringLiteralNode(token.value)
        elif token.type == TokenType.definition_end:
            return DefinitionEndNode()
        elif token.type == TokenType.definition:
            return self.parse_definition(token.value)
        elif token.type == TokenType.function_return:
            return FunctionReturnNode(self.parse_next())
        else:
            return self.parse_next()
            # raise SyntaxError("Invalid token " + str(self.tokens[self.current_index].type) + " in " + self.tokens[self.current_index].file_name + ":" + str(self.tokens[self.current_index].line))

    def parse_definition(self, definition_type):
        self.current_index += 1
        print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
        declaration_token = self.tokens[self.current_index]
        print("declaration: " + declaration_token.value)
        if declaration_token.type == TokenType.declaration_literal:
            if self.tokens[self.current_index + 1].type == TokenType.identifier or self.tokens[self.current_index + 1].type == TokenType.curly_bracket_open:
                function_type = self.parse_type()
                self.current_index += 1
                print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
                self.ignore_comments()
                if self.tokens[self.current_index].type == TokenType.newline:
                    self.current_index += 1
                    print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
                    self.ignore_comments()
                    body = []
                    while self.tokens[self.current_index].type != TokenType.definition_end:
                        body.append(self.parse_next())
                    return FunctionDefinitionNode(declaration_token.value, function_type, body)
                else:
                    raise SyntaxError("Invalid definition in " + self.tokens[self.current_index].file_name + ":" + str(self.tokens[self.current_index].line))
            else:
                self.current_index += 1
                print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
                self.ignore_comments()
                if self.tokens[self.current_index].type == TokenType.newline:
                    # self.current_index += 1
                    # print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
                    # self.ignore_comments()
                    if definition_type == "module":
                        print("parsing module body")
                        body = []
                        while self.tokens[self.current_index].type != TokenType.definition_end:
                            print("parsing module body next")
                            body.append(self.parse_next())
                            print("parsing module body state: " + str(body))
                        print("parsing module body end")
                        return ModuleDefinitionNode(declaration_token.value, body)
                    else:
                        raise SyntaxError("Definition of type not supported yet..." + self.tokens[self.current_index].file_name + ":" + str(self.tokens[self.current_index].line))
                else:
                    raise SyntaxError("Invalid definition in " + self.tokens[self.current_index].file_name + ":" + str(self.tokens[self.current_index].line))
        else:
            raise SyntaxError("Invalid definition in " + self.tokens[self.current_index].file_name + ":" + str(self.tokens[self.current_index].line))
   
    def parse_type(self):
        self.current_index += 1
        print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
        token = self.tokens[self.current_index]
        if token.type == TokenType.identifier:
            if self.tokens[self.current_index + 1].type == TokenType.function_arrow:
                self.current_index += 1
                print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
                return_type = self.parse_type()
                return FunctionTypeNode(None, TypeIdentifierNode(token.value, None), return_type)
            else:
                return TypeIdentifierNode(token.value, None)
        elif token.type == TokenType.curly_bracket_open:
            fields = []
            self.current_index += 1
            print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
            while self.tokens[self.current_index].type != TokenType.curly_bracket_close:
                field_identifier_token = self.tokens[self.current_index]
                if field_identifier_token.type == TokenType.declaration_literal:
                    field_type = self.parse_type()
                    fields.append(StructFieldNode(field_identifier_token.value, field_type))
                else:
                    raise SyntaxError("Field declaration expected " + self.tokens[self.current_index].file_name + ":" + str(self.tokens[self.current_index].line))
            if self.tokens[self.current_index + 1].type == TokenType.function_arrow:
                self.current_index += 1
                print("Next index [" + str(self.current_index) + "]: " + str(self.tokens[self.current_index]))
                return_type = self.parse_type()
                return FunctionTypeNode(None, StructTypeNode(None, fields), return_type)
            else:
                StructTypeNode(None, fields)
        else:
            raise SyntaxError("Type declaration expected " + self.tokens[self.current_index].file_name + ":" + str(self.tokens[self.current_index].line))
