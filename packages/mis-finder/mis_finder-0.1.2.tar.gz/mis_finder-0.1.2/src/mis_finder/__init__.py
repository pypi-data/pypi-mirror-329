__all__ = ["max_independent_set"]

from typing import TYPE_CHECKING, Annotated, Literal

from mis_finder.mis import max_independent_set as _max_independent_set

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray


    ArrayNxN = Annotated[NDArray[np.int64], Literal["N", "N"]]


def max_independent_set(adj_matrix: "ArrayNxN") -> list[int]:
    shape = adj_matrix.shape

    if len(shape) != 2 or shape[0] != shape[1]:
        raise TypeError(f"Adjacency matrix not square. Passed shape: {shape}")

    return _max_independent_set(adj_matrix)
