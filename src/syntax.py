from enum import Enum

class SyntaxError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason

class RootNode:

    def __init__(self, content):
        self.content = content
    
    def __str__(self):
        return "{\n\tRootNode Content: [\n" + "\n".join(str(p) for p in self.content) + "\n]\n}"

class AtomLiteralNode:

    def __init__(self, identifier):
        self.identifier = identifier
    
    def __str__(self):
        return "{\n\tAtomLiteralNode Identifier: " + str(self.identifier) + "\n}"

class IntegerLiteralNode:

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "{\n\tIntegerLiteralNode Value: " + str(self.value) + "\n}"


class FloatLiteralNode:

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "{\n\tFloatLiteralNode Value: " + str(self.value) + "\n}"

class StringLiteralNode:

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "{\n\tStringLiteralNode Value: " + str(self.value) + "\n}"

class StructFieldNode:
    def __init__(self, field_identifier, field_type):
            self.field_identifier = field_identifier
            self.field_type = field_type

    def __str__(self):
        return "{\n\tStructFieldNode Identifier: " + str(self.field_identifier) + " Type: " + str(self.field_type) + "\n}"

class StructTypeNode:
    def __init__(self, identifier, fields):
            self.identifier = identifier
            self.fields = fields

    def __str__(self):
        return "{\n\tStructTypeNode Identifier: " + str(self.identifier) + " Fields: [\n" + "\n".join(str(p) for p in self.fields) + "\n]\n}"

class FunctionTypeNode:
    def __init__(self, identifier, argument_type, return_type):
            self.identifier = identifier
            self.argument_type = argument_type
            self.return_type = return_type

    def __str__(self):
        return "{\n\tFunctionTypeNode Identifier: " + str(self.identifier) + " Signature: " + str(self.argument_type) + "->" + str(self.return_type) + "\n}"

class TypeIdentifierNode:
    def __init__(self, identifier, resolved_type):
            self.identifier = identifier
            self.resolved_type = resolved_type

    def __str__(self):
        return "{\n\tTypeIdentifierNode Identifier: " + str(self.identifier) + " Signature: " + str(self.resolved_type) + "\n}"

class DefinitionEndNode:
    def __str__(self):
        return "{\n\tDefinitionEndNode\n}"

class ModuleDefinitionNode:
    def __init__(self, identifier, body):
            self.identifier = identifier
            self.body = body

    def __str__(self):
        return "{\n\tModuleDefinitionNode Identifier: " + str(self.identifier) + " Body: [\n" + "\n".join(str(p) for p in self.body) + "\n]\n}"

class FunctionDefinitionNode:
    def __init__(self, identifier, function_type, body):
            self.identifier = identifier
            self.function_type = function_type
            self.body = body

    def __str__(self):
        return "{\n\tFunctionDefinitionNode Identifier: " + str(self.identifier) + " Type : " + str(self.function_type) + " Body: [\n" + "\n".join(str(p) for p in self.body) + "\n]\n}"

class FunctionReturnNode:
    def __init__(self, return_value):
            self.return_value = return_value

    def __str__(self):
        return "{\n\tFunctionReturnNode return value: " + str(self.return_value) + "\n}"