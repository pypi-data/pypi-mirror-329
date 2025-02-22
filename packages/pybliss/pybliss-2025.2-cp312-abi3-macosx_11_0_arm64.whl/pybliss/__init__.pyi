from collections.abc import Callable
import enum
from typing import Annotated, overload

from numpy.typing import ArrayLike


class BigNum:
    """
    A wrapper class for non-negative big integers.

    .. automethod:: __init__
    .. automethod:: assign
    .. automethod:: multiply
    .. automethod:: print_to_file
    .. automethod:: __str__
    """

    def __init__(self) -> None: ...

    def assign(self, arg: int, /) -> None: ...

    def multiply(self, arg: int, /) -> None: ...

    def print_to_file(self, arg: object, /) -> None: ...

    def __str__(self) -> str: ...

class Digraph:
    """
    Vertex-colored graph.

      .. automethod:: __init__
      .. automethod:: set_verbose_level
      .. automethod:: set_verbose_file
      .. automethod:: add_vertex
      .. automethod:: add_edge
      .. automethod:: get_color
      .. automethod:: change_color
      .. automethod:: set_failure_recording
      .. automethod:: set_component_recursion
      .. autoattribute:: nvertices
      .. automethod:: permute
      .. automethod:: is_automorphism
      .. automethod:: find_automorphisms
      .. automethod:: get_permutation_to_canonical_form
      .. automethod:: write_dimacs
      .. automethod:: to_dimacs
      .. automethod:: write_dot
      .. automethod:: to_dot
      .. automethod:: show_dot
      .. automethod:: from_dimacs
      .. automethod:: copy
      .. automethod:: cmp
      .. automethod:: __eq__
      .. automethod:: set_long_prune_activity
      .. automethod:: set_splitting_heuristic

    .. note::

      - :class:`Graph` represents an undirected graph, while,
      - :class:`Digraph` represents a directed graph.
    """

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: int, /) -> None: ...

    def set_verbose_level(self, level: int) -> None:
        """
        Set the verbose output level for the algorithms
        :arg level: The level of verbose output, 0 means no verbose output.
        """

    def set_verbose_file(self, fp: object) -> None:
        """
        Set the file stream for verbose output.

        :param file_obj: The file object to write the output to. If None, writing to the file is disabled.
        """

    def add_vertex(self, color: int = 0) -> int:
        """Add a new vertex with color *color* and return its new index."""

    def add_edge(self, source: int, target: int) -> None:
        """Add an edge from *source* to *target*."""

    def get_color(self, v: int) -> int:
        """Returns the color of the vertex *v*"""

    def change_color(self, v: int, c: int) -> None:
        """Change the color of vertex *v* to *c*."""

    def set_failure_recording(self, active: bool) -> None:
        """
        Activate / deactivate failure recording

        :arg active:If true, activate failure recording, deactivate otherwise.
        """

    def set_component_recursion(self, active: bool) -> None:
        """
        Activate/deactivate component recursion. The choice affects the computed canonical labelings; therefore, if you want to compare whether two graphs are isomorphic by computing and comparing (for equality) their canonical versions, be sure to use the same choice for both graphs. May not be called during the search, i.e. from an automorphism reporting hook function.

        :arg active:  If true, activate component recursion, deactivate otherwise.
        """

    @property
    def nvertices(self) -> int:
        """Return the number of vertices in the graph."""

    def permute(self, perm: Annotated[ArrayLike, dict(dtype='uint32', shape=(None))]) -> Digraph:
        """
        Return a new graph that is the result of applying the permutation *perm* to this graph. This graph is not modified. *perm* must contain N=this.get_nof_vertices() elements and be a bijection on {0,1,...,N-1}, otherwise the result is undefined.
        """

    def is_automorphism(self, perm: Annotated[ArrayLike, dict(dtype='uint32', shape=(None))]) -> bool:
        """
        Return true only if *perm* is an automorphism of this graph. *perm* must contain N=this.get_nof_vertices() elements and be a bijection on {0,1,...,N-1}, otherwise the result is undefined.
        """

    def find_automorphisms(self, stats: Stats, report: Callable[[int, Annotated[ArrayLike, dict(dtype='uint32', shape=(None), order='C', writable=False)]], None] | None = None, terminate: Callable[[], bool] | None = None) -> None:
        """
        Find a set of generators for the automorphism group of the graph. The function *report* (if not None) is called each time a new generator for the automorphism group is found. The first argument *n* for the function is the length of the automorphism (equal to get_nof_vertices()), and the second argument *aut* is the automorphism (a bijection on {0,...,nvertices-1}). *aut* is a read-only :class:`numpy.ndarray`. Additionally *aut*'s entries are invalidated across calls to *terminate*. Caller must copy *aut* if long-term usage is intended. Do not call any member functions from the *report* function.

        The search statistics are copied in *stats*.

        If the *terminate* function argument is given, it is called in each search tree node: if the function returns true, then the search is terminated and thus not all the automorphisms may have been generated. The *terminate* function may be used to limit the time spent in bliss in case the graph is too difficult under the available time constraints. If used, keep the function simple to evaluate so that it does not consume too much time.
        """

    def get_permutation_to_canonical_form(self, stats: Stats, report: Callable[[int, Annotated[ArrayLike, dict(dtype='uint32', shape=(None), order='C', writable=False)]], None] | None = None, terminate: Callable[[], bool] | None = None) -> object:
        """
        Returns `P`, a :class:`numpy.ndarray` on {0, ..., nvertices-1}. Applying the 'permutation `P` to this graph results in this graph's canonical graph. The function *report* (if not None) is called each time a new  generator for the automorphism group is found. The first argument  *n* for the function is the length of the automorphism (equal to  get_nof_vertices()), and the second argument *aut* is the  automorphism (a bijection on {0,...,nvertices-1}). *aut* is a read-only :class:`numpy.ndarray`. Additionally *aut*'s entries are invalidated across calls to *terminate*. Caller must copy *aut* if long-term usage is intended. Do not call any  member functions from the *report* function.

        The search statistics are copied in *stats*.

        If the *terminate* function argument is given, it is called in each search tree node: if the function returns true, then the search is terminated and thus not all the automorphisms may have been generated. The *terminate* function may be used to limit the time spent in bliss in case the graph is too difficult under the available time constraints. If used, keep the function simple to evaluate so that it does not consume too much time.

        This wraps the method canonical_form from the C++-API.
        """

    @staticmethod
    def from_dimacs(fp: object) -> Digraph:
        """
        Return a graph corresponding to DIMACS-formatted graph present in *fp*. See the `bliss website <https://users.aalto.fi/tjunttil/bliss>` for the definition of the file format. Note that in the DIMACS file the vertices are numbered from 1 to N while in this API they are from 0 to N-1. Thus the vertex n in the file corresponds to the vertex n-1 in the API.

        :arg fp: The file stream from where the graph is to be read.
        """

    def write_dimacs(self, fp: object) -> None:
        """
        Write the graph to *fp* in a variant of the DIMACS format. See the `bliss website <https://users.aalto.fi/tjunttil/bliss>` for the definition of the file format. Note that in the DIMACS file the vertices are numbered from 1 to N while in this API they are from 0 to N-1. Thus the vertex n in the file corresponds to the vertex n-1 in the API.

        :arg fp: The file stream where the graph is to be written.
        """

    def to_dimacs(self) -> str:
        """Returns a :class:`str` corresponding to DIMACS format of the graph."""

    def write_dot(self, fp: object) -> None:
        """
        Write the graph to *fp* in the graphviz format.

        :arg fp: The file stream where the graph is to be written.
        """

    def copy(self) -> Digraph:
        """Returns a copy of this graph."""

    def cmp(self, other: Digraph) -> int:
        """
        Compare this graph to *other* in a total order on graphs. Returns 0 if graphs are equal, -1 if this graph is "smaller than" the other, and 1 if this graph is "greater than" *other*.
        """

    def __eq__(self, other: Digraph) -> bool:
        """
        Returns True iff this graph is identical to *other*.
        The check is perform in :math:`O(E)`, where :math:`E` is the number
        of edges in this graph.
        """

    def to_dot(self) -> str:
        """Returns a :class:`str` corresponding to graphviz format of the graph."""

    def show_dot(self, output_to: object | None = None) -> None:
        """
        Visualize the graph.

        :arg output_to:  Passed on to :func:`pytools.graphviz.show_dot` unmodified.
        """

    def __hash__(self) -> int: ...

    def set_long_prune_activity(self, active: bool) -> None:
        """
        Disable/enable the long prune method. The choice affects the computed canonical labelings. Therefore, if you want to compare whether two graphs are isomorphic by computing and comparing (for equality) their canonical versions, be sure to use the same choice for both graphs. May not be called during the search, i.e. from an automorphism reporting hook function. *active*  if true, activate long prune, deactivate otherwise
        """

    def set_splitting_heuristic(self, shs: Digraph.SplittingHeuristic) -> None:
        """
        Set the splitting heuristic used by the automorphism and canonical labeling algorithm. The selected splitting heuristics affects the computed canonical labelings. Therefore, if you want to compare whether two graphs are isomorphic by computing and comparing (for equality) their canonical versions, be sure to use the same splitting heuristics for both graphs.
        """

    class SplittingHeuristic(enum.Enum):
        """
        Enum defining the splitting heuristics for graph canonicalization.

        .. attribute:: shs_f

          First non-unit cell. Very fast but may result in large search
          spaces on difficult graphs. Use for large but easy graphs.

        .. attribute:: shs_fs

          First smallest non-unit cell. Fast, should usually produce smaller
          search spaces than shs_f.

        .. attribute:: shs_fl

          First largest non-unit cell. Fast, should usually produce smaller
          search spaces than shs_f.

        .. attribute:: shs_fm

          First maximally non-trivially connected non-unit cell. Not so
          fast, should usually produce smaller search spaces than shs_f,
          shs_fs, and shs_fl.

        .. attribute:: shs_fsm

          First smallest maximally non-trivially connected non-unit cell.
          Not so fast, should usually produce smaller search spaces than
          shs_f, shs_fs, and shs_fl.

        .. attribute:: shs_flm

          First largest maximally non-trivially connected non-unit cell. Not
          so fast, should usually produce smaller search spaces than shs_f,
          shs_fs, and shs_fl.
        """

        shs_f = 0

        shs_fs = 1

        shs_fl = 2

        shs_fm = 3

        shs_fsm = 4

        shs_flm = 5

    shs_f: Digraph.SplittingHeuristic = Digraph.SplittingHeuristic.shs_f

    shs_fs: Digraph.SplittingHeuristic = Digraph.SplittingHeuristic.shs_fs

    shs_fl: Digraph.SplittingHeuristic = Digraph.SplittingHeuristic.shs_fl

    shs_fm: Digraph.SplittingHeuristic = Digraph.SplittingHeuristic.shs_fm

    shs_fsm: Digraph.SplittingHeuristic = Digraph.SplittingHeuristic.shs_fsm

    shs_flm: Digraph.SplittingHeuristic = Digraph.SplittingHeuristic.shs_flm

class Graph:
    """
    Vertex-colored graph.

      .. automethod:: __init__
      .. automethod:: set_verbose_level
      .. automethod:: set_verbose_file
      .. automethod:: add_vertex
      .. automethod:: add_edge
      .. automethod:: get_color
      .. automethod:: change_color
      .. automethod:: set_failure_recording
      .. automethod:: set_component_recursion
      .. autoattribute:: nvertices
      .. automethod:: permute
      .. automethod:: is_automorphism
      .. automethod:: find_automorphisms
      .. automethod:: get_permutation_to_canonical_form
      .. automethod:: write_dimacs
      .. automethod:: to_dimacs
      .. automethod:: write_dot
      .. automethod:: to_dot
      .. automethod:: show_dot
      .. automethod:: from_dimacs
      .. automethod:: copy
      .. automethod:: cmp
      .. automethod:: __eq__
      .. automethod:: set_long_prune_activity
      .. automethod:: set_splitting_heuristic

    .. note::

      - :class:`Graph` represents an undirected graph, while,
      - :class:`Digraph` represents a directed graph.
    """

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: int, /) -> None: ...

    def set_verbose_level(self, level: int) -> None:
        """
        Set the verbose output level for the algorithms
        :arg level: The level of verbose output, 0 means no verbose output.
        """

    def set_verbose_file(self, fp: object) -> None:
        """
        Set the file stream for verbose output.

        :param file_obj: The file object to write the output to. If None, writing to the file is disabled.
        """

    def add_vertex(self, color: int = 0) -> int:
        """Add a new vertex with color *color* and return its new index."""

    def add_edge(self, v1: int, v2: int) -> None:
        """Add an edge between *v1* and *v2*."""

    def get_color(self, v: int) -> int:
        """Returns the color of the vertex *v*"""

    def change_color(self, v: int, c: int) -> None:
        """Change the color of vertex *v* to *c*."""

    def set_failure_recording(self, active: bool) -> None:
        """
        Activate / deactivate failure recording

        :arg active:If true, activate failure recording, deactivate otherwise.
        """

    def set_component_recursion(self, active: bool) -> None:
        """
        Activate/deactivate component recursion. The choice affects the computed canonical labelings; therefore, if you want to compare whether two graphs are isomorphic by computing and comparing (for equality) their canonical versions, be sure to use the same choice for both graphs. May not be called during the search, i.e. from an automorphism reporting hook function.

        :arg active:  If true, activate component recursion, deactivate otherwise.
        """

    @property
    def nvertices(self) -> int:
        """Return the number of vertices in the graph."""

    def permute(self, perm: Annotated[ArrayLike, dict(dtype='uint32', shape=(None))]) -> Graph:
        """
        Return a new graph that is the result of applying the permutation *perm* to this graph. This graph is not modified. *perm* must contain N=this.get_nof_vertices() elements and be a bijection on {0,1,...,N-1}, otherwise the result is undefined.
        """

    def is_automorphism(self, perm: Annotated[ArrayLike, dict(dtype='uint32', shape=(None))]) -> bool:
        """
        Return true only if *perm* is an automorphism of this graph. *perm* must contain N=this.get_nof_vertices() elements and be a bijection on {0,1,...,N-1}, otherwise the result is undefined.
        """

    def find_automorphisms(self, stats: Stats, report: Callable[[int, Annotated[ArrayLike, dict(dtype='uint32', shape=(None), order='C', writable=False)]], None] | None = None, terminate: Callable[[], bool] | None = None) -> None:
        """
        Find a set of generators for the automorphism group of the graph. The function *report* (if not None) is called each time a new generator for the automorphism group is found. The first argument *n* for the function is the length of the automorphism (equal to get_nof_vertices()), and the second argument *aut* is the automorphism (a bijection on {0,...,nvertices-1}). *aut* is a read-only :class:`numpy.ndarray`. Additionally *aut*'s entries are invalidated across calls to *terminate*. Caller must copy *aut* if long-term usage is intended. Do not call any member functions from the *report* function.

        The search statistics are copied in *stats*.

        If the *terminate* function argument is given, it is called in each search tree node: if the function returns true, then the search is terminated and thus not all the automorphisms may have been generated. The *terminate* function may be used to limit the time spent in bliss in case the graph is too difficult under the available time constraints. If used, keep the function simple to evaluate so that it does not consume too much time.
        """

    def get_permutation_to_canonical_form(self, stats: Stats, report: Callable[[int, Annotated[ArrayLike, dict(dtype='uint32', shape=(None), order='C', writable=False)]], None] | None = None, terminate: Callable[[], bool] | None = None) -> object:
        """
        Returns `P`, a :class:`numpy.ndarray` on {0, ..., nvertices-1}. Applying the 'permutation `P` to this graph results in this graph's canonical graph. The function *report* (if not None) is called each time a new  generator for the automorphism group is found. The first argument  *n* for the function is the length of the automorphism (equal to  get_nof_vertices()), and the second argument *aut* is the  automorphism (a bijection on {0,...,nvertices-1}). *aut* is a read-only :class:`numpy.ndarray`. Additionally *aut*'s entries are invalidated across calls to *terminate*. Caller must copy *aut* if long-term usage is intended. Do not call any  member functions from the *report* function.

        The search statistics are copied in *stats*.

        If the *terminate* function argument is given, it is called in each search tree node: if the function returns true, then the search is terminated and thus not all the automorphisms may have been generated. The *terminate* function may be used to limit the time spent in bliss in case the graph is too difficult under the available time constraints. If used, keep the function simple to evaluate so that it does not consume too much time.

        This wraps the method canonical_form from the C++-API.
        """

    @staticmethod
    def from_dimacs(fp: object) -> Graph:
        """
        Return a graph corresponding to DIMACS-formatted graph present in *fp*. See the `bliss website <https://users.aalto.fi/tjunttil/bliss>` for the definition of the file format. Note that in the DIMACS file the vertices are numbered from 1 to N while in this API they are from 0 to N-1. Thus the vertex n in the file corresponds to the vertex n-1 in the API.

        :arg fp: The file stream from where the graph is to be read.
        """

    def write_dimacs(self, fp: object) -> None:
        """
        Write the graph to *fp* in a variant of the DIMACS format. See the `bliss website <https://users.aalto.fi/tjunttil/bliss>` for the definition of the file format. Note that in the DIMACS file the vertices are numbered from 1 to N while in this API they are from 0 to N-1. Thus the vertex n in the file corresponds to the vertex n-1 in the API.

        :arg fp: The file stream where the graph is to be written.
        """

    def to_dimacs(self) -> str:
        """Returns a :class:`str` corresponding to DIMACS format of the graph."""

    def write_dot(self, fp: object) -> None:
        """
        Write the graph to *fp* in the graphviz format.

        :arg fp: The file stream where the graph is to be written.
        """

    def copy(self) -> Graph:
        """Returns a copy of this graph."""

    def cmp(self, other: Graph) -> int:
        """
        Compare this graph to *other* in a total order on graphs. Returns 0 if graphs are equal, -1 if this graph is "smaller than" the other, and 1 if this graph is "greater than" *other*.
        """

    def __eq__(self, other: Graph) -> bool:
        """
        Returns True iff this graph is identical to *other*.
        The check is perform in :math:`O(E)`, where :math:`E` is the number
        of edges in this graph.
        """

    def to_dot(self) -> str:
        """Returns a :class:`str` corresponding to graphviz format of the graph."""

    def show_dot(self, output_to: object | None = None) -> None:
        """
        Visualize the graph.

        :arg output_to:  Passed on to :func:`pytools.graphviz.show_dot` unmodified.
        """

    def __hash__(self) -> int: ...

    def set_long_prune_activity(self, active: bool) -> None:
        """
        Disable/enable the long prune method. The choice affects the computed canonical labelings. Therefore, if you want to compare whether two graphs are isomorphic by computing and comparing (for equality) their canonical versions, be sure to use the same choice for both graphs. May not be called during the search, i.e. from an automorphism reporting hook function. *active*  if true, activate long prune, deactivate otherwise
        """

    def set_splitting_heuristic(self, shs: Graph.SplittingHeuristic) -> None:
        """
        Set the splitting heuristic used by the automorphism and canonical labeling algorithm. The selected splitting heuristics affects the computed canonical labelings. Therefore, if you want to compare whether two graphs are isomorphic by computing and comparing (for equality) their canonical versions, be sure to use the same splitting heuristics for both graphs.
        """

    class SplittingHeuristic(enum.Enum):
        """
        Enum defining the splitting heuristics for graph canonicalization.

        .. attribute:: shs_f

          First non-unit cell. Very fast but may result in large search
          spaces on difficult graphs. Use for large but easy graphs.

        .. attribute:: shs_fs

          First smallest non-unit cell. Fast, should usually produce smaller
          search spaces than shs_f.

        .. attribute:: shs_fl

          First largest non-unit cell. Fast, should usually produce smaller
          search spaces than shs_f.

        .. attribute:: shs_fm

          First maximally non-trivially connected non-unit cell. Not so
          fast, should usually produce smaller search spaces than shs_f,
          shs_fs, and shs_fl.

        .. attribute:: shs_fsm

          First smallest maximally non-trivially connected non-unit cell.
          Not so fast, should usually produce smaller search spaces than
          shs_f, shs_fs, and shs_fl.

        .. attribute:: shs_flm

          First largest maximally non-trivially connected non-unit cell. Not
          so fast, should usually produce smaller search spaces than shs_f,
          shs_fs, and shs_fl.
        """

        shs_f = 0

        shs_fs = 1

        shs_fl = 2

        shs_fm = 3

        shs_fsm = 4

        shs_flm = 5

    shs_f: Graph.SplittingHeuristic = Graph.SplittingHeuristic.shs_f

    shs_fs: Graph.SplittingHeuristic = Graph.SplittingHeuristic.shs_fs

    shs_fl: Graph.SplittingHeuristic = Graph.SplittingHeuristic.shs_fl

    shs_fm: Graph.SplittingHeuristic = Graph.SplittingHeuristic.shs_fm

    shs_fsm: Graph.SplittingHeuristic = Graph.SplittingHeuristic.shs_fsm

    shs_flm: Graph.SplittingHeuristic = Graph.SplittingHeuristic.shs_flm

class Stats:
    """
    Records statistics returned by the search algorithms.

    .. automethod:: __init__
    .. automethod:: print_to_file
    .. autoattribute:: group_size
    .. autoattribute:: group_size_as_bignum
    .. autoattribute:: group_size_approx
    .. autoattribute:: n_nodes
    .. autoattribute:: n_leaf_nodes
    .. autoattribute:: n_bad_nodes
    .. autoattribute:: n_canupdates
    .. autoattribute:: n_generators
    .. autoattribute:: max_level
    .. automethod:: __str__
    """

    def __init__(self) -> None: ...

    def print_to_file(self, arg: object, /) -> None: ...

    @property
    def group_size(self) -> int:
        """The size of the automorphism group as :class:`int`."""

    @property
    def group_size_as_bignum(self) -> BigNum:
        """The size of the automorphism group as :class:`BigNum`."""

    @property
    def group_size_approx(self) -> float:
        """
        An approximation (due to possible overflows/rounding errors) of the size of the automorphism group
        """

    @property
    def n_nodes(self) -> int:
        """Number of nodes in the search tree."""

    @property
    def n_leaf_nodes(self) -> int:
        """Number of leaf nodes in the search tree."""

    @property
    def n_bad_nodes(self) -> int:
        """Number of bad nodes in the search tree."""

    @property
    def n_canupdates(self) -> int:
        """Number of canonical representative nodes."""

    @property
    def n_generators(self) -> int:
        """Number of generator permutations."""

    @property
    def max_level(self) -> int:
        """The maximal depth of the search tree."""

    def __str__(self) -> str: ...

def permutation_to_str(perm: Annotated[ArrayLike, dict(dtype='uint32', shape=(None))], offset: int = 0) -> str:
    """
    Returns a :class:`str` corresponding to the permutation *perm* in cycle format. The amount *offset* is added to each element before stringifying, e.g. the permutation (2 4) is printed as (3 5) when *offset* is 1. Also see :func:`print_permutation_to_file`.
    """

def print_permutation_to_file(fp: object, perm: Annotated[ArrayLike, dict(dtype='uint32', shape=(None))], offset: int = 0) -> None:
    """
    Print the permutation in the cycle format in the file stream *fp*. The amount *offset* is added to each element before printing, e.g. the permutation (2 4) is printed as (3 5) when *offset* is 1. Wraps ``print_permutation`` from the C++-API. Also see :func:`permutation_to_str`.
    """
