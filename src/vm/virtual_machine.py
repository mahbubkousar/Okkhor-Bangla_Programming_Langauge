# src/vm/virtual_machine.py

class VirtualMachine:
    def __init__(self):
        self.stack = []  # Stack for computation
        self.instructions = []  # Bytecode instructions
        self.ip = 0  # Instruction pointer
        self.variables = {}  # Variable storage

    def load_bytecode(self, bytecode):
        """Load bytecode instructions."""
        self.instructions = bytecode

    def execute(self):
        """Execute the loaded bytecode."""
        while self.ip < len(self.instructions):
            opcode, *args = self.instructions[self.ip]
            self.dispatch(opcode, *args)
            self.ip += 1

    def dispatch(self, opcode, *args):
        """Dispatch the opcode to the appropriate handler."""
        if opcode == "PUSH":
            self.stack.append(args[0])
        elif opcode == "POP":
            self.stack.pop()
        elif opcode == "ADD":
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)
        elif opcode == "SUB":
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)
        elif opcode == "STORE":
            self.variables[args[0]] = self.stack.pop()
        elif opcode == "LOAD":
            self.stack.append(self.variables[args[0]])
        elif opcode == "JUMP_IF_ZERO":
            if self.stack.pop() == 0:
                self.ip = args[0] - 1
        elif opcode == "JUMP":
            self.ip = args[0] - 1
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

# Example usage in main.py
if __name__ == "__main__":
    vm = VirtualMachine()
    bytecode = [
        ("PUSH", 10),
        ("PUSH", 20),
        ("ADD",),
        ("STORE", "result"),
        ("LOAD", "result"),
        ("PUSH", 0),
        ("JUMP_IF_ZERO", 10),  # This jump is skipped since 0 is not at the top of the stack
    ]
    vm.load_bytecode(bytecode)
    vm.execute()
    print("Stack:", vm.stack)
    print("Variables:", vm.variables)
