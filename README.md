# Symbol Table Simulator — Advanced Programming Assignment 3

A **functional-style** Python implementation of a symbol table simulator, demonstrating scoped identifier management, type checking, and semantic error detection — built without loops, global variables, or class declarations.

## Functional Programming Constraints

This implementation strictly follows functional programming rules:
- No `for` / `while` loops — uses **recursion**, `map`, `filter`, `reduce` instead
- No global variables or class declarations
- Each variable assigned **exactly once** (immutable style)
- Only 3 allowed imports: `StaticError`, `Symbol`, `functools`

## Supported Commands

| Command | Format | Description |
|---------|--------|-------------|
| `INSERT` | `INSERT <name> <type>` | Declare identifier (`number`/`string`) in current scope |
| `ASSIGN` | `ASSIGN <name> <value>` | Type-check and assign a value to an identifier |
| `BEGIN` | `BEGIN` | Open a new nested block (like `{` in C++) |
| `END` | `END` | Close the current block (like `}` in C++) |
| `LOOKUP` | `LOOKUP <name>` | Find identifier and return its block level |
| `PRINT` | `PRINT` | Print all visible identifiers (innermost → outermost, forward) |
| `RPRINT` | `RPRINT` | Same as PRINT but in reverse order |

## Errors Raised

| Error | Trigger |
|-------|---------|
| `InvalidInstruction` | Malformed command or unknown keyword |
| `Redeclared` | Same identifier declared twice in the same scope |
| `Undeclared` | Identifier used before declaration |
| `TypeMismatch` | Assigned value type differs from identifier type |
| `UnclosedBlock` | Block opened but never closed (reports level) |
| `UnknownBlock` | `END` without a matching `BEGIN` |

## Project Structure

```
.
├── SymbolTable.py    # Core implementation — simulate(list_of_commands)
├── Symbol.py         # Symbol data class (name, type)
├── StaticError.py    # All error classes
├── TestSuite.py      # 50+ test cases
├── TestUtils.py      # Test runner utilities
└── main.py           # Entry point with colored output
```

## Run

```bash
# Run all tests
python3 main.py

# Run a specific test
python3 main.py test_1
```

## Course

**CO2039 — Advanced Programming** — Ho Chi Minh City University of Technology (HCMUT), Semester 242
