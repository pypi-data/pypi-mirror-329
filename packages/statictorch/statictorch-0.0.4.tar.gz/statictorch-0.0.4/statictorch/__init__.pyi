# Generated with statictorch/generator/generator.py
import typing as _typing
import torch as _torch


TensorAny: _typing.TypeAlias = _torch.Tensor


def anify(object: _typing.Any) -> _typing.Any:
    return object


class TensorDimensionDescriptor:
    def __init__(self):
        raise RuntimeError('TensorDimensionDescriptor only exists for type annotation and should not be initialized.')


class Tensor0d(_torch.Tensor):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor0d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor0d.__init__ only exists for type annotation and should not be called in runtime.')


_T1 = _typing.TypeVar('_T1', bound=TensorDimensionDescriptor)
class Tensor1d(_torch.Tensor, _typing.Generic[_T1]):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor1d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor1d.__init__ only exists for type annotation and should not be called in runtime.')


_T2 = _typing.TypeVar('_T2', bound=TensorDimensionDescriptor)
class Tensor2d(_torch.Tensor, _typing.Generic[_T1, _T2]):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor2d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor2d.__init__ only exists for type annotation and should not be called in runtime.')


_T3 = _typing.TypeVar('_T3', bound=TensorDimensionDescriptor)
class Tensor3d(_torch.Tensor, _typing.Generic[_T1, _T2, _T3]):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor3d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor3d.__init__ only exists for type annotation and should not be called in runtime.')


_T4 = _typing.TypeVar('_T4', bound=TensorDimensionDescriptor)
class Tensor4d(_torch.Tensor, _typing.Generic[_T1, _T2, _T3, _T4]):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor4d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor4d.__init__ only exists for type annotation and should not be called in runtime.')


_T5 = _typing.TypeVar('_T5', bound=TensorDimensionDescriptor)
class Tensor5d(_torch.Tensor, _typing.Generic[_T1, _T2, _T3, _T4, _T5]):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor5d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor5d.__init__ only exists for type annotation and should not be called in runtime.')


_T6 = _typing.TypeVar('_T6', bound=TensorDimensionDescriptor)
class Tensor6d(_torch.Tensor, _typing.Generic[_T1, _T2, _T3, _T4, _T5, _T6]):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor6d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor6d.__init__ only exists for type annotation and should not be called in runtime.')


_T7 = _typing.TypeVar('_T7', bound=TensorDimensionDescriptor)
class Tensor7d(_torch.Tensor, _typing.Generic[_T1, _T2, _T3, _T4, _T5, _T6, _T7]):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor7d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor7d.__init__ only exists for type annotation and should not be called in runtime.')


_T8 = _typing.TypeVar('_T8', bound=TensorDimensionDescriptor)
class Tensor8d(_torch.Tensor, _typing.Generic[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor8d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor8d.__init__ only exists for type annotation and should not be called in runtime.')


_T9 = _typing.TypeVar('_T9', bound=TensorDimensionDescriptor)
class Tensor9d(_torch.Tensor, _typing.Generic[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8, _T9]):
    def __new__(cls, tensor: _torch.Tensor) -> 'Tensor9d':
        return tensor  # type: ignore

    def __init__(self, tensor: _torch.Tensor):
        super().__init__()
        raise RuntimeError('Tensor9d.__init__ only exists for type annotation and should not be called in runtime.')