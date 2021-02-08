from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
import subprocess


class Operator(ABC):

    @abstractmethod
    def execute(self, *params: List[str]) -> List[str]:
        pass


class UnaryOperator(Operator):

    def __init__(self, command: str, *flags: List[str]):
        self.command = command
        self.flags = flags

    def execute(self, *params: List[Tuple[str, str]]) -> List[str]:
        if len(params) != 1:
            raise TypeError("Unary operators must take only 1 argument")
        cmd_str = [f"{self.command} {' '.join([y for x in params for y in x if y is not None])}"]
        if len(self.flags) != 0:
            cmd_str[0] += f" {' '.join(self.flags)}"
        return cmd_str
        

class BinaryOperator(Operator):

    def __init__(self, command: str, *flags: List[str]):
        self.command = command
        self.flags = flags

    def execute(self, *params: List[Tuple[str, str]]) -> List[str]:
        if len(params) != 2:
            raise TypeError("Binary operators must take only 2 arguments")
        cmd_str = [f"{self.command} {' '.join([y for x in params for y in x if y is not None])}"]
        if len(self.flags) != 0:
            cmd_str[0] += f" {' '.join(self.flags)}"
        return cmd_str


class TorrentClient:

    def __init__(self, command_name: str, operators: Dict[str, Operator]) -> None:
        self.command_name = command_name
        self.__operators = operators

    def get(self, name: str) -> Operator:
        op = self.__operators.get(name)
        if op is None:
            raise TypeError(f"Operator \"{name}\" is not supported by {self.command_name}")
        return op

    def execute(self, command: str, *args: List[Tuple[str, str]]) -> bool:
        op = self.get(command)
        if isinstance(op, UnaryOperator) and len(args) != 1:
            raise TypeError(f"Unary operator \"{op.command}\" given != 1 args")
        if isinstance(op, BinaryOperator) and len(args) != 2:
            raise TypeError(f"Binary operator \"{op.command}\" given != 2 args")
        execute = op.execute(*args)
        print([self.command_name] + execute)
        subprocess.run([self.command_name] + execute)
