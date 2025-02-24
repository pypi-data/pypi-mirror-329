import typing as t
import torch


def tensor(
    tensor, valid_func: t.Optional[t.Callable[[torch.Tensor], bool]] = None
) -> bool:
    """View tensor and validate it.
    If valid_func is not None, it will be called with the tensor as the only argument.

    Example:
    from meterfuncs import view
    view.tensor()
    """
    print(tensor.size())
    if valid_func:
        return valid_func(tensor)
    else:
        return True
