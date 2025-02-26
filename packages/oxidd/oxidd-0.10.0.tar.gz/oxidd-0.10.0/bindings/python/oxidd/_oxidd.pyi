from __future__ import annotations

__all__ = [
    "BDDFunction",
    "BDDManager",
    "BDDSubstitution",
    "BCDDFunction",
    "BCDDManager",
    "BCDDSubstitution",
    "ZBDDFunction",
    "ZBDDManager",
    "DDMemoryError",
    "BooleanOperator",
]

import enum
from collections.abc import Iterable
from os import PathLike
from typing import final

from typing_extensions import Never, Self

@final
class BDDManager:
    r"""Manager for binary decision diagrams (without complement edges).

    Implements: :class:`~oxidd.protocols.BooleanFunctionManager`\
    [:class:`BDDFunction`]
    """

    @classmethod
    def __new__(
        cls, /, inner_node_capacity: int, apply_cache_capacity: int, threads: int
    ) -> BDDManager:
        """Create a new manager.

        Args:
            inner_node_capacity (int): Maximum count of inner nodes
            apply_cache_capacity (int): Maximum count of apply cache entries
            threads (int): Worker thread count for the internal thread pool

        Returns:
            BDDManager: The new manager
        """

    def new_var(self, /) -> BDDFunction:
        """Get a fresh variable, adding a new level to a decision diagram.

        Acquires the manager's lock for exclusive access.

        Returns:
            BDDFunction: A Boolean function that is true if and only if the
                variable is true
        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def true(self, /) -> BDDFunction:
        """Get the constant true Boolean function ``⊤``.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            BDDFunction: The constant true Boolean function ``⊤``
        """

    def false(self, /) -> BDDFunction:
        """Get the constant false Boolean function ``⊥``.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            BDDFunction: The constant false Boolean function ``⊥``
        """

    def num_inner_nodes(self, /) -> int:
        """Get the number of inner nodes.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            int: The number of inner nodes stored in this manager
        """

    def dump_all_dot_file(
        self,
        /,
        path: str | PathLike[str],
        functions: Iterable[tuple[BDDFunction, str]] = [],
        variables: Iterable[tuple[BDDFunction, str]] = [],
    ) -> None:
        """Dump the entire decision diagram in this manager as Graphviz DOT code.

        The output may also include nodes that are not reachable from
        ``functions``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            path (str | PathLike[str]): Path of the output file. If a file at
                ``path`` exists, it will be truncated, otherwise a new one will
                be created.
            functions (Iterable[tuple[BDDFunction, str]]): Optional names for
                BDD functions
            variables (Iterable[tuple[BDDFunction, str]]): Optional names for
                variables

        Returns:
            None
        """

    def __eq__(self, /, rhs: object) -> bool: ...
    def __ne__(self, /, rhs: object) -> bool: ...
    def __hash__(self, /) -> int: ...

@final
class BDDSubstitution:
    """Substitution mapping variables to replacement functions.

    Implements: :class:`~oxidd.protocols.FunctionSubst`
    """

    @classmethod
    def __new__(
        cls, /, pairs: Iterable[tuple[BDDFunction, BDDFunction]]
    ) -> BDDSubstitution:
        """Create a new substitution object for BDDs.

        See :meth:`BDDFunction.make_substitution()` fore more details.

        Args:
            pairs (Iterable[tuple[BDDFunction, BDDFunction]]):
                ``(variable, replacement)`` pairs, where all variables are
                distinct. The order of the pairs is irrelevant.

        Returns:
            BDDSubstitution: The new substitution
        """

@final
class BDDFunction:
    r"""Boolean function represented as a simple binary decision diagram (BDD).

    Implements:
        :class:`~oxidd.protocols.BooleanFunctionQuant`,
        :class:`~oxidd.protocols.FunctionSubst`\ [:class:`BDDSubstitution`],
        :class:`~oxidd.protocols.HasLevel`

    All operations constructing BDDs may throw a
    :exc:`~oxidd.util.DDMemoryError` in case they run out of memory.

    Note that comparisons like ``f <= g`` are based on an arbitrary total order
    and not related to logical implications. See the
    :meth:`Function <oxidd.protocols.Function.__lt__>` protocol for more
    details.
    """

    @classmethod
    def __new__(cls, _: Never) -> Self:
        """Private constructor."""

    @property
    def manager(self, /) -> BDDManager:
        """BDDManager: The associated manager."""

    def cofactors(self, /) -> tuple[Self, Self] | None:
        r"""Get the cofactors ``(f_true, f_false)`` of ``self``.

        Let f(x₀, …, xₙ) be represented by ``self``, where x₀ is (currently) the
        top-most variable. Then f\ :sub:`true`\ (x₁, …, xₙ) = f(⊤, x₁, …, xₙ)
        and f\ :sub:`false`\ (x₁, …, xₙ) = f(⊥, x₁, …, xₙ).

        Structurally, the cofactors are simply the children in case with edge
        tags adjusted accordingly.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            tuple[Self, Self] | None: The cofactors ``(f_true, f_false)``, or
                ``None`` if ``self`` references a terminal node.

        See Also:
            :meth:`cofactor_true`, :meth:`cofactor_false` if you only need one
            of the cofactors.
        """

    def cofactor_true(self, /) -> Self | None:
        """Get the cofactor ``f_true`` of ``self``.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            Self | None: The cofactor ``f_true``, or ``None`` if ``self``
                references a terminal node.

        See Also:
            :meth:`cofactors`, also for a more detailed description
        """

    def cofactor_false(self, /) -> Self | None:
        """Get the cofactor ``f_false`` of ``self``.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            Self | None: The cofactor ``f_false``, or ``None`` if ``self``
                references a terminal node.

        See Also:
            :meth:`cofactors`, also for a more detailed description
        """

    def level(self, /) -> int | None:
        """Get the level of the underlying node.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            int | None: The level, or ``None`` if the node is a terminal
        """

    def __invert__(self, /) -> Self:
        """Compute the negation ``¬self``.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            Self: ``¬self``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __and__(self, rhs: Self, /) -> Self:
        """Compute the conjunction ``self ∧ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ∧ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __or__(self, rhs: Self, /) -> Self:
        """Compute the disjunction ``self ∨ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ∨ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __xor__(self, rhs: Self, /) -> Self:
        """Compute the exclusive disjunction ``self ⊕ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ⊕ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def nand(self, rhs: Self, /) -> Self:
        """Compute the negated conjunction ``self ⊼ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ⊼ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def nor(self, rhs: Self, /) -> Self:
        """Compute the negated disjunction ``self ⊽ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ⊽ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def equiv(self, rhs: Self, /) -> Self:
        """Compute the equivalence ``self ↔ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ↔ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def imp(self, rhs: Self, /) -> Self:
        """Compute the implication ``self → rhs`` (or ``f ≤ g``).

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self → rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def imp_strict(self, rhs: Self, /) -> Self:
        """Compute the strict implication ``self < rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self < rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def ite(self, /, t: Self, e: Self) -> Self:
        """Compute the BDD for the conditional ``t if self else e``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            t (Self): Then-case; must belong to the same manager as ``self``
            e (Self): Else-case; must belong to the same manager as ``self``

        Returns:
            Self: The Boolean function ``f(v: 𝔹ⁿ) = t(v) if self(v) else e(v)``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    @classmethod
    def make_substitution(cls, pairs: Iterable[tuple[Self, Self]], /) -> Self:
        """Create a new substitution object from pairs ``(var, replacement)``.

        The intent behind substitution objects is to optimize the case where the
        same substitution is applied multiple times. We would like to re-use
        apply cache entries across these operations, and therefore, we need a
        compact identifier for the substitution. This identifier is provided by
        the returned substitution object.

        Args:
            pairs (Iterable[tuple[Self, Self]]): ``(variable, replacement)``
                pairs, where all variables are distinct. The order of the pairs
                is irrelevant.

        Returns:
            Self: The substitution to be used with :meth:`substitute()`
        """

    def substitute(self, substitution: BDDSubstitution, /) -> Self:
        """Substitute variables in ``self`` according to ``substitution``.

        The substitution is performed in a parallel fashion, e.g.:
        ``(¬x ∧ ¬y)[x ↦ ¬x ∧ ¬y, y ↦ ⊥] = ¬(¬x ∧ ¬y) ∧ ¬⊥ = x ∨ y``

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            substitution (BDDSubstitution): A substitution object created using
                :meth:`make_substitution()`. All contained DD functions must
                belong to the same manager as ``self``.

        Returns:
            Self: ``self`` with variables substituted
        """

    def forall(self, /, vars: Self) -> Self:
        """Compute the universal quantification over ``vars``.

        This operation removes all occurrences of variables in ``vars`` by
        universal quantification. Universal quantification ∀x. f(…, x, …) of a
        Boolean function f(…, x, …) over a single variable x is
        f(…, 0, …) ∧ f(…, 1, …).

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (Self): Set of variables represented as conjunction thereof.
                Must belong to the same manager as ``self``.

        Returns:
            Self: ∀ vars: self

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def exists(self, /, vars: Self) -> Self:
        """Compute the existential quantification over ``vars``.

        This operation removes all occurrences of variables in ``vars`` by
        existential quantification. Existential quantification ∃x. f(…, x, …) of
        a Boolean function f(…, x, …) over a single variable x is
        f(…, 0, …) ∨ f(…, 1, …).

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (Self): Set of variables represented as conjunction thereof.
                Must belong to the same manager as ``self``.

        Returns:
            Self: ∃ vars: self

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def exist(self, /, vars: Self) -> Self:
        """Deprecated alias for ``exists()``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (Self): Set of variables represented as conjunction thereof.
                Must belong to the same manager as ``self``.

        Returns:
            Self: ∃ vars: self

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def unique(self, /, vars: Self) -> Self:
        """Compute the unique quantification over ``vars``.

        This operation removes all occurrences of variables in ``vars`` by
        unique quantification. Unique quantification ∃!x. f(…, x, …) of a
        Boolean function f(…, x, …) over a single variable x is
        f(…, 0, …) ⊕ f(…, 1, …). Unique quantification is also known as the
        `Boolean difference <https://en.wikipedia.org/wiki/Boole%27s_expansion_theorem#Operations_with_cofactors>`_ or
        `Boolean derivative <https://en.wikipedia.org/wiki/Boolean_differential_calculus>`_.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (Self): Set of variables represented as conjunction thereof.
                Must belong to the same manager as ``self``.

        Returns:
            Self: ∃! vars: self

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def apply_forall(self, /, op: BooleanOperator, rhs: Self, vars: Self) -> Self:
        """Combined application of ``op`` and :meth:`forall()`.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            op (BooleanOperator): Binary Boolean operator to apply to ``self``
                and ``rhs``
            rhs (Self): Right-hand side of the operator. Must belong to the same
                manager as ``self``.
            vars (Self): Set of variables to quantify over. Represented as
                conjunction of variables. Must belong to the same manager as
                ``self``.

        Returns:
            Self: ``∀ vars. self <op> rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def apply_exists(self, /, op: BooleanOperator, rhs: Self, vars: Self) -> Self:
        """Combined application of ``op`` and :meth:`exists()`.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            op (BooleanOperator): Binary Boolean operator to apply to ``self``
                and ``rhs``
            rhs (Self): Right-hand side of the operator. Must belong to the same
                manager as ``self``.
            vars (Self): Set of variables to quantify over. Represented as
                conjunction of variables. Must belong to the same manager as
                ``self``.

        Returns:
            Self: ``∃ vars. self <op> rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def apply_exist(self, /, op: BooleanOperator, rhs: Self, vars: Self) -> Self:
        """Deprecated alias for ``apply_exists()``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            op (BooleanOperator): Binary Boolean operator to apply to ``self``
                and ``rhs``
            rhs (Self): Right-hand side of the operator. Must belong to the same
                manager as ``self``.
            vars (Self): Set of variables to quantify over. Represented as
                conjunction of variables. Must belong to the same manager as
                ``self``.

        Returns:
            Self: ``∃ vars. self <op> rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def apply_unique(self, /, op: BooleanOperator, rhs: Self, vars: Self) -> Self:
        """Combined application of ``op`` and :meth:`unique()`.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            op (BooleanOperator): Binary Boolean operator to apply to ``self``
                and ``rhs``
            rhs (Self): Right-hand side of the operator. Must belong to the same
                manager as ``self``.
            vars (Self): Set of variables to quantify over. Represented as
                conjunction of variables. Must belong to the same manager as
                ``self``.

        Returns:
            Self: ``∃! vars. self <op> rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def node_count(self, /) -> int:
        """Get the number of descendant nodes.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            int: The count of descendant nodes including the node referenced by
            ``self`` and terminal nodes.
        """

    def satisfiable(self, /) -> bool:
        """Check for satisfiability.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            bool: Whether the Boolean function has at least one satisfying
                assignment
        """

    def valid(self, /) -> bool:
        """Check for validity.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            bool: Whether all assignments satisfy the Boolean function
        """

    def sat_count(self, /, vars: int) -> int:
        """Count the number of satisfying assignments.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (int): Assume that the function's domain has this many
                variables.

        Returns:
            int: The exact number of satisfying assignments
        """

    def sat_count_float(self, /, vars: int) -> float:
        """Count the number of satisfying assignments.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (int): Assume that the function's domain has this many
                variables.

        Returns:
            float: (An approximation of) the number of satisfying assignments
        """

    def pick_cube(self, /) -> list[bool | None] | None:
        """Pick a satisfying assignment.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            list[bool | None] | None: The satisfying assignment where the i-th
            value means that the i-th variable is false, true, or "don't care,"
            respectively, or ``None`` if ``self`` is unsatisfiable
        """

    def pick_cube_dd(self, /) -> Self:
        """Pick a satisfying assignment, represented as decision diagram.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            Self: The satisfying assignment as decision diagram, or ``⊥`` if
            ``self`` is unsatisfiable
        """

    def pick_cube_dd_set(self, /, literal_set: Self) -> Self:
        """Pick a satisfying assignment as DD, with choices as of ``literal_set``.

        ``literal_set`` is a conjunction of literals. Whenever there is a choice
        for a variable, it will be set to true if the variable has a positive
        occurrence in ``literal_set``, and set to false if it occurs negated in
        ``literal_set``. If the variable does not occur in ``literal_set``, then
        it will be left as don't care if possible, otherwise an arbitrary (not
        necessarily random) choice will be performed.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            literal_set (Self): Conjunction of literals to determine the choice
                for variables

        Returns:
            Self: The satisfying assignment as decision diagram, or ``⊥`` if
            ``self`` is unsatisfiable

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def eval(self, /, args: Iterable[tuple[Self, bool]]) -> bool:
        """Evaluate this Boolean function with arguments ``args``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            args (Iterable[tuple[Self, bool]]): ``(variable, value)`` pairs.
                Missing variables are assumed to be false. However, note that
                the arguments may also determine the domain, e.g., in case of
                ZBDDs. If variables are given multiple times, the last value
                counts. Besides that, the order is irrelevant.
                All variable handles must belong to the same manager as ``self``
                and must reference inner nodes.

        Returns:
            bool: The result of applying the function ``self`` to ``args``
        """

    def __eq__(self, /, rhs: object) -> bool: ...
    def __ne__(self, /, rhs: object) -> bool: ...
    def __le__(self, /, rhs: Self) -> bool: ...
    def __lt__(self, /, rhs: Self) -> bool: ...
    def __ge__(self, /, rhs: Self) -> bool: ...
    def __gt__(self, /, rhs: Self) -> bool: ...
    def __hash__(self, /) -> int: ...

@final
class BCDDManager:
    r"""Manager for binary decision diagrams with complement edges.

    Implements: :class:`~oxidd.protocols.BooleanFunctionManager`\
    [:class:`BCDDFunction`]
    """

    @classmethod
    def __new__(
        cls, /, inner_node_capacity: int, apply_cache_capacity: int, threads: int
    ) -> BCDDManager:
        """Create a new manager.

        Args:
            inner_node_capacity (int): Maximum count of inner nodes
            apply_cache_capacity (int): Maximum count of apply cache entries
            threads (int): Worker thread count for the internal thread pool

        Returns:
            BCDDManager: The new manager
        """

    def new_var(self, /) -> BCDDFunction:
        """Get a fresh variable, adding a new level to a decision diagram.

        Acquires the manager's lock for exclusive access.

        Returns:
            BCDDFunction: A Boolean function that is true if and only if the
                variable is true

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def true(self, /) -> BCDDFunction:
        """Get the constant true Boolean function ``⊤``.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            BCDDFunction: The constant true Boolean function ``⊤``
        """

    def false(self, /) -> BCDDFunction:
        """Get the constant false Boolean function ``⊥``.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            BCDDFunction: The constant false Boolean function ``⊥``
        """

    def num_inner_nodes(self, /) -> int:
        """Get the number of inner nodes.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            int: The number of inner nodes stored in this manager
        """

    def dump_all_dot_file(
        self,
        /,
        path: str | PathLike[str],
        functions: Iterable[tuple[BCDDFunction, str]] = [],
        variables: Iterable[tuple[BCDDFunction, str]] = [],
    ) -> None:
        """Dump the entire decision diagram in this manager as Graphviz DOT code.

        The output may also include nodes that are not reachable from
        ``functions``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            path (str | PathLike[str]): Path of the output file. If a file at
                ``path`` exists, it will be truncated, otherwise a new one will
                be created.
            functions (Iterable[tuple[BCDDFunction, str]]): Optional names for
                BCDD functions
            variables (Iterable[tuple[BCDDFunction, str]]): Optional names for
                variables

        Returns:
            None
        """

    def __eq__(self, /, rhs: object) -> bool: ...
    def __ne__(self, /, rhs: object) -> bool: ...
    def __hash__(self, /) -> int: ...

@final
class BCDDSubstitution:
    """Substitution mapping variables to replacement functions.

    Implements: :class:`~oxidd.protocols.FunctionSubst`
    """

    @classmethod
    def __new__(
        cls, /, pairs: Iterable[tuple[BCDDFunction, BCDDFunction]]
    ) -> BCDDSubstitution:
        """Create a new substitution object for BCDDs.

        See :meth:`BCDDFunction.make_substitution()` fore more details.

        Args:
            pairs (Iterable[tuple[BCDDFunction, BCDDFunction]]):
                ``(variable, replacement)`` pairs, where all variables are
                distinct. The order of the pairs is irrelevant.

        Returns:
            BCDDSubstitution: The new substitution
        """

@final
class BCDDFunction:
    r"""Boolean function as binary decision diagram with complement edges (BCDD).

    Implements:
        :class:`~oxidd.protocols.BooleanFunctionQuant`,
        :class:`~oxidd.protocols.FunctionSubst`\ [:class:`BCDDSubstitution`],
        :class:`~oxidd.protocols.HasLevel`

    All operations constructing BCDDs may throw a
    :exc:`~oxidd.util.DDMemoryError` in case they run out of memory.

    Note that comparisons like ``f <= g`` are based on an arbitrary total order
    and not related to logical implications. See the
    :meth:`Function <oxidd.protocols.Function.__lt__>` protocol for more
    details.
    """

    @classmethod
    def __new__(cls, _: Never) -> Self:
        """Private constructor."""

    @property
    def manager(self, /) -> BCDDManager:
        """BCDDManager: The associated manager."""

    def cofactors(self, /) -> tuple[Self, Self] | None:
        r"""Get the cofactors ``(f_true, f_false)`` of ``self``.

        Let f(x₀, …, xₙ) be represented by ``self``, where x₀ is (currently) the
        top-most variable. Then f\ :sub:`true`\ (x₁, …, xₙ) = f(⊤, x₁, …, xₙ)
        and f\ :sub:`false`\ (x₁, …, xₙ) = f(⊥, x₁, …, xₙ).

        Structurally, the cofactors are simply the children in case with edge
        tags adjusted accordingly.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            tuple[Self, Self] | None: The cofactors ``(f_true, f_false)``, or
                ``None`` if ``self`` references a terminal node.

        See Also:
            :meth:`cofactor_true`, :meth:`cofactor_false` if you only need one
            of the cofactors.
        """

    def cofactor_true(self, /) -> Self | None:
        """Get the cofactor ``f_true`` of ``self``.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            Self | None: The cofactor ``f_true``, or ``None`` if ``self``
                references a terminal node.

        See Also:
            :meth:`cofactors`, also for a more detailed description
        """

    def cofactor_false(self, /) -> Self | None:
        """Get the cofactor ``f_false`` of ``self``.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            Self | None: The cofactor ``f_false``, or ``None`` if ``self``
                references a terminal node.

        See Also:
            :meth:`cofactors`, also for a more detailed description
        """

    def level(self, /) -> int | None:
        """Get the level of the underlying node.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            int | None: The level, or ``None`` if the node is a terminal
        """

    def __invert__(self, /) -> Self:
        """Compute the negation ``¬self``.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            Self: ``¬self``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __and__(self, rhs: Self, /) -> Self:
        """Compute the conjunction ``self ∧ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ∧ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __or__(self, rhs: Self, /) -> Self:
        """Compute the disjunction ``self ∨ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ∨ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __xor__(self, rhs: Self, /) -> Self:
        """Compute the exclusive disjunction ``self ⊕ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ⊕ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def nand(self, rhs: Self, /) -> Self:
        """Compute the negated conjunction ``self ⊼ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ⊼ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def nor(self, rhs: Self, /) -> Self:
        """Compute the negated disjunction ``self ⊽ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ⊽ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def equiv(self, rhs: Self, /) -> Self:
        """Compute the equivalence ``self ↔ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ↔ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def imp(self, rhs: Self, /) -> Self:
        """Compute the implication ``self → rhs`` (or ``f ≤ g``).

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self → rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def imp_strict(self, rhs: Self, /) -> Self:
        """Compute the strict implication ``self < rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self < rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def ite(self, /, t: Self, e: Self) -> Self:
        """Compute the BCDD for the conditional ``t if self else e``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            t (Self): Then-case; must belong to the same manager as ``self``
            e (Self): Else-case; must belong to the same manager as ``self``

        Returns:
            Self: The Boolean function ``f(v: 𝔹ⁿ) = t(v) if self(v) else e(v)``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    @classmethod
    def make_substitution(cls, pairs: Iterable[tuple[Self, Self]], /) -> Self:
        """Create a new substitution object from pairs ``(var, replacement)``.

        The intent behind substitution objects is to optimize the case where the
        same substitution is applied multiple times. We would like to re-use
        apply cache entries across these operations, and therefore, we need a
        compact identifier for the substitution. This identifier is provided by
        the returned substitution object.

        Args:
            pairs (Iterable[tuple[Self, Self]]): ``(variable, replacement)``
                pairs, where all variables are distinct. The order of the pairs
                is irrelevant.

        Returns:
            Self: The substitution to be used with :meth:`substitute()`
        """

    def substitute(self, substitution: BCDDSubstitution, /) -> Self:
        """Substitute variables in ``self`` according to ``substitution``.

        The substitution is performed in a parallel fashion, e.g.:
        ``(¬x ∧ ¬y)[x ↦ ¬x ∧ ¬y, y ↦ ⊥] = ¬(¬x ∧ ¬y) ∧ ¬⊥ = x ∨ y``

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            substitution (BCDDSubstitution): A substitution object created using
                :meth:`make_substitution()`. All contained DD functions must
                belong to the same manager as ``self``.

        Returns:
            Self: ``self`` with variables substituted
        """

    def forall(self, /, vars: Self) -> Self:
        """Compute the universal quantification over ``vars``.

        This operation removes all occurrences of variables in ``vars`` by
        universal quantification. Universal quantification ∀x. f(…, x, …) of a
        Boolean function f(…, x, …) over a single variable x is
        f(…, 0, …) ∧ f(…, 1, …).

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (Self): Set of variables represented as conjunction thereof.
                Must belong to the same manager as ``self``.

        Returns:
            Self: ∀ vars: self

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def exists(self, /, vars: Self) -> Self:
        """Compute the existential quantification over ``vars``.

        This operation removes all occurrences of variables in ``vars`` by
        existential quantification. Existential quantification ∃x. f(…, x, …) of
        a Boolean function f(…, x, …) over a single variable x is
        f(…, 0, …) ∨ f(…, 1, …).

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (Self): Set of variables represented as conjunction thereof.
                Must belong to the same manager as ``self``.

        Returns:
            Self: ∃ vars: self

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def exist(self, /, vars: Self) -> Self:
        """Deprecated alias for :meth:`exists()`.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (Self): Set of variables represented as conjunction thereof.
                Must belong to the same manager as ``self``.

        Returns:
            Self: ∃ vars: self

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def unique(self, /, vars: Self) -> Self:
        """Compute the unique quantification over ``vars``.

        This operation removes all occurrences of variables in ``vars`` by
        unique quantification. Unique quantification ∃!x. f(…, x, …) of a
        Boolean function f(…, x, …) over a single variable x is
        f(…, 0, …) ⊕ f(…, 1, …). Unique quantification is also known as the
        `Boolean difference <https://en.wikipedia.org/wiki/Boole%27s_expansion_theorem#Operations_with_cofactors>`_ or
        `Boolean derivative <https://en.wikipedia.org/wiki/Boolean_differential_calculus>`_.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (Self): Set of variables represented as conjunction thereof.
                Must belong to the same manager as ``self``.

        Returns:
            Self: ∃! vars: self

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def apply_forall(self, /, op: BooleanOperator, rhs: Self, vars: Self) -> Self:
        """Combined application of ``op`` and :meth:`forall()`.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            op (BooleanOperator): Binary Boolean operator to apply to ``self``
                and ``rhs``
            rhs (Self): Right-hand side of the operator. Must belong to the same
                manager as ``self``.
            vars (Self): Set of variables to quantify over. Represented as
                conjunction of variables. Must belong to the same manager as
                ``self``.

        Returns:
            Self: ``∀ vars. self <op> rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def apply_exists(self, /, op: BooleanOperator, rhs: Self, vars: Self) -> Self:
        """Combined application of ``op`` and :meth:`exists()`.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            op (BooleanOperator): Binary Boolean operator to apply to ``self``
                and ``rhs``
            rhs (Self): Right-hand side of the operator. Must belong to the same
                manager as ``self``.
            vars (Self): Set of variables to quantify over. Represented as
                conjunction of variables. Must belong to the same manager as
                ``self``.

        Returns:
            Self: ``∃ vars. self <op> rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def apply_exist(self, /, op: BooleanOperator, rhs: Self, vars: Self) -> Self:
        """Deprecated alias for :meth:`apply_exists()`.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            op (BooleanOperator): Binary Boolean operator to apply to ``self``
                and ``rhs``
            rhs (Self): Right-hand side of the operator. Must belong to the same
                manager as ``self``.
            vars (Self): Set of variables to quantify over. Represented as
                conjunction of variables. Must belong to the same manager as
                ``self``.

        Returns:
            Self: ``∃ vars. self <op> rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def apply_unique(self, /, op: BooleanOperator, rhs: Self, vars: Self) -> Self:
        """Combined application of ``op`` and :meth:`unique()`.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            op (BooleanOperator): Binary Boolean operator to apply to ``self``
                and ``rhs``
            rhs (Self): Right-hand side of the operator. Must belong to the same
                manager as ``self``.
            vars (Self): Set of variables to quantify over. Represented as
                conjunction of variables. Must belong to the same manager as
                ``self``.

        Returns:
            Self: ``∃! vars. self <op> rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def node_count(self, /) -> int:
        """Get the number of descendant nodes.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            int: The count of descendant nodes including the node referenced by
            ``self`` and terminal nodes.
        """

    def satisfiable(self, /) -> bool:
        """Check for satisfiability.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            bool: Whether the Boolean function has at least one satisfying
                assignment
        """

    def valid(self, /) -> bool:
        """Check for validity.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            bool: Whether all assignments satisfy the Boolean function
        """

    def sat_count(self, /, vars: int) -> int:
        """Count the number of satisfying assignments.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (int): Assume that the function's domain has this many
                variables.

        Returns:
            int: The exact number of satisfying assignments
        """

    def sat_count_float(self, /, vars: int) -> float:
        """Count the number of satisfying assignments.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (int): Assume that the function's domain has this many
                variables.

        Returns:
            float: (An approximation of) the number of satisfying assignments
        """

    def pick_cube(self, /) -> list[bool | None] | None:
        """Pick a satisfying assignment.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            list[bool | None] | None: The satisfying assignment where the i-th
            value means that the i-th variable is false, true, or "don't care,"
            respectively, or ``None`` if ``self`` is unsatisfiable
        """

    def pick_cube_dd(self, /) -> Self:
        """Pick a satisfying assignment, represented as decision diagram.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            Self: The satisfying assignment as decision diagram, or ``⊥`` if
            ``self`` is unsatisfiable
        """

    def pick_cube_dd_set(self, /, literal_set: Self) -> Self:
        """Pick a satisfying assignment as DD, with choices as of ``literal_set``.

        ``literal_set`` is a conjunction of literals. Whenever there is a choice
        for a variable, it will be set to true if the variable has a positive
        occurrence in ``literal_set``, and set to false if it occurs negated in
        ``literal_set``. If the variable does not occur in ``literal_set``, then
        it will be left as don't care if possible, otherwise an arbitrary (not
        necessarily random) choice will be performed.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            literal_set (Self): Conjunction of literals to determine the choice
                for variables

        Returns:
            Self: The satisfying assignment as decision diagram, or ``⊥`` if
            ``self`` is unsatisfiable

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def eval(self, /, args: Iterable[tuple[Self, bool]]) -> bool:
        """Evaluate this Boolean function with arguments ``args``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            args (Iterable[tuple[Self, bool]]): ``(variable, value)`` pairs.
                Missing variables are assumed to be false. However, note that
                the arguments may also determine the domain, e.g., in case of
                ZBDDs. If variables are given multiple times, the last value
                counts. Besides that, the order is irrelevant.
                All variable handles must belong to the same manager as ``self``
                and must reference inner nodes.

        Returns:
            bool: The result of applying the function ``self`` to ``args``
        """

    def __eq__(self, /, rhs: object) -> bool: ...
    def __ne__(self, /, rhs: object) -> bool: ...
    def __le__(self, /, rhs: Self) -> bool: ...
    def __lt__(self, /, rhs: Self) -> bool: ...
    def __ge__(self, /, rhs: Self) -> bool: ...
    def __gt__(self, /, rhs: Self) -> bool: ...
    def __hash__(self, /) -> int: ...

@final
class ZBDDManager:
    r"""Manager for zero-suppressed binary decision diagrams.

    Implements: :class:`~oxidd.protocols.BooleanFunctionManager`\
    [:class`ZBDDFunction`]
    """

    @classmethod
    def __new__(
        cls, /, inner_node_capacity: int, apply_cache_capacity: int, threads: int
    ) -> ZBDDManager:
        """Create a new manager.

        Args:
            inner_node_capacity (int): Maximum count of inner nodes
            apply_cache_capacity (int): Maximum count of apply cache entries
            threads (int): Worker thread count for the internal thread pool

        Returns:
            ZBDDManager: The new manager
        """

    def new_singleton(self, /) -> ZBDDFunction:
        """Get a fresh variable in the form of a singleton set.

        This adds a new level to a decision diagram. Note that if you interpret
        Boolean functions with respect to all variables, then the semantics
        change from f to f'(x₁, …, xₙ, xₙ₊₁) = f(x₁, …, xₙ) ∧ ¬xₙ₊₁. This is
        different compared to B(C)DDs where we have
        f'(x₁, …, xₙ, xₙ₊₁) = f(x₁, …, xₙ).

        Locking behavior: acquires the manager's lock for exclusive access.

        Returns:
            ZBDDFunction: The singleton set

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def new_var(self, /) -> ZBDDFunction:
        """Get a fresh variable, adding a new level to a decision diagram.

        Note that if you interpret Boolean functions with respect to all
        variables, then adding a level changes the semantics change from
        f to f'(x₁, …, xₙ, xₙ₊₁) = f(x₁, …, xₙ) ∧ ¬xₙ₊₁. This is different
        compared to B(C)DDs where we have f'(x₁, …, xₙ, xₙ₊₁) = f(x₁, …, xₙ).

        Locking behavior: acquires the manager's lock for exclusive access.

        Returns:
            ZBDDFunction: A Boolean function that is true if and only if the
                variable is true

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def empty(self, /) -> ZBDDFunction:
        """Get the ZBDD set ∅.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            ZBDDFunction: The set `∅` (or equivalently `⊥`)
        """

    def base(self, /) -> ZBDDFunction:
        """Get the ZBDD set {∅}.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            ZBDDFunction: The set `{∅}`
        """

    def true(self, /) -> ZBDDFunction:
        """Get the constant true Boolean function ``⊤``.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            ZBDDFunction: The constant true Boolean function ``⊤``
        """

    def false(self, /) -> ZBDDFunction:
        """Get the constant false Boolean function ``⊥``.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            ZBDDFunction: The constant false Boolean function ``⊥``
        """

    def num_inner_nodes(self, /) -> int:
        """Get the number of inner nodes.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            int: The number of inner nodes stored in this manager
        """

    def dump_all_dot_file(
        self,
        /,
        path: str | PathLike[str],
        functions: Iterable[tuple[ZBDDFunction, str]] = [],
        variables: Iterable[tuple[ZBDDFunction, str]] = [],
    ) -> None:
        """Dump the entire decision diagram in this manager as Graphviz DOT code.

        The output may also include nodes that are not reachable from
        ``functions``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            path (str | PathLike[str]): Path of the output file. If a file at
                ``path`` exists, it will be truncated, otherwise a new one will
                be created.
            functions (Iterable[tuple[ZBDDFunction, str]]): Optional names for
                ZBDD functions
            variables (Iterable[tuple[ZBDDFunction, str]]): Optional names for
                variables. The variables must be handles for the respective
                decision diagram levels, i.e., singleton sets.

        Returns:
            None
        """

    def __eq__(self, /, rhs: object) -> bool: ...
    def __ne__(self, /, rhs: object) -> bool: ...
    def __hash__(self, /) -> int: ...

@final
class ZBDDFunction:
    """Boolean function as zero-suppressed binary decision diagram (ZBDD).

    Implements:
        :class:`~oxidd.protocols.BooleanFunction`,
        :class:`~oxidd.protocols.HasLevel`

    All operations constructing ZBDDs may throw a
    :exc:`~oxidd.util.DDMemoryError` in case they run out of memory.

    Note that comparisons like ``f <= g`` are based on an arbitrary total order
    and not related to logical implications. See the
    :meth:`Function <oxidd.protocols.Function.__lt__>` protocol for more
    details.
    """

    @classmethod
    def __new__(cls, _: Never) -> Self:
        """Private constructor."""

    @property
    def manager(self, /) -> ZBDDManager:
        """ZBDDManager: The associated manager."""

    def cofactors(self, /) -> tuple[Self, Self] | None:
        r"""Get the cofactors ``(f_true, f_false)`` of ``self``.

        Let f(x₀, …, xₙ) be represented by ``self``, where x₀ is (currently) the
        top-most variable. Then f\ :sub:`true`\ (x₁, …, xₙ) = f(⊤, x₁, …, xₙ)
        and f\ :sub:`false`\ (x₁, …, xₙ) = f(⊥, x₁, …, xₙ).

        Note that the domain of f is 𝔹\ :sup:`n+1` while the domain of
        f\ :sub:`true` and f\ :sub:`false` is 𝔹\ :sup:`n`. This is irrelevant in
        case of BDDs and BCDDs, but not for ZBDDs: For instance, g(x₀) = x₀ and
        g'(x₀, x₁) = x₀ have the same representation as BDDs or BCDDs, but
        different representations as ZBDDs.

        Structurally, the cofactors are simply the children in case with edge
        tags adjusted accordingly.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            tuple[Self, Self] | None: The cofactors ``(f_true, f_false)``, or
                ``None`` if ``self`` references a terminal node.

        See Also:
            :meth:`cofactor_true`, :meth:`cofactor_false` if you only need one
            of the cofactors.
        """

    def cofactor_true(self, /) -> Self | None:
        """Get the cofactor ``f_true`` of ``self``.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            Self | None: The cofactor ``f_true``, or ``None`` if ``self``
                references a terminal node.

        See Also:
            :meth:`cofactors`, also for a more detailed description
        """

    def cofactor_false(self, /) -> Self | None:
        """Get the cofactor ``f_false`` of ``self``.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            Self | None: The cofactor ``f_false``, or ``None`` if ``self``
                references a terminal node.

        See Also:
            :meth:`cofactors`, also for a more detailed description
        """

    def level(self, /) -> int | None:
        """Get the level of the underlying node.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            int | None: The level, or ``None`` if the node is a terminal
        """

    def var_boolean_function(self, /) -> Self:
        """Get the Boolean function v for the singleton set {v}.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            Self: The Boolean function `v` as ZBDD

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __invert__(self, /) -> Self:
        """Compute the negation ``¬self``.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            Self: ``¬self``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __and__(self, rhs: Self, /) -> Self:
        """Compute the conjunction ``self ∧ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ∧ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __or__(self, rhs: Self, /) -> Self:
        """Compute the disjunction ``self ∨ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ∨ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __xor__(self, rhs: Self, /) -> Self:
        """Compute the exclusive disjunction ``self ⊕ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ⊕ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def __sub__(self, rhs: Self, /) -> Self:
        """Compute the set difference ``self ∖ rhs``.

        Locking behavior: acquires the manager's lock for exclusive access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ∖ rhs``, or equivalently ``rhs.strict_imp(self)``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def nand(self, rhs: Self, /) -> Self:
        """Compute the negated conjunction ``self ⊼ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ⊼ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def nor(self, rhs: Self, /) -> Self:
        """Compute the negated disjunction ``self ⊽ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ⊽ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def equiv(self, rhs: Self, /) -> Self:
        """Compute the equivalence ``self ↔ rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self ↔ rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def imp(self, rhs: Self, /) -> Self:
        """Compute the implication ``self → rhs`` (or ``f ≤ g``).

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self → rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def imp_strict(self, rhs: Self, /) -> Self:
        """Compute the strict implication ``self < rhs``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            rhs (Self): Right-hand side operand. Must belong to the same manager
                as ``self``

        Returns:
            Self: ``self < rhs``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def ite(self, /, t: Self, e: Self) -> Self:
        """Compute the ZBDD for the conditional ``t if self else e``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            t (Self): Then-case; must belong to the same manager as ``self``
            e (Self): Else-case; must belong to the same manager as ``self``

        Returns:
            Self: The Boolean function ``f(v: 𝔹ⁿ) = t(v) if self(v) else e(v)``

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def make_node(self, /, hi: Self, lo: Self) -> Self:
        """Create a node at ``self``'s level with edges ``hi`` and ``lo``.

        ``self`` must be a singleton set at a level above the top level of
        ``hi`` and ``lo``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            hi (Self): Edge for the case where the variable is true; must belong
                to the same manager as ``self``
            lo (Self): Edge for the case where the variable is false; must
                belong to the same manager as ``self``

        Returns:
            Self: The new ZBDD node

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def node_count(self, /) -> int:
        """Get the number of descendant nodes.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            int: The count of descendant nodes including the node referenced by
            ``self`` and terminal nodes.
        """

    def satisfiable(self, /) -> bool:
        """Check for satisfiability.

        Locking behavior: acquires the manager's lock for shared access.

        Time complexity: O(1)

        Returns:
            bool: Whether the Boolean function has at least one satisfying
                assignment
        """

    def valid(self, /) -> bool:
        """Check for validity.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            bool: Whether all assignments satisfy the Boolean function
        """

    def sat_count(self, /, vars: int) -> int:
        """Count the number of satisfying assignments.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (int): Assume that the function's domain has this many
                variables.

        Returns:
            int: The exact number of satisfying assignments
        """

    def sat_count_float(self, /, vars: int) -> float:
        """Count the number of satisfying assignments.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            vars (int): Assume that the function's domain has this many
                variables.

        Returns:
            float: (An approximation of) the number of satisfying assignments
        """

    def pick_cube(self, /) -> list[bool | None] | None:
        """Pick a satisfying assignment.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            list[bool | None] | None: The satisfying assignment where the i-th
            value means that the i-th variable is false, true, or "don't care,"
            respectively, or ``None`` if ``self`` is unsatisfiable
        """

    def pick_cube_dd(self, /) -> Self:
        """Pick a satisfying assignment, represented as decision diagram.

        Locking behavior: acquires the manager's lock for shared access.

        Returns:
            Self: The satisfying assignment as decision diagram, or ``⊥`` if
            ``self`` is unsatisfiable
        """

    def pick_cube_dd_set(self, /, literal_set: Self) -> Self:
        """Pick a satisfying assignment as DD, with choices as of ``literal_set``.

        ``literal_set`` is a conjunction of literals. Whenever there is a choice
        for a variable, it will be set to true if the variable has a positive
        occurrence in ``literal_set``, and set to false if it occurs negated in
        ``literal_set``. If the variable does not occur in ``literal_set``, then
        it will be left as don't care if possible, otherwise an arbitrary (not
        necessarily random) choice will be performed.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            literal_set (Self): Conjunction of literals to determine the choice
                for variables

        Returns:
            Self: The satisfying assignment as decision diagram, or ``⊥`` if
            ``self`` is unsatisfiable

        Raises:
            DDMemoryError: If the operation runs out of memory
        """

    def eval(self, /, args: Iterable[tuple[Self, bool]]) -> bool:
        """Evaluate this Boolean function with arguments ``args``.

        Locking behavior: acquires the manager's lock for shared access.

        Args:
            args (Iterable[tuple[Self, bool]]): ``(variable, value)`` pairs
                where variables must be handles for the respective decision
                diagram levels, i.e., singleton sets.
                Missing variables are assumed to be false. However, note that
                the arguments may also determine the domain, e.g., in case of
                ZBDDs. If variables are given multiple times, the last value
                counts. Besides that, the order is irrelevant.
                All variable handles must belong to the same manager as ``self``
                and must reference inner nodes.

        Returns:
            bool: The result of applying the function ``self`` to ``args``
        """

    def __eq__(self, /, rhs: object) -> bool: ...
    def __ne__(self, /, rhs: object) -> bool: ...
    def __le__(self, /, rhs: Self) -> bool: ...
    def __lt__(self, /, rhs: Self) -> bool: ...
    def __ge__(self, /, rhs: Self) -> bool: ...
    def __gt__(self, /, rhs: Self) -> bool: ...
    def __hash__(self, /) -> int: ...

class DDMemoryError(MemoryError):
    """Exception that is raised in case a DD operation runs out of memory."""

class BooleanOperator(enum.Enum):
    """Binary operators on Boolean functions."""

    AND = ...
    """Conjunction ``lhs ∧ rhs``"""
    OR = ...
    """Disjunction ``lhs ∨ rhs``"""
    XOR = ...
    """Exclusive disjunction ``lhs ⊕ rhs``"""
    EQUIV = ...
    """Equivalence ``lhs ↔ rhs``"""
    NAND = ...
    """Negated conjunction ``lhs ⊼ rhs``"""
    NOR = ...
    """Negated disjunction ``lhs ⊽ rhs``"""
    IMP = ...
    """Implication ``lhs → rhs`` (or `lhs ≤ rhs)`"""
    IMP_STRICT = ...
    """Strict implication ``lhs < rhs``"""
