from lazylinop import LazyLinOp
import numpy as np
import os
import warnings


def bitrev(N: int, backend: str = 'recursive'):
    r"""
    Returns a :class:`.LazyLinOp` ``L`` for the bit-reversal permutation.
    :octicon:`alert-fill;1em;sd-text-danger` Size of the signal ``N``
    must be a power of two. Bit-reversal permutation maps each item
    of the sequence ``0`` to ``N - 1`` to the item whose bit
    representation has the same bits in reversed order.

    Args:
        N: ``int``
            Size of the signal.
        backend: ``str``, optional
            - Default is 'recursive'.
            - 'numba' backend implements algorithm from [1].

    Returns:
        :class:`.LazyLinOp`

    Example:
        >>> import numpy as np
        >>> from lazylinop.basicops import bitrev
        >>> x = np.arange(4)
        >>> L = bitrev(4)
        >>> L @ x
        array([0, 2, 1, 3])

    References:
        [1] Fast Bit-Reversal Algorithms, Anne Cathrine Elster.
            IEEE International Conf. on Acoustics, Speech, and
            Signal Processing 1989 (ICASSP'89), Vol. 2,
            pp. 1099-1102, May 1989.

    .. seealso:
        - `Bit-reversal permutation (Wikipedia) <https://en.wikipedia.org/
          wiki/Bit-reversal_permutation>`_.
    """

    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of 2.")
    if backend != 'recursive' and backend != 'numba':
        raise ValueError("backend must be either 'recursive' or 'numba'.")

    def njit(*args, **kwargs):
        def dummy(f):
            return f
        return dummy

    def prange(n):
        return range(n)

    new_backend = backend
    try:
        import numba as nb
        from numba import njit
        if "NUMBA_DISABLE_JIT" in os.environ.keys():
            nb.config.DISABLE_JIT = os.environ["NUMBA_DISABLE_JIT"]
        else:
            nb.config.DISABLE_JIT = 0
        nb.config.THREADING_LAYER = 'omp'
    except ImportError:
        warnings.warn("Did not find Numba, switch to 'recursive' backend.")
        new_backend = 'recursive'

    def _bitrev(x):
        n = x.shape[0]
        y = np.copy(x)
        if n == 1:
            return y
        else:
            return np.hstack(
                (
                    _bitrev(y[np.arange(0, n, 2, dtype='int')]),
                    _bitrev(y[np.arange(1, n, 2, dtype='int')])
                )
            )

    @njit(cache=True)
    def numba_bitrev(n):
        p = int(np.log2(n))
        H = 1 << (p - 1)
        idx = np.empty(n, dtype='int')
        for i in range(n):
            idx[i] = i
        idx[1] = H
        for i in range(2, n - 1, 2):
            idx[i] = idx[i // 2] >> 1
            idx[i + 1] = idx[i] | idx[1]
        return idx

    def _matmat(x):
        if new_backend == 'recursive':
            return x[_bitrev(np.arange(x.shape[0])), :]
        else:
            return x[numba_bitrev(x.shape[0]), :]

    return LazyLinOp(
        shape=(N, N),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _matmat(x)
    )
