from typing import Dict, List

from .call_stack import InstructionPointer


class VariableChangeHistoryEntry:
    def __init__(self, instruction_pointer: InstructionPointer, value: any):
        self.instruction_pointer = instruction_pointer
        self.value = value


class Variable:
    def __init__(self, name: str, value: any):
        self.name = name
        self.value = value
        self.change_history: List[VariableChangeHistoryEntry] = []

    def update(self, new_value: any, instruction_pointer: InstructionPointer):
        self.change_history.append(
            VariableChangeHistoryEntry(instruction_pointer, new_value)
        )
        self.value = new_value


class Variables:
    def __init__(self):
        self.variables: Dict[str, Variable] = {}

    def __getitem__(self, name: str) -> Variable:
        return self.variables.get(name, None)

    def __setitem__(
        self,
        name: str,
        value: any,
        instruction_pointer: InstructionPointer = None,
    ):
        if name not in self.variables:
            self.variables[name] = Variable(name, value)
        self.variables[name].update(value, instruction_pointer)

    def __iter__(self):
        return iter(self.variables.values())

    def __len__(self):
        return len(self.variables)

    def to_dict(self):
        return {name: variable.value for name, variable in self.variables.items()}
