from StaticError import *
from Symbol import *
from functools import reduce

def simulate(list_of_commands):
    """
    Executes a list of commands and processes them sequentially.
    
    Args:
        list_of_commands (list[str]): A list of commands to be executed.
    
    Returns:
        list[str]: A list of return messages corresponding to each command.
    """
    def split_command(command, i=0, parts=None, current_part="", in_quotes=False):
        """
        Recursively splits a command string while preserving quoted sections.
        """
        parts_final = parts if parts is not None else []
        if i >= len(command):
            return parts_final + ([current_part] if current_part or parts_final else [])
        char = command[i]
        if char == "'":
            return split_command(command, i + 1, parts, current_part + char, not in_quotes)
        if char.isspace() and not in_quotes:
            return split_command(command, i + 1, parts_final + [current_part], "", in_quotes)
        return split_command(command, i + 1, parts, current_part + char, in_quotes)

    def find_symbol(symbol, identifier_name):
        """
        Recursively finds a symbol in the symbol table.
        """
        matches = [(sym, len(symbol) - 1 - level) 
                  for level, scope in enumerate(reversed(symbol))
                  for sym in scope 
                  if sym.name == identifier_name]
        return matches[0] if matches else (None, -1)

    def process_commands(commands, symbol, result):
        """
        Recursively processes commands without loops or reassignments.
        """
        if not commands:
            if len(symbol) > 1:
                raise UnclosedBlock(len(symbol) - 1)
            return result

        command = commands[0]
        parts = split_command(command)
        if not parts:
            raise InvalidInstruction("Invalid command")

        # Check the first token for valid commands
        valid_commands = {"INSERT", "ASSIGN", "BEGIN", "END", "LOOKUP", "PRINT", "RPRINT"}
        if not parts[0] in valid_commands:
            raise InvalidInstruction("Invalid command")

        # Validate that the command has no leading or trailing spaces
        expected_command = " ".join([part for part in parts if part])  # Remove empty tokens for comparison
        if command != expected_command and command != " ".join(parts):
            raise InvalidInstruction("Invalid command")

        # Helper functions with immutable variables
        is_number_constant = lambda value: value.isdigit()
        is_string_constant = lambda value: value.startswith("'") and value.endswith("'") and all(c.isalnum() for c in value[1:-1])
        is_valid_identifier = lambda value: len(value) > 0 and value[0].islower() and all(c.isalnum() or c == '_' for c in value)

        def get_value_type(value, identifier_name_target):
            if is_number_constant(value):
                return "number"
            if is_string_constant(value):
                return "string"
            sym, _ = find_symbol(symbol, value)
            if sym is None:
                raise Undeclared(f"ASSIGN {identifier_name_target} {value}")
            return sym.typ

        # Process each command type with unique variable names to avoid reassignment
        if parts[0] == "INSERT":
            if len(parts) != 3:
                raise InvalidInstruction(command)
            
            identifier_name_insert = parts[1]
            identifier_type_insert = parts[2]
            expected_command_insert = f"INSERT {identifier_name_insert} {identifier_type_insert}"
            
            if not identifier_name_insert or \
               not (identifier_name_insert[0].islower() and all(c.isalnum() or c == '_' for c in identifier_name_insert)) or \
               identifier_type_insert not in ["number", "string"]:
                raise InvalidInstruction(command)
            
            current_scope = symbol[-1]
            if any(sym.name == identifier_name_insert for sym in current_scope):
                raise Redeclared(command)
            
            new_symbol = Symbol(identifier_name_insert, identifier_type_insert)
            symbol_insert = symbol[:-1] + [current_scope + [new_symbol]]
            result_insert = result + ["success"]
            return process_commands(commands[1:], symbol_insert, result_insert)

        elif parts[0] == "ASSIGN":
            if len(parts) != 3:
                raise InvalidInstruction(command)
            
            identifier_name_assign = parts[1]
            value = parts[2]
            expected_command_assign = f"ASSIGN {identifier_name_assign} {value}"
            
            if not identifier_name_assign or \
               not (identifier_name_assign[0].islower() and all(c.isalnum() or c == '_' for c in identifier_name_assign)) or \
               not (is_number_constant(value) or is_string_constant(value) or is_valid_identifier(value)):
                raise InvalidInstruction(command)
            
            target_symbol, _ = find_symbol(symbol, identifier_name_assign)
            if target_symbol is None:
                raise Undeclared(command)
            
            value_type = get_value_type(value, identifier_name_assign)
            if value_type != target_symbol.typ:
                raise TypeMismatch(command)
            
            result_assign = result + ["success"]
            return process_commands(commands[1:], symbol, result_assign)

        elif parts[0] == "BEGIN":
            if len(parts) != 1:
                raise InvalidInstruction(command)
            symbol_begin = symbol + [[]]
            return process_commands(commands[1:], symbol_begin, result)

        elif parts[0] == "END":
            if len(parts) != 1:
                raise InvalidInstruction(command)
            if len(symbol) <= 1:
                raise UnknownBlock()
            symbol_end = symbol[:-1]
            return process_commands(commands[1:], symbol_end, result)

        elif parts[0] == "LOOKUP":
            if len(parts) != 2:
                raise InvalidInstruction(command)
            
            identifier_name_lookup = parts[1]
            expected_command_lookup = f"LOOKUP {identifier_name_lookup}"
            
            if not identifier_name_lookup or \
               not (identifier_name_lookup[0].islower() and all(c.isalnum() or c == '_' for c in identifier_name_lookup)):
                raise InvalidInstruction(command)
            
            sym, level = find_symbol(symbol, identifier_name_lookup)
            if sym is None:
                raise Undeclared(command)
            
            result_lookup = result + [str(level)]
            return process_commands(commands[1:], symbol, result_lookup)

        elif parts[0] in ["RPRINT", "PRINT"]:
            if len(parts) != 1:
                raise InvalidInstruction(command)
            identifiers_with_level = [
                (sym.name, len(symbol) - 1 - level)
                for level, scope in enumerate(reversed(symbol))
                for sym in reversed(scope)
            ]
            
            unique_identifiers = reduce(
                lambda acc, item: acc + [item] if item[0] not in [x[0] for x in acc] else acc,
                identifiers_with_level,
                []
            )
            
            formatted_identifiers_print = [f"{name}//{level}" for name, level in unique_identifiers]
            final_identifiers = formatted_identifiers_print if parts[0] == "RPRINT" else formatted_identifiers_print[::-1]
            
            result_print = result + [" ".join(final_identifiers) if final_identifiers else ""]
            return process_commands(commands[1:], symbol, result_print)

        else:
            raise InvalidInstruction("Invalid command")

    return process_commands(list_of_commands, [[]], [])