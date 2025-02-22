from ._ir import *
from _typeshed import Incomplete

__all__ = ['BaseChecker', 'OverlapChecker', 'EnvelopeChecker', 'TwoCapiChecker', 'SequenceChecker', 'PlyChecker', 'DrstChecker', 'CapiChecker', 'FmsiChecker', 'IRNumberChecker']

class BaseChecker:
    warnings_instruction: Incomplete
    error_instruction: Incomplete
    IR_list: Incomplete
    def __init__(self) -> None: ...
    def check_ir(self, IR_list) -> list: ...

class OverlapChecker(BaseChecker):
    def __init__(self) -> None: ...
    def check_ir(self, ir_list: list): ...

class SequenceChecker(BaseChecker):
    def __init__(self) -> None: ...
    def check_ir(self, ir_list) -> list: ...

class EnvelopeChecker(BaseChecker):
    def __init__(self) -> None: ...
    def check_ir(self, ir_list): ...

class PlyChecker(BaseChecker):
    def __init__(self) -> None: ...
    def check_ir(self, ir_list): ...

class DrstChecker(BaseChecker):
    def __init__(self) -> None: ...
    def check_ir(self, ir_list): ...

class CapiChecker(BaseChecker):
    def __init__(self) -> None: ...
    def check_ir(self, ir_list): ...

class FmsiChecker(BaseChecker):
    def __init__(self) -> None: ...
    def check_ir(self, ir_list): ...

class IRNumberChecker(BaseChecker):
    def __init__(self) -> None: ...
    def check_ir(self, ir_list): ...

class TwoCapiChecker(BaseChecker):
    def __init__(self) -> None: ...
    def check_ir(self, ir_list): ...
