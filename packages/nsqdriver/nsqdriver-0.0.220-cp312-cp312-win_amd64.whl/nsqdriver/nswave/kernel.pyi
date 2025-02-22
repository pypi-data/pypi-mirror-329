from ._functions import *
from ._rules import *
from ._checkers import *
from ._optimizations import *
from ._translate import *
import ast
from ._ir import IRBase
from _typeshed import Incomplete

__all__ = ['kernel', 'Kernel']

class KernelParseError(Exception): ...

class NSQCKernel(type):
    def __init__(cls, name, bases, attrs) -> None: ...

class Kernel(ast.NodeVisitor, metaclass=NSQCKernel):
    max_frame: int
    name: Incomplete
    func_args: Incomplete
    func_kwargs: Incomplete
    top_src: Incomplete
    top_node: Incomplete
    var_symbol: Incomplete
    frame_symbol: Incomplete
    frame_idx: int
    envelope_symbol: Incomplete
    register_symbol: Incomplete
    register_idx: int
    instruction_list: Incomplete
    jail_tag: Incomplete
    compile_params: Incomplete
    pass_params: Incomplete
    def __init__(self, func: Incomplete | None = None, args: Incomplete | None = None, kwargs: Incomplete | None = None) -> None: ...
    def clear(self) -> None: ...
    def parse(self): ...
    def show(self) -> None: ...
    def __call__(self, *args, **kwargs): ...
    def visit_arg(self, node: ast.arg): ...
    def visit_Assign(self, node: ast.Assign): ...
    def visit_AugAssign(self, node: ast.AugAssign): ...
    def visit_AnnAssign(self, node: ast.AnnAssign): ...
    def visit_Call(self, node: ast.Call) -> object: ...
    def visit_BinOp(self, node: ast.BinOp): ...
    def visit_Constant(self, node): ...
    def visit_Expr(self, node: ast.Expr): ...
    def visit_Compare(self, node: ast.Compare): ...
    def visit_If(self, node: ast.If): ...
    def visit_For(self, node: ast.For): ...
    def visit_Return(self, node) -> None: ...
    def visit_FunctionDef(self, node: ast.FunctionDef): ...
    def visit_arguments(self, node: ast.arguments): ...
    def visit_Module(self, node: ast.Module): ...
    def with_error(self, error: list): ...
    def node_line(self, error_ir: IRBase): ...

def kernel(func): ...
