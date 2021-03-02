from abc import ABC, abstractmethod
import logging
from typing import List, Dict, Tuple
import subprocess


class Operator(ABC):

    @abstractmethod
    def execute(self, *params: List[str]) -> List[str]:
        pass


class UnaryOperator(Operator):

    def __init__(self, command: str, *flags: List[str], arg_flag: str):
        self.command = command
        self.flags = flags
        self.arg_flag = arg_flag

    def execute(self, *params: List[str]) -> List[str]:
        if len(params) != 1:
            raise TypeError("Unary operators must take only 1 argument")
        arg_str = (self.arg_flag + " " if len(self.arg_flag) > 0 else "") + params[0]
        cmd_str = [f"{self.command} {arg_str}"]
        if len(self.flags) != 0:
            cmd_str[0] += f" {' '.join(self.flags)}"
        return cmd_str
        

class BinaryOperator(Operator):

    def __init__(self, command: str, *flags: List[str], arg1_flag: str = "", arg2_flag: str = ""):
        self.command = command
        self.flags = flags
        self.arg1_flag = arg1_flag
        self.arg2_flag = arg2_flag

    def execute(self, *params: List[str]) -> List[str]:
        if len(params) != 2:
            raise TypeError("Binary operators must take only 2 arguments")
        arg1_str = (self.arg1_flag + " " if len(self.arg1_flag) > 0 else "") + params[0]
        arg2_str = (self.arg2_flag + " " if len(self.arg1_flag) > 0 else "") + params[1]
        cmd_str = [f"{self.command} {arg1_str} {arg2_str}"]
        if len(self.flags) != 0:
            cmd_str[0] += f" {' '.join(self.flags)}"
        return cmd_str


class TorrentClient:
    LINUX_ERRORS = ["No such file or directory"]

    def __init__(self, command_name: str, operators: Dict[str, Operator], error_strings: List[str], success_strings: List[str]) -> None:
        self.command_name = command_name
        self.__operators = operators
        self.__error_strings = error_strings
        self.__success_strings = success_strings

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
        proc = subprocess.run([self.command_name] + execute, capture_output=True)
        if any(x in str(proc.stderr + proc.stdout) for x in self.LINUX_ERRORS):
            logging.error(proc.stderr.split("\n")[-1])
            return False
        if any(x in str(proc.stderr + proc.stdout) for x in self.__error_strings):
            return False
        if any(x in str(proc.stderr + proc.stdout) for x in self.__success_strings):
            return True
        return False
