# -*- coding: utf-8 -*-

from lazylinop import aslazylinop, islazylinop, LazyLinOp
from lazylinop.basicops import eye
from lazylinop.wip.butterfly.GB_factorization import GBfactorize
from lazylinop.wip.butterfly.GB_operators import twiddle_to_dense
from lazylinop.wip.butterfly.GB_param_generate import DebflyGen
from lazylinop.wip.butterfly.ksm import ksm, _find_hyper_parameters
from lazylinop.wip.butterfly.ksm import multiple_ksm, _context
from lazylinop.wip.butterfly import Chain
try:
    import pickle
except ModuleNotFoundError:
    from warnings import warn
    warn("pickle not found, " +
         " please install pickle to save LazyLinOp object.")
try:
    import json
except ModuleNotFoundError:
    from warnings import warn
    warn("json not found, " +
         " please install json to save result of ksd function.")
try:
    import pycuda.driver as cuda
    import pycuda._driver as _cuda
except:
    cuda, _cuda = None, None
try:
    import pyopencl as cl
except:
    cl = None
from scipy.sparse import csr_matrix
import numpy as np
try:
    import torch
except ModuleNotFoundError:
    # "Fake" torch
    class Torch():
        def __init__(self):
            self._Tensor = type(None)

        @property
        def Tensor(self):
            return self._Tensor

    torch = Torch()


def bitrev_perm(n):
    r"""
    Bitreversal permutation.

    Args:
        n: ``int``
            The size of the permutation, it must be a power of two.
            P dimensions will be n x n.

    Returns:
        A ``scipy.sparse.csr_matrix`` defining the bit-reversal permutation.

    .. seealso::
        `Wikipedia <https://en.wikipedia.org/wiki/Bit-reversal_permutation>`_.
    """
    if np.log2(n) > np.log2(np.floor(n)):
        raise ValueError('n must be a power of two')
    row_inds = np.arange(0, n, dtype='int')
    col_inds = bitrev(row_inds)
    ones = np.ones((n), dtype='float')
    return csr_matrix((ones, (row_inds, col_inds)), shape=(n, n))


def bitrev(inds):
    r"""
    Bitreversal permutation.

    Args:
        inds: ``list[int]``
            The list of indices to bit-reverse.

    Returns:
        The bit-reversal permutation of inds.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.butterfly.ksd import bitrev
        >>> bitrev(np.arange(4))
        array([0, 2, 1, 3])

    .. seealso::
        `Wikipedia <https://en.wikipedia.org/wiki/Bit-reversal_permutation>`_.
    """
    n = len(inds)
    if n == 1:
        return inds
    else:
        even = bitrev(inds[np.arange(0, n, 2, dtype='int')])
        odd = bitrev(inds[np.arange(1, n, 2, dtype='int')])
        return np.hstack((even, odd))


def _balanced_permutation(k):
    if k == 1:
        return [1]
    elif k == 2:
        return [1, 2]
    if k % 2 == 0:
        left_perm = _balanced_permutation((k // 2) - 1)
        right_perm = [
            i + (k + 1) // 2 for i in _balanced_permutation(k // 2)]
        return [k // 2] + left_perm + right_perm
    elif k % 2 == 1:
        left_perm = _balanced_permutation(k // 2)
        right_perm = [
            i + (k + 1) // 2 for i in _balanced_permutation(k // 2)]
        return [k // 2 + 1] + left_perm + right_perm


def ksd(matrix: np.ndarray,
        chain: Chain,
        ortho: bool = True,
        order: str = 'l2r',
        svd_backend: str = 'numpy',
        save: str = '',
        **kwargs):
    r"""
    Returns a :class:`.LazyLinOp`
    corresponding to the (often called "butterfly") factorization of
    ``matrix`` into Kronecker-sparse factors with sparsity patterns
    determined by ``chain``. Also returned a list of :class:`.LazyLinOp`
    of all the factors of the decomposition.

    - ``A, _ = ksd(...)`` returns a :class:`.LazyLinOp`
      corresponding to the factorization of ``matrix`` where
      ``A = ksm(...) @ ksm(...) @ ... @ ksm(...)``.
    - ``_, factors = ksd(...)`` returns a list of :class:`.LazyLinOp`
      of all the factors of the decomposition where
      ``factors = [ksm(...), ksm(...), ..., ksm(...)]``.

   ``A.data`` returns a dict of the result of the factorization.
    Each factor ``i`` is associated to a key ``'factor' + str(i)``.
    For each factor you can access to its values using ``'values'``
    and Kronecker-sparse pattern using ``'ks_pattern'``.

    Args:
        matrix: ``np.ndarray``
            Matrix to factorize.
        chain: ``Chain``
            Instance of the ``Chain`` class.
            See :class:`.Chain` documentation for more details.
        ortho: ``bool``, optional
            Default is ``True``.
        order: ``str``, optional
            See [1] for more details.

            - ``'l2r'`` Left-to-right decomposition (default).
            - ``'balanced'``
        svd_backend: ``str``, optional
            Use NumPy ``'numpy'`` (default) or PyTorch ``'pytorch'``
            to compute SVD and QR decompositions.

    Kwargs:
        Additional arguments ``backend``,
        ``params`` (one per pattern) to pass to :func:`ksm`.

    Returns:
        A ``tuple(A, factors)`` where ``A`` is a :class:`.LazyLinOp`
        that corresponds to the product of ``n_patterns``
        :class:`.LazyLinOp` each one returned by :func:`ksm` and where
        ``factors`` is a list of ``n_patterns`` :class:`.LazyLinOp`
        each one returned by :func:`ksm`.

    .. seealso::
        - :class:`.Chain`,
        - :func:`ksm`,
        - :func:`read`,
        - :func:`save`.

    References:
        [1] Butterfly Factorization with Error Guarantees.
        Léon Zheng, Quoc-Tung Le, Elisa Riccietti, and Rémi Gribonval
        https://hal.science/hal-04763712v1/document

    Examples:
        >>> import numpy as np
        >>> from lazylinop import aslazylinop
        >>> from lazylinop.wip.butterfly import bitrev_perm, Chain, ksd
        >>> N = 2 ** 8
        >>> M = N
        >>> n_factors = 2
        >>> x = np.exp(-2.0j * np.pi * np.arange(N) / N)
        >>> V = np.vander(x, N=None, increasing=True)[:M, :]
        >>> chain = Chain(V.shape, 'smallest monotone', n_factors)
        >>> # Use bit reversal permutations matrix.
        >>> P = bitrev_perm(N)
        >>> F, _ = ksd(V @ P.T, chain)
        >>> F = F @ aslazylinop(P)
        >>> approx = F @ np.eye(F.shape[1])
        >>> error = np.linalg.norm(V - approx) / np.linalg.norm(V)
        >>> np.allclose(error, 0.0)
        True
    """

    # Rank of sub-blocks (1 is default), used by the underlying SVD.
    rank = 1

    if chain.n_patterns < 2:
        raise ValueError("n_patterns must be > 1.")

    shape = matrix.shape

    if 'backend' not in kwargs.keys():
        kwargs['backend'] = 'numpy'
    if 'params' not in kwargs.keys():
        kwargs['params'] = [(None, None)] * chain.n_patterns
    else:
        if not isinstance(kwargs['params'], list):
            raise Exception("params must be a list of tuple.")
        n_factors = len(kwargs['params'])
        if n_factors != chain.n_patterns:
            raise Exception("Length of kwargs['params'] must be" +
                            " equal to chain.n_patterns.")
        for i in range(n_factors):
            if not isinstance(kwargs['params'][i], tuple):
                raise Exception("params must be a list of tuple.")

    nrows, ncols = shape[0], shape[1]
    if nrows <= rank or ncols <= rank:
        raise Exception("Number of rows and number of columns must" +
                        " be greater than the rank value.")
    if type(matrix) is np.ndarray and (svd_backend != 'numpy' and
                                       svd_backend != 'scipy'):
        raise Exception("Because svd_backend='numpy' or 'scipy'" +
                        " matrix must be a NumPy array.")
    if type(matrix).__name__ == 'Torch' and svd_backend != 'pytorch':
        raise Exception("Because ``svd_backend='pytorch'`` matrix" +
                        " must be a PyTorch tensor.")

    matrix = matrix.reshape(1, 1, nrows, ncols)

    # Set architecture for butterfly factorization.
    if chain._chain_type == "custom":
        min_param = chain.ks_patterns
    elif chain._chain_type == "square dyadic":
        min_param = chain.ks_patterns
    elif chain._chain_type == "random":
        context, context_idx = _context(kwargs['backend'])
        if context is None:
            min_param = chain.ks_patterns
        else:
            # Get maximum shared memory before to determine hyper-parameters.
            if cuda is not None and \
               _cuda is not None and isinstance(context, cuda.Context):
                smem = context.get_device().get_attribute(
                    _cuda.device_attribute.MAX_SHARED_MEMORY_PER_BLOCK
                )
                max_block_dim = (
                    context.get_device().get_attribute(cuda.device_attribute.MAX_BLOCK_DIM_X),
                    context.get_device().get_attribute(cuda.device_attribute.MAX_BLOCK_DIM_Y),
                    context.get_device().get_attribute(cuda.device_attribute.MAX_BLOCK_DIM_Z))
                max_grid_dim = (
                    context.get_device().get_attribute(cuda.device_attribute.MAX_GRID_DIM_X),
                    context.get_device().get_attribute(cuda.device_attribute.MAX_GRID_DIM_Y),
                    context.get_device().get_attribute(cuda.device_attribute.MAX_GRID_DIM_Z))
            elif cl is not None:
                smem = context.devices[0].get_info(
                    cl.device_info.LOCAL_MEM_SIZE)
                max_block_dim = None
                max_grid_dim = None
            else:
                smem = 49152
                max_block_dim = None
                max_grid_dim = None
            # Find a chain such that hyper-parameters are
            # found for all the factors.
            new_chain = chain
            for t in range(10000):
                tmp = new_chain.ks_patterns
                # print('r', tmp)
                failed = False
                for i in range(new_chain.n_patterns):
                    a, b, c, d = tmp[i]
                    # Check if we find hyper-parameters for the current factor.
                    hp = _find_hyper_parameters(a, b, c, d, 1,
                                                smem, matrix.dtype.itemsize,
                                                max_block_dim=max_block_dim,
                                                max_grid_dim=max_grid_dim)
                    if hp == [0] * 6:
                        # print('failed', a, b, c, d)
                        failed = True
                        break
                    rhp = _find_hyper_parameters(a, c, b, d, 1,
                                                 smem, matrix.dtype.itemsize,
                                                 max_block_dim=max_block_dim,
                                                 max_grid_dim=max_grid_dim)
                    if rhp == [0] * 6:
                        # print('rfailed', a, b, c, d)
                        failed = True
                        break
                if not failed:
                    min_param = new_chain.ks_patterns
                    break
                else:
                    new_chain = Chain(chain.shape,
                                      chain_type='random',
                                      n_patterns=chain.n_patterns)
            del context
    elif chain._chain_type == "smallest monotone":
        min_param = chain.ks_patterns
    else:
        pass

    # Permutation.
    if order == "l2r":
        perm = [i for i in range(chain.n_patterns - 1)]
    elif order == "balanced":
        perm = [i - 1 for i in _balanced_permutation(chain.n_patterns - 1)]
    else:
        raise NotImplementedError("order must be either 'l2r' or 'balanced'")

    # FIXME: p, q compatibility
    tmp = []
    for i in range(len(min_param)):
        tmp.append((min_param[i][0], min_param[i][1],
                    min_param[i][2], min_param[i][3], 1, 1))
    min_param = tmp

    # Run factorization and return a list of factors.
    factor_list = GBfactorize(matrix, min_param,
                              perm, ortho,
                              backend=svd_backend)

    data = {}
    for i, f in enumerate(factor_list):
        data["factor" + str(i)] = {}
        # See GB_operators.twiddle_to_dense().
        a, d, b, c = f.factor.shape
        if isinstance(f.factor, torch.Tensor):
            data["factor" + str(i)]['package'] = 'torch'
            factor_list[i] = (f.factor).permute(0, 2, 1, 3).permute(0, 1, 3, 2)
        elif isinstance(f.factor, np.ndarray):
            data["factor" + str(i)]['package'] = 'numpy'
            factor_list[i] = np.swapaxes(
                np.swapaxes((f.factor), 2, 1), 3, 2)
        else:
            data["factor" + str(i)]['package'] = 'none'
            pass
        # Store current factor in a dict.
        data["factor" + str(i)]['ks_pattern'] = (a, b, c, d)
        data["factor" + str(i)]['values'] = factor_list[i].real.tolist()
        if 'complex' in str(factor_list[i].dtype):
            data["factor" + str(i)]['imag'] = factor_list[i].imag.tolist()
        data["factor" + str(i)]['dtype'] = str(factor_list[i].dtype)
        data["factor" + str(i)]['params'] = kwargs['params'][i]
        data["factor" + str(i)]['backend'] = kwargs['backend']

    factors = []
    for i in range(chain.n_patterns):
        factors.append(
            ksm(factor_list[i], params=kwargs['params'][i],
                backend=kwargs['backend']))
    L = multiple_ksm(factor_list,
                     params=kwargs['params'], backend=kwargs['backend'])

    # Add data to instance for further use.
    L.data = data

    return L, factors


def save(L: LazyLinOp, name: str):
    """
    Save the instance ``L = A[0]`` of :class:`LazyLinOp`
    returned by ``A = ksd(...)`` function.
    Save the result of the factorization
    in a json file ``name + '.json'``.
    Each factor ``i`` is associated to a key ``'factor' + str(i)``.
    For each factor you can access to its values using ``'values'``
    and Kronecker-sparse pattern using ``'ks_pattern'``.
    To load the result of the factorization use :func:`read`.

    Args:
        L: ``LazyLinOp``
            The ``LazyLinOp`` ``L`` to save.
        name: ``str``
            Name of the file.

    .. seealso::
        - :func:`ksd`,
        - :func:`read`.

    Examples:
        >>> import scipy as sp
        >>> import numpy as np
        >>> from lazylinop.wip.butterfly import Chain, ksd, read, save
        >>> H = sp.linalg.hadamard(8)
        >>> x = np.random.randn(8)
        >>> chain = Chain(H.shape, 'smallest monotone', 2)
        >>> A, factors = ksd(H, chain)
        >>> save(A, "hadamard_8x8")
        >>> A_, factors_, chain_ = read("hadamard_8x8")
        >>> y = A @ x
        >>> y_ = A_ @ x
        >>> np.allclose(y, y_)
        True
    """
    if not islazylinop(L):
        raise Exception("L must be an instance of LazyLinOp class.")
    # Save result of factorization in a json file.
    with open(name + '.json', 'w') as f:
        json.dump(L.data, f, indent=1)


def read(name: str):
    """
    Read the tuple ``(A, factors, chain)`` from file ``name``.
    The file ``name`` has been created by :func:`ksd`.

    Args:
        name: ``str``
            Name of the file where to read the
            tuple ``(A, factors, chain)``.

    Returns:
        A ``tuple(A, factors, chain)`` where ``A`` is a :class:`.LazyLinOp`
        that corresponds to the product of ``n_patterns``
        :class:`.LazyLinOp` each one returned by :func:`ksm` and where
        ``factors`` is a list of ``n_patterns`` :class:`.LazyLinOp`
        each one returned by :func:`ksm` and where chain is a :class:`.Chain`
        that gathers a description of the sparsity patterns
        of Kronecker-sparse factors.
        If file does not exist, return ``(None, [], None)``.

    .. seealso::
        - :func:`ksd`,
        - :func:`save`.

    Examples:
        >>> import scipy as sp
        >>> import numpy as np
        >>> from lazylinop.wip.butterfly import Chain, ksd, read, save
        >>> H = sp.linalg.hadamard(8)
        >>> x = np.random.randn(8)
        >>> chain = Chain(H.shape, 'smallest monotone', 2)
        >>> A, factors = ksd(H, chain)
        >>> save(A, "hadamard_8x8")
        >>> # Read wrong file.
        >>> read("hadamard_4x4")
        (None, [], None)
        >>> A_, factors_, chain_ = read("hadamard_8x8")
        >>> y = A @ x
        >>> y_ = A_ @ x
        >>> np.allclose(y, y_)
        True
    """
    try:
        A, factors, ks_patterns = None, [], []
        with open(name + '.json', 'r') as f:
            data = json.load(f)
            # Loop over the Kronecker-sparse factors.
            values, params, backend = [], [], []
            for k in data.keys():
                K = ksm(
                    np.asarray(data[k]['values']).astype(data[k]['dtype']),
                    params=data[k]['params'], backend=data[k]['backend'])
                factors.append(K)
                if 'complex' in str(data[k]['dtype']):
                    values.append(
                        np.asarray(data[k]['values']).astype(data[k]['dtype']) +
                        (1j * np.asarray(data[k]['imag'])).astype(data[k]['dtype']))
                else:
                    values.append(
                        np.asarray(data[k]['values']).astype(data[k]['dtype']))
                params.append(data[k]['params'])
                backend.append(data[k]['backend'])
                ks_patterns.append(data[k]['ks_pattern'])
            A = multiple_ksm(values, params, backend[0])
            A.data = data
        return (A, factors, Chain(A.shape, chain_type='custom',
                                  ks_patterns=ks_patterns))
    except IOError:
        return (None, [], None)


# def save(L: tuple[LazyLinOp, list], name: str):
#     """
#     Save the tuple ``(A, factors)`` returned by
#     ``ksd(...)`` function.

#     Args:
#         L: ``tuple = (lazylinop.LazyLinOp, list)``
#             The tuple ``(A, factors)`` to save.
#         name: ``str``
#             Name of the file.

#     .. seealso::
#         - :func:`ksd`,
#         - :func:`read`.
#     """
#     msg = "L must be a tuple (lazylinop.LazyLinOp, list)."
#     if not isinstance(L, tuple) and len(L) != 2 and \
#        not islazylinop(L[0]) and not isinstance(L[1], list):
#         raise Exception(msg)
#     with open(name, 'wb') as f:
#         pickle.dump(L, f, pickle.HIGHEST_PROTOCOL)


# def read(name: str):
#     """
#     Read the tuple ``(A, factors)`` from file ``name``.
#     The file ``name`` has been created by :func:`save`.

#     Args:
#         name: ``str``
#             Name of the file where to read the
#             tuple ``(A, factors)``.

#     Returns:
#         ``tuple`` if file exists, otherwise ``None``.

#     .. seealso::
#         - :func:`ksd`,
#         - :func:`save`.
#     """
#     try:
#         with open(name, 'rb') as f:
#             L = pickle.load(f)
#     except IOError:
#         L = None
#     return L
