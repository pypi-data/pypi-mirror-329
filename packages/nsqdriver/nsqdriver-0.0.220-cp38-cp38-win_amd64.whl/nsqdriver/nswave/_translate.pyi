import numpy as np

__all__ = ['NormalTranslator', 'PlayDDRTranslator']

class NormalTranslator:
    def get_envelope(self, ir_list): ...
    def translate_ir(self, ir_list: list) -> tuple[np.ndarray, str]: ...

class PlayDDRTranslator(NormalTranslator):
    @staticmethod
    def get_arb(ir_list): ...
    def translate_ir(self, ir_list: list) -> tuple[list[str], str]: ...
