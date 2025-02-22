from lazylinop import binary_dtype, LazyLinOp, aslazylinops
import numpy as np


def block_diag(*ops):
    """
    Returns a :class:`.LazyLinOp` ``L`` that acts as the block-diagonal
    concatenation of compatible linear operators ``ops``.

    Args:
        ops:
            Operators (:class:`.LazyLinOp`-s or other compatible
            linear operators) to concatenate block-diagonally.

    Returns:
        The resulting block-diagonal :class:`.LazyLinOp`.

    Example:
        >>> import numpy as np
        >>> import lazylinop as lz
        >>> from lazylinop import aslazylinop
        >>> import scipy
        >>> nt = 10
        >>> d = 64
        >>> v = np.random.rand(d)
        >>> terms = [np.random.rand(64, 64) for _ in range(10)]
        >>> ls = lz.block_diag(*terms) # ls is the block diagonal LazyLinOp
        >>> np.allclose(scipy.linalg.block_diag(*terms), ls.toarray())
        True

    .. seealso::
        `scipy.linalg.block_diag <https://docs.scipy.org/doc/scipy/reference/
        generated/scipy.linalg.block_diag.html>`_,
        :func:`.aslazylinop`
    """

    n_ops = len(ops)

    nrows, ncols = 0, 0
    for i in range(n_ops):
        nrows += ops[i].shape[0]
        ncols += ops[i].shape[1]
        if i == 0:
            dtype = ops[0].dtype
        else:
            dtype = binary_dtype(dtype, ops[i].dtype)

    def _matmat(x, adjoint):
        # Loop over blocks.
        h = int(adjoint)
        cum_y, cum_x = 0, 0
        y = np.empty((ncols if adjoint
                      else nrows, x.shape[1]),
                     dtype=binary_dtype(dtype, x.dtype))
        for i, L in enumerate(ops):
            m, n = L.shape[h], L.shape[1 - h]
            y[cum_y:(cum_y + m)] = (L.T.conj() if adjoint
                                    else L) @ x[cum_x:(cum_x + n)]
            cum_y += m
            cum_x += n
        return y

    return LazyLinOp(
        shape=(nrows, ncols),
        matmat=lambda x: _matmat(x, False),
        rmatmat=lambda x: _matmat(x, True)
    )
