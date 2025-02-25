from lazylinop import LazyLinOp, binary_dtype, aslazylinops
import numpy as np


def kron(L1, L2):
    r"""
    Returns the :class:`LazyLinOp` for the Kronecker product $L_1\otimes L_2$
    using as a *definition* the mixed Kronecker matrix-vector property

    .. math::

        \begin{equation}
        (L_2^T\otimes L_1)x=\mathtt{vec}(L_1XL_2)
        \end{equation}

    where $X$ is a matrix of appropriate dimension
    such that $\mathtt{vec}(X)=x$.
    Importantly here $\mathtt{vec}(X)$ stacks the *columns* of $X$.

    .. note::
        This specialization is particularly optimized for multiplying the
        operator by a vector.

    Args:
        L1: (compatible linear operator)
            scaling factor,
        L2: (compatible linear operator)
            block factor.

    Returns:
        The Kronecker product :class:`LazyLinOp`.

    Example:
        >>> import numpy as np
        >>> import lazylinop as lz
        >>> A = np.random.randn(100, 100)
        >>> B = np.random.randn(100, 100)
        >>> AxB = np.kron(A, B)
        >>> lAxB = lz.kron(A, B)
        >>> x = np.random.randn(AxB.shape[1], 1)
        >>> print(np.allclose(AxB@x, lAxB@x))
        True
        >>> from timeit import timeit
        >>> timeit(lambda: AxB @ x, number=10) # doctest:+ELLIPSIS
        0...
        >>> # example: 0.4692082800902426
        >>> timeit(lambda: lAxB @ x, number=10) # doctest:+ELLIPSIS
        0...
        >>> # example 0.03464869409799576

    .. seealso::
        - `numpy.kron <https://numpy.org/doc/
          stable/reference/generated/numpy.kron.html>`_,
        - `scipy.sparse.kron <https://docs.scipy.org/doc/
          scipy/reference/generated/scipy.sparse.kron.html>`_,
        - `pylops.Kronecker <https://pylops.readthedocs.io/en/
          stable/api/generated/pylops.Kronecker.html>`_,
        - :func:`.aslazylinop`,
        - `Kronecker product on Wikipedia
          <https://en.wikipedia.org/wiki/Kronecker_product>`_.
    """
    L1, L2 = aslazylinops(L1, L2)

    def _kron(L1, L2, shape, x):

        # x is always 2d

        if hasattr(x, 'reshape') and \
           hasattr(x, '__matmul__') and hasattr(x, '__getitem__'):
            # From 1d stack of columns to 2d array.
            x_mat = x.reshape((L1.shape[1], L2.shape[1])).swapaxes(0, 1)
            # Do we multiply from left to right or from right to left?
            m, k = L2.shape
            k, n = x_mat.shape
            p, n = L1.shape
            ltor = m * k * n + m * n * p
            rtol = m * k * p + k * n * p
            # Compute and stack the columns of the results.
            if ltor < rtol:
                return ((L2 @ x_mat) @ L1.T).swapaxes(0, 1).reshape(shape[0])
            else:
                return (L2 @ (x_mat @ L1.T)).swapaxes(0, 1).reshape(shape[0])
        else:
            raise TypeError('x must possess reshape, __matmul__ and'
                            ' __getitem__ attributes to be multiplied by a'
                            ' Kronecker LazyLinOp (use toarray on the'
                            ' latter to multiply by the former)')

    shape = (L1.shape[0] * L2.shape[0], L1.shape[1] * L2.shape[1])
    return LazyLinOp(
        shape=shape,
        matvec=lambda x: _kron(L1, L2, shape, x),
        rmatvec=lambda x: _kron(L1.T.conj(), L2.T.conj(),
                                (shape[1], shape[0]), x),
        dtype=binary_dtype(L1.dtype, L2.dtype))
