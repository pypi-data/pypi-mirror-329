import torch
import torch.nn.functional as F


def collateDetect(is_exit: bool = False):
    """decorators, to debug size.

    @collateDetect(is_exit=True)
    def collate_fn(): ...
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            print("func return[1] size: ", res[1].size())
            if is_exit:
                import sys

                sys.exit()
            return res

        return wrapper

    return decorator


def use_onehot(pos: int, num_classes=74):
    """this function is for dataset related, like __get_item__"""
    pos_tensor = F.one_hot(torch.tensor(pos), num_classes=num_classes).float()
    return pos_tensor


def use_embed(pos: int, dim: int = 1):
    """this function is for dataset related, like __get_item__,
    the shape will like (32, 1) if dim=1, (32, 1, 1) if dim=2"""
    if dim == 1:
        pos_tensor = torch.tensor(pos, dtype=torch.long)
    elif dim == 2:
        pos_tensor = torch.tensor([pos], dtype=torch.long)
    return pos_tensor
