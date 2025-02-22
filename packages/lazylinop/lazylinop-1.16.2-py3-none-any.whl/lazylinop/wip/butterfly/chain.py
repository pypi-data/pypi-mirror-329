# -*- coding: utf-8 -*-

from lazylinop.wip.butterfly.GB_param_generate import DebflyGen
import numpy as np


class Chain():
    """
    The class ``Chain`` gathers a description of the sparsity
    patterns of Kronecker-sparse factors used when approximating
    a matrix as a product of such factors using :func:`.ksd`.

    The concatenation ``chain`` of two chains ``chain1``
    and ``chain2`` is given by ``chain = chain1 @ chain2``.
    :octicon:`info;1em;sd-text-info` Second dimension of the
    matrix described by ``chain1`` must be equal to the first
    dimension of the matrix described by ``chain2``.
    """
    def __init__(self, shape: tuple[int, int],
                 chain_type: str = 'smallest monotone',
                 n_patterns: int = None,
                 ks_patterns: list = None):
        """
        A ``Chain`` instance is defined by the shape of the
        matrix, the type of the chain, and other arguments
        that depend on the type of the chain.

        Args:
            shape: ``tuple``
                Shape of the input matrix, expect a tuple $(M,~N)$.
            chain_type: ``str``, optional
                Type of the chain to use in the decomposition.
                Possible values are:

                - ``'smallest monotone'`` (default).
                - ``'random'`` Random chain.
                - ``'custom'`` Custom chain (see ``ks_patterns``
                  for more details).
                - ``'square dyadic'`` Number of ``ks_patterns`` is equal
                  to ``np.log2(shape[0])``.
                  Here, ``n_patterns=...`` has no effect.
                  Matrix must be square ``shape[0] = shape[1]`` and
                  shape values must be power of two.
                  The l-th pattern is given by
                  ``(2 ** (l - 1), 2, 2, shape[0] // 2 ** l)`` where
                  ``1 <= l <= int(np.log2(shape[0]))``.
            n_patterns: ``int``, optional
                Number of factors of the decomposition.
                Default is 2, except when ``chain_type`` is:

                - ``'custom'`` in which case
                  ``n_patterns`` is ``len(ks_patterns)``.
                - ``'square dyadic'`` in which case
                  ``n_patterns`` is ``int(np.log2(shape[0]))``.
            ks_patterns: ``list``, optional
                List of pattern $(a_i,~b_i,~c_i,~d_i)$.
                Size of the tuple must be equal to the
                number of factors.
                It is only used when ``chain_type`` argument
                is ``'custom'`` (default is ``None``).

        Attributes:
            shape: ``tuple``
                Shape of the input matrix.
            n_patterns: ``int``
                Number of factors of the decomposition.
            ks_patterns: ``list``
                List of pattern $(a_i,~b_i,~c_i,~d_i)$.
            chainable: ``bool``
                ``True`` if ``self`` is chainable, ``False`` otherwise.
                ``chainable`` is ``True`` if the three following
                conditions return ``True``:

                - $M=a_0b_0d_0$ is ``True``
                - and $a_ic_id_i=a_{i+1}c_{i+1}d_{i+1}$ is ``True``
                - and $N=a_{n-1}c_{n-1}d_{n-1}$ is ``True``
                See [1] for more details.

        Return:
            ``chain``

        Examples:
            >>> from lazylinop.wip.butterfly.ksd import Chain
            >>> chain = Chain((2, 2), 'smallest monotone', n_patterns=2)
            >>> chain.ks_patterns
            [(1, 1, 1, 2, 1, 1), (1, 2, 2, 1, 1, 1)]
            >>> chain = Chain((2, 2), 'custom', ks_patterns=[(2, 1, 1, 2), (2, 1, 1, 2)])
            >>> chain.ks_patterns
            [(2, 1, 1, 2, 1, 1), (2, 1, 1, 2, 1, 1)]
            >>> # Concatenation of two chains.
            >>> chain1 = Chain((2, 3), 'smallest monotone', n_patterns=2)
            >>> chain2 = Chain((3, 4), 'smallest monotone', n_patterns=2)
            >>> chain = chain1 @ chain2
            >>> chain.shape
            (2, 4)
            >>> chain.n_patterns
            4
            >>> chain.ks_patterns
            [(1, 1, 1, 2), (1, 2, 3, 1), (1, 1, 1, 3), (1, 3, 4, 1)]

        References:
            [1] Butterfly Factorization with Error Guarantees.
            Léon Zheng, Quoc-Tung Le, Elisa Riccietti, and Rémi Gribonval
            https://hal.science/hal-04763712v1/document
        """
        if chain_type != 'custom' and chain_type != 'random' and \
           chain_type != 'smallest monotone' and chain_type != 'square dyadic':
            raise ValueError("chain_type must be either 'custom',"
                             + " 'random', 'smallest monotone'"
                             + " or 'square dyadic'.")
        if chain_type == 'custom' and n_patterns is not None:
            raise Exception("'custom' chain type expects"
                            + " n_patterns to be None.")
        if chain_type != 'custom' and ks_patterns is not None:
            raise Exception("'smallest_monotone', 'square dyadic' and"
                            + " 'random' expect"
                            + " ks_patterns to be None.")
        self.shape = shape
        self._chain_type = chain_type
        self.n_patterns = n_patterns
        if chain_type == 'custom':
            if ks_patterns is None:
                raise Exception("ks_patterns expects a tuple of tuple.")
            self.n_patterns = len(ks_patterns)
        self.ks_patterns = ks_patterns

        if chain_type == 'custom':
            tmp = self.ks_patterns
            # Convert to 'abcdpq' format with p=q=1.
            self.ks_patterns = []
            for t in tmp:
                self.ks_patterns.append((t[0], t[1], t[2], t[3]))
            self.chainable = self._is_chainable()
        elif chain_type == 'random':
            rank = 1
            test = DebflyGen(self.shape[0], self.shape[1], rank)
            tmp = test.random_debfly_chain(n_patterns, format="abcd")
            # Convert to 'abcdpq' format with p=q=1.
            self.ks_patterns = []
            for t in tmp:
                self.ks_patterns.append((t[0], t[1], t[2], t[3]))
            del test
            self.chainable = True
        elif chain_type == 'smallest monotone':
            rank = 1
            test = DebflyGen(self.shape[0], self.shape[1], rank)
            _, tmp = test.smallest_monotone_debfly_chain(
                self.n_patterns, format="abcdpq")
            # Convert to 'abcd' format.
            self.ks_patterns = []
            for t in tmp:
                self.ks_patterns.append((t[0], t[1], t[2], t[3]))
            del test
            self.chainable = True
        elif chain_type == 'square dyadic':
            m, n = self.shape
            if m != n:
                raise Exception("Matrix must be square shape[0]=shape[1].")
            ok = ((m & (m - 1)) == 0) and m > 0
            ok = ok and (((n & (n - 1)) == 0) and n > 0)
            if not ok:
                raise Exception("shape of the matrix must be power of two.")
            self.n_patterns = int(np.log2(m))
            self.ks_patterns = []
            for i in range(1, self.n_patterns + 1):
                self.ks_patterns.append((2 ** (i - 1), 2, 2, m // 2 ** i))
            self.chainable = True
        else:
            pass

    def _is_chainable(self):
        """
        Check if ``self`` is chainable.
        The following conditions must be true:

        - $M=a_0b_0d_0$
        - $a_ic_id_i=a_{i+1}c_{i+1}d_{i+1}$
        - $N=a_{n-1}c_{n-1}d_{n-1}$
        See [1] for more details.

        References:
            [1] Butterfly Factorization with Error Guarantees.
            Léon Zheng, Quoc-Tung Le, Elisa Riccietti, and Rémi Gribonval
            https://hal.science/hal-04763712v1/document
        """
        if self._chain_type != 'custom':
            return True
        # a_1 * b_1 * d_1 must be equal to the number
        # of rows of the input matrix.
        a, b, c, d = self.ks_patterns[0]
        if a * b * d != self.shape[0]:
            return False
        # a_F * c_F * d_F must be equal to the number
        # of columns of the input matrix.
        F = self.n_patterns
        a, b, c, d = self.ks_patterns[F - 1]
        if a * c * d != self.shape[1]:
            return False
        # Number of columns of the current factor must
        # be equal to the number of rows of the next factor.
        for i in range(F - 1):
            a, b, c, d = self.ks_patterns[i]
            col = a * c * d
            a, b, c, d = self.ks_patterns[i + 1]
            row = a * b * d
            if col != row:
                return True
        return True

    def __matmul__(self, chain):
        """
        Return the concatenation of two chains.

        Args:
            chain: ``Chain``
                An instance of ``Chain``
                to concatenate with ``self``.

        Returns:
            An instance of ``Chain`` that is the
            concatenation of ``chain`` and ``self``.

        Examples:
            >>> from lazylinop.wip.butterfly.ksd import Chain
            >>> chain1 = Chain((2, 3), 'smallest monotone', n_patterns=2)
            >>> chain1.ks_patterns
            [(1, 1, 1, 2), (1, 2, 3, 1)]
            >>> chain2 = Chain((3, 4), 'smallest monotone', n_patterns=2)
            >>> chain2.ks_patterns
            [(1, 1, 1, 3), (1, 3, 4, 1)]
            >>> chain = chain1 @ chain2
            >>> chain.shape
            (2, 4)
            >>> chain.n_patterns
            4
            >>> chain.ks_patterns
            [(1, 1, 1, 2), (1, 2, 3, 1), (1, 1, 1, 3), (1, 3, 4, 1)]
        """
        M, K = self.shape
        if K != chain.shape[0]:
            raise Exception("self.shape[1] must be equal to chaine.shape[0].")
        return Chain((M, chain.shape[1]), chain_type='custom',
                     n_patterns=None,
                     ks_patterns=self.ks_patterns + chain.ks_patterns)
