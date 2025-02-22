from typing import Union
import numpy as np
from lazylinop import LazyLinOp, binary_dtype


def ones(shape: tuple[int, int],
         dtype: Union[str, None] = None):
    """
    Returns a :class:`LazyLinOp` ones.

    .. admonition:: Fixed memory cost
        :class: admonition note

        Whatever is the shape of the ``ones``, it has the same memory cost.

    Args:

        shape: ``tuple[int, int]``
            Operator shape, e.g., ``(2, 3)``.

        dtype: ``str`` or ``numpy.dtype``, optional
            numpy dtype ``str`` (e.g. ``'float64'``).

    Returns:
        :class:`LazyLinOp` ones.

    Example:
        >>> import numpy as np
        >>> from lazylinop.basicops.ones import ones
        >>> L = ones((6, 5), dtype='float')
        >>> v = np.arange(5)
        >>> L @ v
        array([10., 10., 10., 10., 10., 10.])
        >>> A = np.ones((6, 5))
        >>> A @ v
        array([10., 10., 10., 10., 10., 10.])
        >>> M = np.arange(5 * 4).reshape(5, 4)
        >>> L @ M
        array([[40., 45., 50., 55.],
               [40., 45., 50., 55.],
               [40., 45., 50., 55.],
               [40., 45., 50., 55.],
               [40., 45., 50., 55.],
               [40., 45., 50., 55.]])
        >>> A @ M
        array([[40., 45., 50., 55.],
               [40., 45., 50., 55.],
               [40., 45., 50., 55.],
               [40., 45., 50., 55.],
               [40., 45., 50., 55.],
               [40., 45., 50., 55.]])

    .. seealso::
        `numpy.ones <https://numpy.org/devdocs/reference/generated/
        numpy.ones.html>`_

    """
    if not isinstance(shape, tuple):
        raise TypeError('shape is not a tuple')

    if len(shape) != 2:
        raise ValueError('shape must be of length 2')

    m, n = shape

    if dtype is None:
        dtype = 'int'

    def mul(nrows, ncols, x):
        out_dtype = binary_dtype(dtype, x.dtype)
        # x is always 2d.
        # x is a np array or scipy matrix (see LazyLinOp.__matmul__)
        # so it has a sum method.
        s = x.sum(axis=0)
        return np.tile(s, (nrows, 1)).astype(out_dtype)

    return LazyLinOp(shape=(m, n),
                     matmat=lambda x: mul(m, n, x),
                     rmatmat=lambda x: mul(n, m, x),
                     dtype=dtype)
