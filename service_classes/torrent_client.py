from abc import ABC, abstractmethod
from typing import Callable, List, Dict, Any


# TODO: redo this file


class TorrentClient:

    @abstractmethod
    def execute(self, command: str, *args: str):
        pass


class Operator(ABC):

    @abstractmethod
    def execute(self, *params: str):
        pass


class UnaryOperator(Operator):

    def __init__(self, func: Callable[[Any, Any], None]):
        self.func = func

    def execute(self, *params: str):
        if len(params) != 1:
            raise TypeError("Unary operators must take only 2 arguments")
        return self.func(*params)


class BinaryOperator(Operator):

    def __init__(self, func: Callable[[Any, Any], None]):
        self.func = func

    def execute(self, *params: str):
        if len(params) != 2:
            raise TypeError("Binary operators must take only 2 arguments")
        return self.func(*params)


# class ShellProgram:
#
#     def __init__(self, command_name: str, params: List[str], operators: Dict[str, Operator], error_strings: List[str], success_strings: List[str]) -> None:
#         self.command_name = command_name
#         self.params = params
#         self.__operators = operators
#         self.__error_strings = error_strings
#         self.__success_strings = success_strings
#
#     def get(self, name: str) -> Operator:
#         op = self.__operators.get(name)
#         if op is None:
#             raise TypeError(f"Operator \"{name}\" is not supported by {self.command_name}")
#         return op
#
#     def execute(self, command: str, *args: str) -> bool:
#         op = self.get(command)
#         if isinstance(op, UnaryOperator) and len(args) != 1:
#             raise TypeError(f"Unary operator \"{command}\" given {len(args)} args")
#         if isinstance(op, BinaryOperator) and len(args) != 2:
#             raise TypeError(f"Binary operator \"{command}\" given {len(args)} args")
#         execute = op.execute(*args)
#         try:
#             print([self.command_name] + self.params + execute)
#             proc = subprocess.run([self.command_name] + self.params + execute, capture_output=True)
#         except FileNotFoundError:
#             logging.error(f"{self.command_name} was not found on the system. Make sure it is installed.")
#             return False
#         logging.error(proc.stderr)
#         logging.error(proc.stdout)
#         if any(x in str(proc.stderr + proc.stdout) for x in self.__error_strings):
#             return False
#         if any(x in str(proc.stderr + proc.stdout) for x in self.__success_strings):
#             return True
#         return False


class PythonFunctions(TorrentClient):

    def __init__(self, operators: Dict[str, Operator]):
        self.__operators = operators

    def get(self, name: str) -> Operator:
        op = self.__operators.get(name)
        if op is None:
            raise TypeError(f"Operator \"{name}\" is not supported")
        return op

    def execute(self, command: str, *args: str):
        return self.get(command).execute(*args)
