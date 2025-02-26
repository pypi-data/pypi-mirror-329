"""
Module defining data structures describing the computational grid.

.. figure:: ../../../docs/source/resources/data_structures_overview.png

"""

from __future__ import annotations

import copy
import textwrap
import datetime
import time
from functools import partial
from multiprocessing import Pool

import numpy as np
from scipy.spatial import Delaunay, KDTree
from typing import Iterable, Any, List, Dict, Tuple, Optional
from collections import defaultdict, deque

from pyCFS.data.io import CFSResultArray, cfs_types
from pyCFS.data.io.CFSResultData import CFSResultData
from pyCFS.data.io.cfs_types import cfs_element_type, cfs_result_type
from pyCFS.data.util import (
    vprint,
    progressbar,
    element_quality,
    list_search,
    element_centroid,
    element_normal_2d,
    node_normal_2d,
    renumber_connectivity,
    reshape_connectivity,
    apply_dict_vectorized,
    TimeRecord,
)
from pyCFS.data import v_def


class CFSMeshInfo:
    """
    Data structure containing mesh information

    Notes
    -----
    -  ``update_by_coord_types`` Update structure based on coordinate and element types as defined in CFSMeshData

    Examples
    --------
    >>> from pyCFS.data.io import CFSReader, CFSMeshInfo
    >>> with CFSReader('file.cfs') as f:
    >>>     coordinates = f.Coordinates
    >>>     element_types = f.ElementTypes
    >>> MeshInfo = CFSMeshInfo()
    >>> MeshInfo.update_by_coord_types(coordinates=coordinates,element_types=element_types)

    """

    def __init__(self, coordinates: Optional[np.ndarray] = None, types: Optional[np.ndarray] = None) -> None:
        self._initilize()

        if coordinates is not None and types is not None:
            self.update_by_coord_types(coordinates=coordinates, types=types)

    def __repr__(self) -> str:
        return f"""Mesh Info ({self.Dimension}D, {self.NumNodes} Nodes, {self.NumElems} Elements)"""

    def __str__(self) -> str:
        return textwrap.dedent(
            f"""
        Mesh
         - Dimension: {self.Dimension}
         - Nodes:     {self.NumNodes}
         - Elements:  {self.NumElems}"""
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, CFSMeshInfo):
            return False
        return all(
            [
                self.Dimension == other.Dimension,
                self.Num1DElems == other.Num1DElems,
                self.Num2DElems == other.Num2DElems,
                self.Num3DElems == other.Num3DElems,
                self.NumElems == other.NumElems,
                self.Num_HEXA20 == other.Num_HEXA20,
                self.Num_HEXA27 == other.Num_HEXA27,
                self.Num_HEXA8 == other.Num_HEXA8,
                self.Num_PYRA13 == other.Num_PYRA13,
                self.Num_PYRA14 == other.Num_PYRA14,
                self.Num_PYRA5 == other.Num_PYRA5,
                self.Num_WEDGE15 == other.Num_WEDGE15,
                self.Num_WEDGE18 == other.Num_WEDGE18,
                self.Num_WEDGE6 == other.Num_WEDGE6,
                self.Num_TET10 == other.Num_TET10,
                self.Num_TET4 == other.Num_TET4,
                self.Num_QUAD4 == other.Num_QUAD4,
                self.Num_QUAD8 == other.Num_QUAD8,
                self.Num_QUAD9 == other.Num_QUAD9,
                self.Num_TRIA3 == other.Num_TRIA3,
                self.Num_TRIA6 == other.Num_TRIA6,
                self.Num_LINE2 == other.Num_LINE2,
                self.Num_LINE3 == other.Num_LINE3,
                self.Num_POINT == other.Num_POINT,
                self.Num_POLYGON == other.Num_POLYGON,
                self.Num_POLYHEDRON == other.Num_POLYHEDRON,
                self.Num_UNDEF == other.Num_UNDEF,
                self.QuadraticElems == other.QuadraticElems,
                self.NumNodes == other.NumNodes,
            ]
        )

    def _initilize(self) -> None:
        self.Dimension = -1
        self.Num1DElems = 0
        self.Num2DElems = 0
        self.Num3DElems = 0
        self.NumElems = 0
        self.Num_HEXA20 = 0
        self.Num_HEXA27 = 0
        self.Num_HEXA8 = 0
        self.Num_PYRA13 = 0
        self.Num_PYRA14 = 0
        self.Num_PYRA5 = 0
        self.Num_WEDGE15 = 0
        self.Num_WEDGE18 = 0
        self.Num_WEDGE6 = 0
        self.Num_TET10 = 0
        self.Num_TET4 = 0
        self.Num_QUAD4 = 0
        self.Num_QUAD8 = 0
        self.Num_QUAD9 = 0
        self.Num_TRIA3 = 0
        self.Num_TRIA6 = 0
        self.Num_LINE2 = 0
        self.Num_LINE3 = 0
        self.Num_POINT = 0
        self.Num_POLYGON = 0
        self.Num_POLYHEDRON = 0
        self.Num_UNDEF = 0
        self.QuadraticElems = False
        self.NumNodes = 0

    def update_by_coord_types(self, coordinates: np.ndarray, types: np.ndarray) -> None:
        """
        Update structure based on coordinate and element types as defined in CFSMeshData

        Parameters
        ----------
        coordinates : numpy.ndarray
            Coordinate array (Nx3) of the whole mesh (N number of nodes)

        types : numpy.ndarray[cfs_element_type]
            Element type array (Nx1) of the whole mesh (N number of elements).
            Element definitions based on pyCFS.data.io.cfs_types.cfs_element_type

        """
        # Reinitialize structure for empty input arrays
        if coordinates.size == 0 or types.size == 0:
            self._initilize()
            return

        self.NumNodes = coordinates.shape[0]
        self.NumElems = types.shape[0]

        self.Num_HEXA20 = np.count_nonzero(types == cfs_element_type.HEXA20)
        self.Num_HEXA27 = np.count_nonzero(types == cfs_element_type.HEXA27)
        self.Num_HEXA8 = np.count_nonzero(types == cfs_element_type.HEXA8)
        self.Num_PYRA13 = np.count_nonzero(types == cfs_element_type.PYRA13)
        self.Num_PYRA14 = np.count_nonzero(types == cfs_element_type.PYRA14)
        self.Num_PYRA5 = np.count_nonzero(types == cfs_element_type.PYRA5)
        self.Num_WEDGE15 = np.count_nonzero(types == cfs_element_type.WEDGE15)
        self.Num_WEDGE18 = np.count_nonzero(types == cfs_element_type.WEDGE18)
        self.Num_WEDGE6 = np.count_nonzero(types == cfs_element_type.WEDGE6)
        self.Num_TET10 = np.count_nonzero(types == cfs_element_type.TET10)
        self.Num_TET4 = np.count_nonzero(types == cfs_element_type.TET4)
        self.Num_QUAD4 = np.count_nonzero(types == cfs_element_type.QUAD4)
        self.Num_QUAD8 = np.count_nonzero(types == cfs_element_type.QUAD8)
        self.Num_QUAD9 = np.count_nonzero(types == cfs_element_type.QUAD9)
        self.Num_TRIA3 = np.count_nonzero(types == cfs_element_type.TRIA3)
        self.Num_TRIA6 = np.count_nonzero(types == cfs_element_type.TRIA6)
        self.Num_LINE2 = np.count_nonzero(types == cfs_element_type.LINE2)
        self.Num_LINE3 = np.count_nonzero(types == cfs_element_type.LINE3)
        self.Num_POINT = np.count_nonzero(types == cfs_element_type.POINT)
        self.Num_POLYGON = np.count_nonzero(types == cfs_element_type.POLYGON)
        self.Num_POLYHEDRON = np.count_nonzero(types == cfs_element_type.POLYHEDRON)
        self.Num_UNDEF = np.count_nonzero(types == cfs_element_type.UNDEF)

        self.QuadraticElems = (
            self.Num_HEXA20
            + self.Num_HEXA27
            + self.Num_PYRA13
            + self.Num_PYRA14
            + self.Num_WEDGE15
            + self.Num_WEDGE18
            + self.Num_TET10
            + self.Num_QUAD8
            + self.Num_QUAD9
            + self.Num_TRIA6
            + self.Num_LINE3
        ) > 0

        self.Num1DElems = self.Num_LINE2 + self.Num_LINE3
        self.Num2DElems = (
            self.Num_QUAD4 + self.Num_QUAD8 + self.Num_QUAD9 + self.Num_TRIA3 + self.Num_TRIA6 + self.Num_POLYGON
        )
        self.Num3DElems = (
            self.Num_HEXA20
            + self.Num_HEXA27
            + self.Num_HEXA8
            + self.Num_PYRA13
            + self.Num_PYRA14
            + self.Num_PYRA5
            + self.Num_WEDGE15
            + self.Num_WEDGE18
            + self.Num_WEDGE6
            + self.Num_TET10
            + self.Num_TET4
            + self.Num_POLYHEDRON
        )

        if self.Num3DElems > 0:
            self.Dimension = 3
        elif self.Num2DElems > 0:
            self.Dimension = 2
        elif self.Num1DElems > 0:
            self.Dimension = 1
        elif self.Num_POINT > 0:
            self.Dimension = 0
        else:
            self.Dimension = -1


class CFSMeshData:
    """
    Data structure containing mesh definition

    .. figure:: ../../../docs/source/resources/data_structures_CFSMeshData.png

    Parameters
    ----------
    coordinates : numpy.ndarray, optional
        Coordinate array (Nx3) of the whole mesh (N number of nodes)
    connectivity : numpy.ndarray, optional
        Connectivity array (NxM) of the whole mesh (N number of elements, M maximum number of nodes per element).
        Includes zero entries in case of different element types.
    types : numpy.ndarray[cfs_element_type], optional
        Element type array (Nx1) of the whole mesh (N number of elements).
        Element definitions based on pyCFS.data.io.cfs_types.cfs_element_type
    regions : list[pyCFS.data.io.CFSRegData], optional
        list of data structures containing data about a group or region.
    verbosity : int, optional
        Verbosity level <=1000 ; see v_def.py for predefined levels. Default is v_def.release.

    Attributes
    ----------
    Coordinates : np.ndarray
        Coordinate array (Nx3) of the whole mesh (N number of nodes)
    Connectivity : np.ndarray
        Connectivity array (NxM) of the whole mesh (N number of elements, M maximum number of nodes per element).
        Includes zero entries in case of different element types.
    Types : np.ndarray
        Element type array (Nx1) of the whole mesh (N number of elements).
        Element definitions based on pyCFS.data.io.cfs_types.cfs_element_type
    MeshInfo : CFSMeshInfo
        Data structure containing mesh information. All attributes are also directly accessible e.g. `meshdata_obj.NumNodes`.
    Regions : list[CFSRegData]
        List of data structures containing mesh region definition
    ElementCentroids : np.ndarray
        Centroids of mesh elements
    Quality : np.ndarray
        Quality metric of mesh elements

    Notes
    -----
    -  ``update_mesh_centroids`` Compute element centroids.

    -  ``get_mesh_centroids`` Compute geometric centers of mesh elements.

    -  ``get_mesh_surface_normals`` Compute surface normal vectors of surface mesh.

    -  ``update_mesh_quality`` Compute mesh metric based on ‘metric’.

    -  ``get_mesh_quality`` Compute mesh metric based on the specified metric.

    -  ``merge`` Merges mesh with other mesh removing duplicate coordinates and elements

    -  ``update_info`` Update structure based on coordinate and element types

    -  ``check_add_point_elements`` Check groups/regions for not defined Elements (Nodes only) and create POINT elements

    -  ``extract_nodes_elements`` Extract nodes and elements from the mesh data structure.

    -  ``drop_nodes_elements`` Drop nodes and elements from the mesh data structure.

    -  ``drop_unused_nodes_elements`` Drop nodes and elements that are not used in the given list of groups/regions.

    -  ``merge_duplicate_nodes`` Merge duplicate nodes in the coordinate array and update regions.

    -  ``renumber_nodes`` Renumber nodes in the connectivity array and update regions.

    -  ``convert_to_simplex`` Convert arbitrary 3D elements into simplexes (tetrahedra), by applying Delaunay triangulation.

    -  ``convert_quad2tria`` Convert QUAD4 elements into TRIA3 elements. If ‘idx_convert’ is unspecified all QUAD4 in the mesh are converted.

    -  ``get_region`` Get region data structure by name.

    -  ``get_region_nodes`` Get node indices of a region.

    -  ``get_region_elements`` Get element indices of a region.

    -  ``get_region_coordinates`` Get coordinates of a region.

    -  ``get_region_connectivity`` Get connectivity of a region.

    -  ``get_region_element_types`` Get element types of a region.

    -  ``get_region_centroids`` Get element centroids of a region.

    -  ``get_closest_node`` Get the closest node to a given coordinate.

    -  ``get_closest_element`` Get the closest element to a given coordinate.

    -  ``reorient_region`` Reorient elements of a region based on the element centroid.

    -  ``reorient_elements`` Reorient elements based on the element centroid.

    -  ``from_coordinates_connectivity`` (Classmethod)
        Generates data objects to create cfs mesh with one single region containing all elements.
        Detects element type from number of nodes. Therefore, all elements must have same dimension.

    Examples
    --------
    >>> from pyCFS.data.io import CFSReader, CFSMeshInfo
    >>> with CFSReader('file.cfs') as f:
    >>>     coordinates = f.Coordinates
    >>>     connectivity = f.Connectivity
    >>>     ElementTypes = f.ElementTypes
    >>>     region_data = f.MeshGroupsRegions
    >>> mesh = CFSMeshData(coordinates=coordinates, connectivity=connectivity, ElementTypes=ElementTypes,
    >>>                    regions=region_data)

    """  # noqa : E501

    def __init__(
        self,
        coordinates=np.empty((0, 3)),
        connectivity=np.empty((0, 1)),
        types=np.empty(0),
        regions: List[CFSRegData] | None = None,
        verbosity=v_def.release,
    ) -> None:
        """Initializes a CFSMeshData object. If both Coordinates and types are provided,
        also updates mesh attributes."""
        if regions is None:
            regions = []
        self.Verbosity = verbosity
        self.Coordinates = coordinates
        self.Connectivity = connectivity
        self.Types: np.ndarray = types
        if self.Types.ndim == 1:
            self.Types = self.Types.reshape(-1, 1)
        self.Regions: List[CFSRegData] = regions
        self.check_add_point_elements()
        self._flag_warn_element_centroid = True
        self._flag_warn_element_quality = True
        self._ElementCentroids: np.ndarray | None = None
        self._Quality: np.ndarray | None = None

    def __getattr__(self, name):
        return getattr(self.MeshInfo, name)

    def __deepcopy__(self, memodict={}):
        # Create a new instance of CFSMeshData
        new_instance = self.__class__()
        memodict[id(self)] = new_instance

        # Copy attributes
        for k, v in self.__dict__.items():
            setattr(new_instance, k, copy.deepcopy(v, memodict))

        return new_instance

    # noinspection LongLine
    def __repr__(self) -> str:
        return f"""Mesh ({self.MeshInfo.Dimension}D, {self.MeshInfo.NumNodes} Nodes, {self.MeshInfo.NumElems} Elements, {len(self.Regions)} Regions)"""

    def __str__(self) -> str:
        reg_str = str().join([f"   - {reg}\n" for reg in self.Regions])
        return textwrap.dedent(f"{self.MeshInfo}\n - Regions:   {len(self.Regions)}\n{reg_str}")

    def __eq__(self, other) -> bool:
        if not isinstance(other, CFSMeshData):
            return False
        return all(
            [
                np.array_equal(self.Coordinates, other.Coordinates),
                np.array_equal(self.Connectivity, other.Connectivity),
                np.array_equal(self.Types, other.Types),
                self.MeshInfo == other.MeshInfo,
                sorted(self.Regions) == sorted(other.Regions),
            ]
        )

    def __add__(self, other: CFSMeshData):
        return self.merge(other)

    @property
    def MeshInfo(self) -> CFSMeshInfo:
        """Mesh information data structure"""
        return CFSMeshInfo(coordinates=self.Coordinates, types=self.Types)

    @property
    def Connectivity(self):
        """Element Connectivity array"""
        return self._Connectivity

    @Connectivity.setter
    def Connectivity(self, nodes):
        self._Connectivity = np.array(nodes, dtype=np.uint32)

    @property
    def ElementCentroids(self) -> np.ndarray | None:
        """
        Compute element centroids. Doesn't update automatically compute for large meshes.

        Returns
        -------
        np.ndarray
            Array of element centroids.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>> mesh.update_mesh_centroids()
        >>> centroids = mesh.ElementCentroids

        """
        max_element_threshold = 1e3  # Don't compute automatically for large meshes.
        if self.MeshInfo.NumElems < max_element_threshold:
            if self._ElementCentroids is None:
                self._ElementCentroids = self.get_mesh_centroids()
        else:
            if self._flag_warn_element_centroid:
                vprint(
                    "Warning: ElementCentroids not updated automatically due to large number of elements. "
                    'Please call "obj.get_mesh_centroids()" to compute centroids',
                    verbose=self.Verbosity >= v_def.release,
                )
                self._flag_warn_element_centroid = False
        return self._ElementCentroids

    def update_mesh_centroids(self, processes: int | None = None):
        """Compute element centroids."""
        self._ElementCentroids = self.get_mesh_centroids(processes=processes)

    def get_mesh_centroids(self, el_idx: np.ndarray | None = None, processes: int | None = None) -> np.ndarray:
        """
        Compute geometric centers of mesh elements.

        Parameters
        ----------
        el_idx : numpy.ndarray, optional
            Array of (global) element ids (starting from 0) for which to compute centroids. The default is ``None``,
            in which case all elements are processed.
        processes : int, optional
            Number of processes to use in parallel. The default is ``None``, in which case all cores are used.

        Returns
        -------
        np.ndarray
            Array of element centroids.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>> element_indices = np.array([0,1,2,3])
        >>> centroids = mesh.get_mesh_centroids(el_idx=element_indices,processes=1)

        """
        if el_idx is None:
            el_idx_it: Iterable[Any] = range(self.Connectivity.shape[0])
        elif isinstance(el_idx, np.ndarray):
            el_idx_it = el_idx
        else:
            raise TypeError("el_idx must be of type numpy.ndarray, or None")

        mesh_centroids = np.zeros((self.Connectivity[el_idx_it, :].shape[0], 3), dtype=float)

        t_start = time.time()
        el_idx_it_done: List = []
        for cidx in progressbar(
            range(self.Connectivity.shape[1]),
            prefix="Computing mesh centroids: ",
            verbose=self.Verbosity >= v_def.debug,
        ):
            if cidx == 0:
                conn = self.Connectivity
            else:
                conn = self.Connectivity[:, 0:-cidx]

            el_idx_it_cur = np.intersect1d(el_idx_it, np.argwhere(np.all(conn, axis=1)))  # type: ignore[call-overload]
            el_idx_it_cur = el_idx_it_cur[~np.isin(el_idx_it_cur, el_idx_it_done)]
            if el_idx_it_cur.size == 0:
                continue
            element_connectivity = conn[el_idx_it_cur, :]
            element_coordinates = self.Coordinates[element_connectivity - 1, :]
            mesh_centroids[np.isin(el_idx_it, el_idx_it_cur), :] = element_centroid(element_coordinates)  # type: ignore[arg-type]

            el_idx_it_done += list(el_idx_it_cur)
            if el_idx_it_cur.size > 0 and np.all(conn[el_idx_it, 0:-cidx]) and np.all(conn[el_idx_it, :]):
                vprint(
                    f"Computing mesh centroids | Elapsed time: {datetime.timedelta(seconds=int(time.time() - t_start))}",
                    verbose=self.Verbosity >= v_def.debug,
                )
                break

        return mesh_centroids

    def get_mesh_surface_normals(
        self,
        restype=cfs_result_type.ELEMENT,
        node_idx_include: Optional[np.ndarray] = None,
        el_idx_include: Optional[np.ndarray] = None,
        processes: Optional[int] = None,
    ) -> np.ndarray:
        """
        Compute surface normal vectors of surface mesh.

        Parameters
        ----------
        restype: cfs_result_type, optional
        node_idx_include: numpy.ndarray, optional
        el_idx_include: numpy.ndarray, optional
        processes: int, optional

        Returns
        -------
        numpy.ndarray

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>> mesh_normal_vectors = mesh.get_mesh_surface_normals()
        """
        _supported_types = [cfs_element_type.TRIA3, cfs_element_type.QUAD4, cfs_element_type.POLYGON]

        if node_idx_include is None:
            node_idx_include = np.arange(self.Coordinates.shape[0])
        if el_idx_include is None:
            el_idx_include = np.arange(self.Connectivity.shape[0])

        # Get supported elements
        el_idx_supported = np.argwhere(np.isin(self.Types[el_idx_include].flatten(), _supported_types)).flatten()

        if restype == cfs_result_type.ELEMENT:
            surface_normals = np.zeros((el_idx_include.shape[0], 3))
            surface_normals.fill(np.nan)
            # Extract element coordinates for supported elements
            el_coord = self.Coordinates[self.Connectivity[el_idx_include[el_idx_supported], 0:3] - 1]
            # Compute element surface normal vecotors
            surface_normals[el_idx_supported, :] = element_normal_2d(element_coordinates=el_coord)

        elif restype == cfs_result_type.NODE:
            # raise NotImplementedError("Evaluating surface normal on nodes currently not implemented.")
            coord = self.Coordinates[node_idx_include, :]
            conn = self.Connectivity[el_idx_include, :][el_idx_supported, :]

            surface_normals = np.zeros((coord.shape[0], 3))
            surface_normals.fill(np.nan)

            with TimeRecord(message="Computing node normals", verbose=self.Verbosity >= v_def.debug):
                with Pool(processes=processes) as pool:
                    for idx, res in enumerate(
                        pool.map(
                            partial(
                                _compute_mesh_node_normal,
                                connectivity=conn,
                                coordinates=coord,
                            ),
                            node_idx_include,
                        )
                    ):
                        surface_normals[node_idx_include[idx], :] = res
        else:
            raise NotImplementedError(
                f"Evaluating surface normal on {restype} not implemented. Supported on NODE and ELEMENT, only!"
            )

        return surface_normals

    @property
    def Quality(self) -> np.ndarray | None:
        """
        Compute mesh metric with standard parameters. Doesn't update automatically for large meshes.

        Returns
        -------
        np.ndarray
            Array of mesh metric values. Return -1 for unsupported element types.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>> mesh.update_mesh_quality()
        >>> metric = mesh.Quality

        """
        max_element_threshold = 1e3  # Don't compute automatically for large meshes.
        if self.MeshInfo.NumElems < max_element_threshold:
            if self._Quality is None:
                # TODO deal with failing element quality computation (prevent infinite loop)
                self._Quality = self.get_mesh_quality()
        else:
            if self._flag_warn_element_quality:
                vprint(
                    "Warning: Quality not updated automatically due to large number of elements. "
                    'Please call "obj.update_mesh_quality()" to compute element quality.',
                    verbose=self.Verbosity >= v_def.release,
                )
                self._flag_warn_element_quality = False
        return self._Quality

    def update_mesh_quality(self, metric="quality", processes: int | None = None):
        """
        Compute mesh metric based on 'metric'.

        Parameters
        ----------
        metric : str, optional
            Metric type to compute. The default is 'quality'.
        processes : int, optional
            Number of processes to use in parallel. The default is ``None``, in which case all cores are used.

        Returns
        -------
        np.ndarray
            Array of mesh metric values. Return -1 for unsupported element types.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>> mesh.update_mesh_quality(metric='skewness', processes=1)
        >>> metric = mesh.Quality

        """
        """ Compute mesh metric """
        self._Quality = self.get_mesh_quality(metric=metric, processes=processes)

    def get_mesh_quality(self, metric="quality", processes: int | None = None) -> np.ndarray:
        """
        Compute mesh metric based on the specified metric.

        Parameters
        ----------
        metric : str, optional
            Metric type to compute. The default is ``quality``.
        processes : int, optional
            Number of processes to use in parallel. The default is ``None``, in which case all cores are used.

        Returns
        -------
        np.ndarray
            Array of mesh metric values. Returns -1 for unsupported element types.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>> metric = mesh.get_mesh_quality(metric='skewness', processes=1)
        """
        supported_types = {
            "quality": (
                cfs_element_type.TRIA3,
                cfs_element_type.QUAD4,
                cfs_element_type.TET4,
                cfs_element_type.HEXA8,
                cfs_element_type.WEDGE6,
                cfs_element_type.PYRA5,
            ),
            "skewness": (cfs_element_type.TRIA3, cfs_element_type.QUAD4),
        }

        if metric not in supported_types:
            raise NotImplementedError(f"Implemented mesh quality metrics: {list(supported_types.keys())}.")

        mesh_quality = np.ones(self.Types.shape, dtype=float) * -1
        # Extract supported element types
        idx_support_lst = []
        for el_type in supported_types[metric]:
            idx_support_lst.append(np.where(self.Types == el_type)[0])
        idx_support = np.hstack(idx_support_lst)

        with TimeRecord(message="Computing mesh quality", verbose=self.Verbosity >= v_def.debug):
            with Pool(processes=processes) as pool:
                for i, res in enumerate(
                    pool.map(
                        partial(
                            _compute_mesh_quality,
                            connectivity=self.Connectivity,
                            coordinates=self.Coordinates,
                            el_types=self.Types,
                            metric=metric,
                        ),
                        idx_support,
                    )
                ):
                    mesh_quality[i] = res

        return mesh_quality

    def merge(self, other: CFSMeshData) -> CFSMeshData:
        """
        Merges mesh with other mesh removing duplicate Coordinates and elements

        Parameters
        ----------
        other : CFSMeshData
            Mesh data object that is merged with.

        Returns
        -------
        CFSMeshData
            Merged mesh data structure.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file1.cfs') as f:
        >>>     mesh1 = f.MeshData
        >>> with CFSReader('file2.cfs') as f:
        >>>     mesh2 = f.MeshData
        >>> mesh_merged = mesh1.merge(mesh2)

        """
        if type(other) is not CFSMeshData:
            raise NotImplementedError("Addition of CFSMeshData only implemented with other object of type CFSMeshData!")

        # Merge Coordinates
        coord_merge, idx_coord_inv = np.unique(
            np.append(self.Coordinates, other.Coordinates, axis=0),
            axis=0,
            return_inverse=True,
        )

        idx_coord_self = idx_coord_inv[: self.Coordinates.shape[0]]
        idx_coord_other = idx_coord_inv[self.Coordinates.shape[0] :]

        # Take starting index 1 for Connectivity into account (keep in mind there are 0 entries for unused columns)
        idx_coord_self = np.insert(idx_coord_self, 0, values=-1)
        idx_coord_other = np.insert(idx_coord_other, 0, values=-1)

        # Merge Connectivity
        conn_self = idx_coord_self[self.Connectivity] + 1
        conn_other = idx_coord_other[other.Connectivity] + 1

        num_rows = max(conn_self.shape[1], conn_other.shape[1])
        while conn_self.shape[1] < num_rows:
            conn_self = np.c_[conn_self, np.zeros(conn_self.shape[0])]

        while conn_other.shape[1] < num_rows:
            conn_other = np.c_[conn_other, np.zeros(conn_other.shape[0])]

        conn_merge, idx_conn, idx_conn_inv = np.unique(
            np.append(conn_self, conn_other, axis=0),
            axis=0,
            return_index=True,
            return_inverse=True,
        )

        idx_conn_self = idx_conn_inv[: conn_self.shape[0]]
        idx_conn_other = idx_conn_inv[conn_self.shape[0] :]

        # Merge types
        types_merge = np.append(self.Types, other.Types)[idx_conn]

        # Create merged mesh object
        return_mesh = CFSMeshData(
            coordinates=coord_merge,
            connectivity=conn_merge,
            types=types_merge,
            verbosity=self.Verbosity,
        )

        if self.Regions or other.Regions:
            # Merge and update regions
            for reg in self.Regions:
                return_reg = CFSRegData(
                    name=reg.Name,
                    dimension=reg.Dimension,
                    is_group=reg.IsGroup,
                    verbosity=self.Verbosity,
                )
                return_reg.Nodes = idx_coord_self[reg.Nodes] + 1
                return_reg.Elements = idx_conn_self[reg.Elements - 1] + 1
                return_mesh.Regions.append(return_reg)
            for reg in other.Regions:
                return_reg = CFSRegData(
                    name=reg.Name,
                    dimension=reg.Dimension,
                    is_group=reg.IsGroup,
                    verbosity=self.Verbosity,
                )
                return_reg.Nodes = idx_coord_other[reg.Nodes] + 1
                return_reg.Elements = idx_conn_other[reg.Elements - 1] + 1
                return_mesh.Regions.append(return_reg)

        return return_mesh

    def update_info(self) -> None:
        """Update structure based on coordinate and element types"""
        self.MeshInfo.update_by_coord_types(coordinates=self.Coordinates, types=self.Types)

    def check_add_point_elements(self) -> None:
        """Check groups/regions for not defined Elements (Nodes only) and create POINT elements"""
        for reg in self.Regions:
            if reg.Elements.size == 0:
                vprint(
                    f"Missing point elements detected in group/region {reg.Name}. Adding point elements.",
                    verbose=self.Verbosity >= v_def.release,
                )
                # Define Element IDs
                reg.Elements = np.arange(reg.Nodes.size, dtype=np.int32) + self.Connectivity.shape[0] + 1
                # Add elements to connectivity and types
                conn_add = np.zeros((reg.Nodes.size, self.Connectivity.shape[1]))
                conn_add[:, 0] = reg.Nodes
                el_types_add = np.array(
                    [cfs_element_type.POINT for _ in range(reg.Nodes.size)], dtype=np.int32
                ).reshape(-1, 1)

                self.Connectivity = np.vstack((self.Connectivity, conn_add))
                self.Types = np.vstack((self.Types, el_types_add))

    def extract_nodes_elements(
        self,
        node_idx: np.ndarray | None = None,
        el_idx: np.ndarray | None = None,
        result_data: CFSResultData | None = None,
    ) -> CFSResultData | None:

        el_idx_extract: Optional[List[int] | np.ndarray] = None
        if node_idx is not None:
            vprint(f"Extracting {len(node_idx)} nodes", verbose=self.Verbosity >= v_def.debug)
            # Drop Elements from connectivity
            mask = np.ones(self.Connectivity.shape[0], dtype=bool)

            for idx in progressbar(node_idx, prefix="Select elements: ", verbose=self.Verbosity >= v_def.debug):
                # Check for rows that do not contain the specified value
                mask = ~np.any(self.Connectivity == idx + 1, axis=1) & mask

            vprint(
                f"Selected {np.sum(~mask)} elements containing nodes to extract",
                verbose=self.Verbosity >= v_def.debug,
            )
            el_idx_extract = np.where(~mask)[0]

        if el_idx_extract is None or len(el_idx_extract) == 0:
            el_idx_extract = el_idx
        elif el_idx is not None:
            el_idx_extract = np.union1d(el_idx, el_idx_extract)

        el_idx_drop = np.setdiff1d(np.arange(self.Connectivity.shape[0]), el_idx_extract)  # type: ignore[arg-type]

        result_data = self.drop_nodes_elements(el_idx=el_idx_drop, result_data=result_data)

        return result_data

    def drop_nodes_elements(
        self,
        node_idx: np.ndarray | None = None,
        el_idx: np.ndarray | None = None,
        result_data: CFSResultData | None = None,
    ) -> CFSResultData | None:
        """
        Drop nodes and elements from the mesh data structure. (AI-generated)

        Parameters
        ----------
        node_idx : np.ndarray or None, optional
            Array of node indices to drop, by default None.
        el_idx : np.ndarray or None, optional
            Array of element indices to drop, by default None.
        result_data : CFSResultData or None, optional
            Result data associated with the mesh, by default None.

        Returns
        -------
        CFSResultData or None
            Updated result data after dropping nodes and elements, or None if no result data is provided.
        """
        el_idx_drop: Optional[List[int] | np.ndarray] = None
        if node_idx is not None:
            vprint(f"Dropping {len(node_idx)} nodes", verbose=self.Verbosity >= v_def.debug)
            # Drop Elements from connectivity
            mask = np.ones(self.Connectivity.shape[0], dtype=bool)

            for idx in progressbar(node_idx, prefix="Select elements: ", verbose=self.Verbosity >= v_def.debug):
                # Check for rows that do not contain the specified value
                mask = ~np.any(self.Connectivity == idx + 1, axis=1) & mask

            vprint(
                f"Selected {np.sum(~mask)} elements containing dropped nodes to be removed",
                verbose=self.Verbosity >= v_def.debug,
            )
            el_idx_drop = np.where(~mask)[0]

        if el_idx_drop is None or len(el_idx_drop) == 0:
            el_idx_drop = el_idx
        elif el_idx is not None:
            el_idx_drop = np.union1d(el_idx, el_idx_drop)

        if el_idx_drop is not None:
            vprint(f"Dropping {len(el_idx_drop)} elements", verbose=self.Verbosity >= v_def.release)
            result_data = self._drop_elements(el_idx=el_idx_drop, result_data=result_data)

        return result_data

    def _drop_elements(
        self,
        el_idx: List[int] | np.ndarray,
        result_data: CFSResultData | None = None,
    ) -> CFSResultData | None:
        """
        Drop elements from the mesh data structure. (AI-generated)

        Parameters
        ----------
        el_idx : list of int or np.ndarray
            List or array of element indices to drop.
        result_data : CFSResultData or None, optional
            Result data associated with the mesh, by default None.

        Returns
        -------
        CFSResultData or None
            Updated result data after dropping elements, or None if no result data is provided.
        """
        self.Types = np.delete(self.Types, el_idx, axis=0)

        nodes = np.unique(self.Connectivity)
        conn_new = np.delete(self.Connectivity, el_idx, axis=0)
        nodes_new = np.unique(conn_new)
        # Remove zero entry
        nodes = np.delete(nodes, np.where(nodes == 0)[0])
        nodes_new = np.delete(nodes_new, np.where(nodes_new == 0)[0])

        # Extract Coordinates
        _, idx_intersect, node_idx_keep = np.intersect1d(nodes_new, nodes, return_indices=True)
        self.Coordinates = self.Coordinates[node_idx_keep, :]

        # Element renumbering
        el_idx_keep = np.delete(np.arange(self.Connectivity.shape[0]), el_idx)
        renumber_element_dict = {el_idx_keep[idx] + 1: idx + 1 for idx in range(el_idx_keep.size)}

        # Node renumbering
        renumber_node_dict = {node_idx_keep[idx] + 1: idx + 1 for idx in range(node_idx_keep.size)}
        renumber_node_dict[0] = 0

        # Update regions
        result_data_node_dict = dict()
        result_data_el_dict = dict()

        idx_pop = []
        for idx, reg in enumerate(self.Regions):
            reg_el_idx = np.where(np.isin(reg.Elements, el_idx_keep + 1))[0]
            if reg_el_idx.size == 0:
                idx_pop.append(idx)
                continue
            reg.Elements = reg.Elements[reg_el_idx]

            reg_nodes = np.unique(self.get_region_connectivity(region=reg))
            reg_nodes = np.delete(reg_nodes, np.where(reg_nodes == 0)[0])
            _, _, reg_node_idx = np.intersect1d(reg_nodes, reg.Nodes, return_indices=True)
            reg.Nodes = reg_nodes

            # ID Renumbering
            reg.Nodes = apply_dict_vectorized(dictionary=renumber_node_dict, data=reg.Nodes)
            reg.Elements = apply_dict_vectorized(dictionary=renumber_element_dict, data=reg.Elements)

            result_data_node_dict[reg.Name] = reg_node_idx
            result_data_el_dict[reg.Name] = reg_el_idx

        idx_pop.sort(reverse=True)
        for idx in idx_pop:
            self.Regions.pop(idx)

        # Renumber Connectivity
        self.Connectivity = apply_dict_vectorized(dictionary=renumber_node_dict, data=conn_new)
        self.Connectivity = reshape_connectivity(self.Connectivity)

        if result_data is not None:
            idx_pop = []
            for idx, item in enumerate(result_data.Data):
                if item.ResType == cfs_result_type.NODE:
                    if item.Region in result_data_node_dict:
                        result_data.Data[idx] = item[:, result_data_node_dict[item.Region], ...]  # type: ignore[call-overload]
                    else:
                        idx_pop.append(idx)
                        continue
                elif item.ResType == cfs_result_type.ELEMENT:
                    if item.Region in result_data_el_dict:
                        result_data.Data[idx] = item[:, result_data_el_dict[item.Region], ...]  # type: ignore[call-overload]
                    else:
                        result_data.Data.pop(result_data.Data.index(item))
                        idx_pop.append(idx)
                        continue
            idx_pop.sort(reverse=True)
            for idx in idx_pop:
                result_data.Data.pop(idx)

        return result_data

    def drop_unused_nodes_elements(self, reg_data_list: Optional[List[CFSRegData]] = None):
        """
        Drop nodes and elements that are not used in the given list of groups/regions.

        Parameters
        ----------
        reg_data_list : list[CFSRegData], optional
            List of groups/regions

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> from pyCFS.data.util import list_search
        >>> with CFSReader('file1.cfs') as f:
        >>>     mesh = f.MeshData
        >>>     regions_data = f.MeshGroupsRegions
        >>> regions_data_keep = [list_search(regions_data, 'region_name')]
        >>> mesh.drop_unused_nodes_elements(reg_data_list=regions_data_keep)

        """
        if reg_data_list is None:
            reg_data_list = self.Regions
        self._drop_unused_elements(reg_data_list)
        self._drop_unused_nodes(reg_data_list)
        self.Regions = reg_data_list

    # noinspection PyTypeChecker,LongLine
    def _drop_unused_elements(self, reg_data_list: List[CFSRegData]) -> bool:
        """
        Drop elements that are not used in the given list of groups/regions.

        Parameters
        ----------
        reg_data_list

        Returns
        -------
        bool

        """
        # TODO optimize (see for CFSRegData.update_nodes_from_elements)
        used_elements = set()
        for reg_data in reg_data_list:
            used_elements.update(reg_data.Elements.tolist())
        if self.Types.size == len(used_elements):
            vprint("No elements dropped", verbose=self.Verbosity > v_def.release)
            return False
        conn = []
        el_type = []
        counter = 1
        el_id_dict = {}
        for el_id in progressbar(
            range(self.Connectivity.shape[0]),
            prefix=f"{self.Types.size - len(used_elements)} elements dropped. Renumbering elments: ",
            size=24,
            verbose=self.Verbosity >= v_def.release,
        ):
            if el_id + 1 in used_elements:
                el_id_dict[el_id + 1] = counter
                counter += 1
                conn.append(self.Connectivity[el_id, :])
                el_type.append(self.Types[el_id])

        self.Connectivity = np.array(conn)

        # Remove columns containing zeros only
        self.Connectivity = reshape_connectivity(self.Connectivity)

        self.Types = np.array(el_type)
        self.MeshInfo.update_by_coord_types(self.Coordinates, self.Types)

        for reg_data in reg_data_list:
            reg_data.Elements = np.array([el_id_dict[el_id] for el_id in reg_data.Elements])
        return True

    # noinspection PyTypeChecker,LongLine
    def _drop_unused_nodes(self, reg_data_list: List[CFSRegData]):
        """
        Drop nodes that are not used in the given list of groups/regions.

        Parameters
        ----------
        reg_data_list

        Returns
        -------
        bool

        """
        # TODO optimize (see for CFSRegData.update_nodes_from_elements)
        # TODO optimize (see for CFSMeshData.renumber_nodes)
        used_nodes = set()
        for reg_data in reg_data_list:
            used_nodes.update(reg_data.Nodes.tolist())
        if self.Coordinates.shape[0] == len(used_nodes):
            vprint("No nodes dropped", verbose=self.Verbosity > v_def.release)
            return False
        coord = []
        counter = 1
        node_id_dict = {0: 0}
        for node_id in progressbar(
            range(self.Coordinates.shape[0]),
            prefix=f"{self.Coordinates.shape[0] - len(used_nodes)} nodes dropped. Renumbering nodes: ",
            size=26,
            verbose=self.Verbosity >= v_def.release,
        ):
            if node_id + 1 in used_nodes:
                node_id_dict[node_id + 1] = counter
                counter += 1
                coord.append(self.Coordinates[node_id, :])

        self.Coordinates = np.array(coord)
        self.MeshInfo.update_by_coord_types(self.Coordinates, self.Types)

        for c in range(self.Connectivity.shape[1]):
            self.Connectivity[:, c] = apply_dict_vectorized(data=self.Connectivity[:, c], dictionary=node_id_dict)

        for reg_data in reg_data_list:
            reg_data.Nodes = apply_dict_vectorized(data=reg_data.Nodes, dictionary=node_id_dict)

        return True

    def merge_duplicate_nodes(self, precision=10):
        """
        Merge duplicate nodes in the coordinate array and update regions.
        """
        # TODO merge_duplicate_elements
        coord_rounded = np.round(self.Coordinates, decimals=precision)

        _, unique_indices, inverse_indices, counts = np.unique(
            coord_rounded, axis=0, return_index=True, return_inverse=True, return_counts=True
        )

        node_id_dict = {nidx + 1: inverse_indices[nidx] + 1 for nidx in range(self.Coordinates.shape[0])}
        node_id_dict[0] = 0

        self.Coordinates = self.Coordinates[unique_indices]
        self.Connectivity = apply_dict_vectorized(data=self.Connectivity, dictionary=node_id_dict)

        # TODO for duplicate connectivity entries and change element type accordingly
        # for elidx in range(self.Connectivity.shape[0]):
        #     elconn, ridx, rinv = np.unique(self.Connectivity[elidx, :], return_index=True, return_inverse=True)

        for reg in self.Regions:
            reg.Nodes = np.unique(apply_dict_vectorized(data=reg.Nodes, dictionary=node_id_dict))

    def renumber_nodes(self):
        """
        Renumber nodes in the connectivity array and update regions.
        """
        self.Connectivity, eid_dict = renumber_connectivity(self.Connectivity)
        for reg in self.Regions:
            reg.Nodes = apply_dict_vectorized(data=reg.Nodes, dictionary=eid_dict)

    def convert_to_simplex(self, idx_convert: np.ndarray | None = None, result_data: CFSResultData | None = None):
        """
        Convert arbitrary 3D elements into simplices (tetrahedra), by applying Delaunay triangulation.
        """
        # TODO Check algorithm to prevent holes inside the volume domain
        # TODO Add support for 2D elements
        supported_types = {
            # cfs_element_type.QUAD4, cfs_element_type.QUAD8, cfs_element_type.QUAD9,
            cfs_element_type.TET10,
            cfs_element_type.HEXA8,
            cfs_element_type.HEXA20,
            cfs_element_type.HEXA27,
            cfs_element_type.PYRA5,
            cfs_element_type.PYRA13,
            cfs_element_type.PYRA14,
            cfs_element_type.WEDGE6,
            cfs_element_type.WEDGE15,
            cfs_element_type.WEDGE18,
            cfs_element_type.POLYHEDRON,
        }

        if idx_convert is None:
            idx_convert = np.array([i for i in range(self.Connectivity.shape[0])])

        num_el = self.Connectivity.shape[0]
        idx_convert_dict = {}
        reg_idx_convert_dict: Dict = {reg.Name: {} for reg in self.Regions}

        conn_add = []
        types_add = []

        for idx in progressbar(
            idx_convert,
            prefix="Converting elements into simplexes: ",
            verbose=self.Verbosity >= v_def.release,
        ):
            if cfs_element_type(self.Types[idx]) not in supported_types:
                if cfs_element_type(self.Types[idx]) == cfs_element_type.UNDEF:
                    vprint(
                        f"Warning: Element of type {cfs_element_type.UNDEF} can lead to unexpected result!",
                        verbose=self.Verbosity >= v_def.more,
                    )
                else:
                    vprint(
                        f"Skipped unsupported element ({cfs_element_type(self.Types[idx])})!",
                        verbose=self.Verbosity >= v_def.more,
                    )
                    continue
            conn_complex = self.Connectivity[idx, :]
            # Remove columns containing zeros only
            idx_zero = np.argwhere(conn_complex == 0).flatten()
            conn_complex = np.delete(conn_complex, idx_zero)
            coord_complex = self.Coordinates[conn_complex - 1, :]
            tri = Delaunay(coord_complex)

            complex_simplex_link = {i: conn_complex[i] for i in range(conn_complex.shape[0])}
            conn_simplex = apply_dict_vectorized(data=tri.simplices, dictionary=complex_simplex_link)
            conn_simplex = np.hstack(
                (
                    conn_simplex,
                    np.zeros(
                        (
                            conn_simplex.shape[0],
                            self.Connectivity.shape[1] - conn_simplex.shape[1],
                        ),
                        dtype=int,
                    ),
                )
            )

            vprint(
                f"Converted element ({cfs_element_type(self.Types[idx])}) into {conn_simplex.shape[0]} elements ({cfs_element_type.TET4})",
                verbose=self.Verbosity >= v_def.debug,
            )

            self.Connectivity[idx, :] = conn_simplex[0, :]  # Replace element
            self.Types[idx] = cfs_element_type.TET4

            conn_add.append(conn_simplex[1:, :])
            types_add.append(np.array([cfs_element_type.TET4 for i in range(conn_simplex.shape[0] - 1)]).reshape(-1, 1))

            idx_convert_dict[idx] = np.array([idx] + [i + num_el for i in range(conn_simplex.shape[0] - 1)])
            num_el += conn_simplex.shape[0] - 1  # Update number of elements

            for reg in self.Regions:
                if idx + 1 in reg.Elements.flatten():
                    reg_el_idx = int(np.where(idx + 1 == reg.Elements.flatten())[0].item())
                    reg_idx_convert_dict[reg.Name][reg_el_idx] = np.array(
                        [reg_el_idx] + [i + reg.Elements.size for i in range(conn_simplex.shape[0] - 1)]
                    )

                    reg.Elements = np.vstack(
                        (
                            np.expand_dims(reg.Elements.flatten(), 1),
                            np.expand_dims(idx_convert_dict[idx][1:] + 1, 1),
                        )
                    ).flatten()

        # Add additional elements
        self.Connectivity = np.vstack([self.Connectivity] + conn_add)
        self.Types = np.vstack([self.Types] + types_add)

        self.update_info()

        # Remove columns containing zeros only
        self.Connectivity = reshape_connectivity(self.Connectivity)

        # Adapt element result data
        if result_data is not None:
            for res_idx, res_data in enumerate(result_data.Data):
                if res_data.ResType == cfs_result_type.ELEMENT:
                    data_list = []
                    for k in progressbar(
                        range(res_data.StepValues.size),
                        prefix=f"Converting result {res_data.Quantity}: ",
                        verbose=self.Verbosity >= v_def.more,
                    ):
                        data = res_data[k, :, :]
                        for idx in reg_idx_convert_dict[res_data.Region]:
                            val = data[idx, :]
                            data = np.vstack(
                                (
                                    data,
                                    np.ones(
                                        (
                                            reg_idx_convert_dict[res_data.Region][idx].size - 1,
                                            res_data.shape[2],
                                        )
                                    )
                                    * val,
                                )
                            )
                        data_list.append(data)
                    res_data_new = CFSResultArray(np.array(data_list))
                    res_data_new.MetaData = res_data.MetaData
                    result_data.Data[res_idx] = res_data_new

            return result_data

        return None

    def convert_quad2tria(self, idx_convert: np.ndarray | None = None, result_data=None):
        """
        Convert QUAD4 elements into TRIA3 elements. If 'idx_convert' is unspecified all QUAD4 in the mesh are converted.
        """
        conn = self.Connectivity
        # Get indices of quad4 elements
        idx_quad = np.where(self.Types == cfs_element_type.QUAD4)[0]
        if idx_convert is not None:
            # Check if all specified indices are quad4 elements
            idx_quad_convert = np.intersect1d(idx_quad, idx_convert)
            if idx_quad_convert.size < idx_convert.size:
                vprint(
                    "Warning: Some element indices are ignored because the element is not of type QUAD4!",
                    verbose=self.Verbosity >= v_def.debug,
                )
        else:
            idx_quad_convert = idx_quad

        if idx_quad_convert.size == 0:
            vprint("No QUAD4 elements found!", verbose=self.Verbosity >= v_def.debug)
            return

        conn_quad = conn[idx_quad_convert, :]
        conn_quad_tria = np.hstack(
            (
                conn_quad[:, (0, 1, 2)],
                np.zeros((conn_quad.shape[0], self.Connectivity.shape[1] - 3), dtype=int),
            )
        )
        conn_tria_add = np.hstack(
            (
                conn_quad[:, (0, 2, 3)],
                np.zeros((conn_quad.shape[0], self.Connectivity.shape[1] - 3), dtype=int),
            )
        )
        idx_tria_add = np.array([i for i in range(conn.shape[0], conn.shape[0] + conn_tria_add.shape[0])])

        self.Connectivity = np.vstack((conn, conn_tria_add))
        self.Connectivity[idx_quad_convert, :] = conn_quad_tria
        self.Types = np.append(self.Types, np.array([cfs_element_type.TRIA3 for i in range(conn_tria_add.shape[0])]))
        self.Types[idx_quad_convert] = cfs_element_type.TRIA3
        self.update_info()

        for reg in self.Regions:
            idx_reg_quad = np.where(np.isin(reg.Elements.flatten(), idx_quad_convert + 1))[0]
            idx_reg_tria_add = np.where(np.isin(idx_quad_convert, reg.Elements[idx_reg_quad] - 1))
            reg.Elements = np.vstack(
                (
                    np.expand_dims(reg.Elements.flatten(), 1),
                    np.expand_dims(idx_tria_add[idx_reg_tria_add] + 1, 1),
                )
            ).flatten()

        # Remove columns containing zeros only
        self.Connectivity = reshape_connectivity(self.Connectivity)

        if result_data is not None:
            # TODO: Adapt element result data
            raise NotImplementedError("Adapting result data not implemented!")
            return result_data

        return None

    def get_region(self, region: str | CFSRegData) -> CFSRegData:
        return list_search(self.Regions, region)

    def get_region_nodes(self, region: str | CFSRegData) -> np.ndarray:
        reg_obj = self.get_region(region=region)
        return reg_obj.Nodes

    def get_region_elements(self, region: str | CFSRegData) -> np.ndarray:
        reg_obj = self.get_region(region=region)
        return reg_obj.Elements

    def get_region_coordinates(self, region: str | CFSRegData) -> np.ndarray:
        reg_obj = self.get_region(region=region)
        return self.Coordinates[reg_obj.Nodes - 1, :]

    def get_region_connectivity(self, region: str | CFSRegData) -> np.ndarray:
        reg_obj = self.get_region(region=region)
        return self.Connectivity[reg_obj.Elements - 1, :]

    def get_region_element_types(self, region: str | CFSRegData) -> np.ndarray:
        reg_obj = self.get_region(region=region)
        return self.Types[reg_obj.Elements - 1]

    def get_region_centroids(self, region: str | CFSRegData, processes: int | None = None) -> np.ndarray:
        reg_obj = self.get_region(region=region)
        return self.get_mesh_centroids(el_idx=reg_obj.Elements - 1, processes=processes)

    def get_closest_node(
        self, coordinate: np.ndarray, region: str | CFSRegData | None = None, eps: float = 1e-3
    ) -> np.ndarray:
        """
        Return node ids of closest nodes to coordinate array.

        Parameters
        ----------

        coordinate: np.ndarray
            Coordinate array (Nx3, N is the number of query points)
        region : str or CFSRegData, optional
            Name of the group/region. The default is ``None``, in which case the global mesh will be used instead.
        eps : float, optional
            Show warning if distance of closest node exceeds the specified value. The default value is ``1e-3``.
        Returns
        -------
        np.ndarray
            Array of node ids (starting from 0) of the closest node to the respective coordinate. If region is passed,
            return region node id, otherwise return global node id.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> search_coord = np.array([0,0,0])
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>>     node_indices = mesh.get_closest_node(search_coord):

        """
        if region is None:
            search_coord = self.Coordinates
        else:
            search_coord = self.get_region_coordinates(region=region)
        search_coord_kdtree = KDTree(search_coord)
        d, idx = search_coord_kdtree.query(coordinate)
        if np.any(d > eps):
            vprint(
                f"Warning: Nearest neighbor distance {np.max(d)} exceeds {eps}",
                verbose=self.Verbosity >= v_def.release,
            )
        return idx

    def get_closest_element(self, coordinate: np.ndarray, region: str | None = None, eps=1e-3) -> np.ndarray:
        """
        Return element ids of closest element centroids to coordinate array.

        Parameters
        ----------

        coordinate: np.ndarray
            Coordinate array (Nx3, N is the number of query points)
        region : str, optional
            Name of the group/region. The default is ``None``, in which case the global mesh will be used instead.
        eps : float, optional
            Show warning if distance of closest node exceeds the specified value. The default value is ``1e-3``.
        Returns
        -------
        np.ndarray
            Array of element ids (starting from 0) of the closest element centroid to the respective coordinate.
            If region is passed, return region element id, otherwise return global element id.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> search_coord = np.array([0,0,0])
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>>     element_indices = mesh.get_closest_element(search_coord):

        """
        if region is None:
            search_conn = self.Connectivity
        else:
            search_conn = self.get_region_connectivity(region=region)

        search_coord = np.zeros((search_conn.shape[0], self.Coordinates.shape[1]))
        # TODO Vectorize
        # Remove columns containing zeros only
        # search_conn = reshape_connectivity(search_conn)
        # el_coord = self.Coordinates[search_conn - 1]
        # search_coord = np.sum(el_coord, axis=1) / el_coord.shape[1]
        for i in np.argwhere(np.any(search_conn[..., :] == 0, axis=1)):
            el_conn = search_conn[i, np.argwhere(search_conn[i, :] != 0)[:, 1]]
            el_coord = self.Coordinates[el_conn - 1]
            search_coord[i, :] = np.sum(el_coord, axis=0) / el_coord.shape[0]

        search_coord_kdtree = KDTree(search_coord)
        d, idx = search_coord_kdtree.query(coordinate)
        if any(d > eps):
            vprint(
                f"Warning: Nearest neighbor distance {max(d)} exceeds {eps}",
                verbose=self.Verbosity >= v_def.release,
            )
        return idx

    def reorient_region(self, region: str | CFSRegData) -> None:
        """
        Reorient elements in a specified region. (AI-generated)

        Parameters
        ----------
        region : str
            Name of the region whose elements need to be reoriented.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>> mesh.reorient_region('region_name')
        """
        if type(region) is str:
            region_obj = list_search(self.Regions, region)
        else:
            region_obj = region
        vprint(
            f"Reorienting elements in region {region_obj.Name}",
            verbose=self.Verbosity >= v_def.more,
        )
        self.reorient_elements(idx_reorient=region_obj.Elements - 1)

    def reorient_elements(self, idx_reorient: List | np.ndarray) -> None:
        """
        Reorient elements based on the element centroid. (AI-generated)

        Parameters
        ----------
        idx_reorient : np.ndarray
            Indices of the elements that need to be reoriented.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>> mesh.reorient_elements(idx_reorient=[0, 1, 2])
        """
        for el_idx in progressbar(
            list(idx_reorient),
            prefix="Reorienting elements: ",
            verbose=self.Verbosity >= v_def.debug,
        ):
            if self.Types[el_idx] == cfs_element_type.LINE2:
                self.Connectivity[el_idx, [0, 1]] = self.Connectivity[el_idx, [1, 0]]
            elif self.Types[el_idx] == cfs_element_type.TRIA3:
                self.Connectivity[el_idx, [0, 1]] = self.Connectivity[el_idx, [1, 0]]
            elif self.Types[el_idx] == cfs_element_type.QUAD4:
                self.Connectivity[el_idx, [1, 3]] = self.Connectivity[el_idx, [3, 1]]
            else:
                raise NotImplementedError(f"Reorienting of element type {self.Types[el_idx]} not implemented!")

    @staticmethod
    def from_coordinates_connectivity(
        coordinates: np.ndarray,
        connectivity: Optional[np.ndarray] = None,
        element_types: Optional[np.ndarray] = None,
        element_dimension: Optional[int] = None,
        region_name="Region",
        verbosity=v_def.release,
    ) -> CFSMeshData:
        """
        Generates data objects to create cfs mesh with one single region containing all elements. Detects element type from
        number of nodes. Therefore, all elements must have same dimension.

        Parameters
        ----------
        coordinates : numpy.ndarray, optional
            Coordinate array (NxD) of the whole mesh (N number of nodes, D space dimension)
        connectivity : numpy.ndarray, optional
            Connectivity array (NxM) of the whole mesh (N number of elements, M maximum number of nodes per element).
            Includes zero entries in case of different element types.
        element_types : numpy.ndarray, optional
            Array of element types (Nx1) of the whole mesh (N number of elements). Default is ``None`` in which case the
            element type is identified based on the number of nodes.
        element_dimension : int, optional
            Dimension of all elements. Default is ``None`` in which case the dimension is chosen based on the coordinates
            parameter
        region_name : str, optional
        verbosity : int, optional
            Verbosity level <=1000 ; see v_def.py for predefined levels. Default is v_def.release.

        Returns
        -------
        pyCFS.data.io.CFSMeshData
            Mesh data structure.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     coordinates = f.Coordinates
        >>>     connectivity = f.Connectivity
        >>>     ElementTypes = f.ElementTypes
        >>>     region_data = f.MeshGroupsRegions
        >>> mesh = CFSMeshData.from_coordinates_connectivity(coordinates=coordinates, connectivity=connectivity,
        >>>                                           element_dimension=3, region_name='region')

        """
        if element_dimension is None:
            element_dimension = coordinates.shape[1]

        if connectivity is None:
            connectivity = np.reshape(np.arange(coordinates.shape[0]) + 1, (coordinates.shape[0], 1))
            type_array = np.array([cfs_element_type.POINT for _ in range(connectivity.shape[0])])

        else:
            connectivity = reshape_connectivity(connectivity)

            if element_types is None:
                type_link = {
                    0: {1: cfs_element_type.POINT},
                    1: {2: cfs_element_type.LINE2, 3: cfs_element_type.LINE3},
                    2: {
                        3: cfs_element_type.TRIA3,
                        6: cfs_element_type.TRIA6,
                        4: cfs_element_type.QUAD4,
                        8: cfs_element_type.QUAD8,
                        9: cfs_element_type.QUAD9,
                    },
                    3: {
                        4: cfs_element_type.TET4,
                        10: cfs_element_type.TET10,
                        8: cfs_element_type.HEXA8,
                        20: cfs_element_type.HEXA20,
                        27: cfs_element_type.HEXA27,
                        5: cfs_element_type.PYRA5,
                        13: cfs_element_type.PYRA13,
                        14: cfs_element_type.PYRA14,
                        6: cfs_element_type.WEDGE6,
                        15: cfs_element_type.WEDGE15,
                        18: cfs_element_type.WEDGE18,
                    },
                }

                type_array = apply_dict_vectorized(
                    data=(connectivity != 0).sum(axis=1),
                    dictionary=type_link[element_dimension],
                    val_no_key=cfs_element_type.UNDEF,
                )
            else:
                type_array = element_types

            connectivity, _ = renumber_connectivity(connectivity)

        reg_node = np.array([i + 1 for i in range(coordinates.shape[0])])
        reg_el = np.array([i + 1 for i in range(connectivity.shape[0])])
        reg_data = [
            CFSRegData(
                name=region_name,
                elements=reg_el,
                nodes=reg_node,
                dimension=np.max(apply_dict_vectorized(dictionary=cfs_types.cfs_element_dimension, data=type_array)),
                verbosity=verbosity,
            )
        ]

        mesh_data = CFSMeshData(
            coordinates=coordinates,
            connectivity=connectivity,
            types=type_array,
            regions=reg_data,
            verbosity=verbosity,
        )

        return mesh_data

    def split_regions_by_connectivity(
        self, result_data: CFSResultData | None = None, regions: list[CFSRegData] | None = None
    ):
        """
        Split regions by connectivity.

        This method splits the regions in the mesh data structure based on their connectivity. It clusters input regions
        into subregions in which all elements are connected.

        Parameters
        ----------
        result_data : CFSResultData, optional
            Result data object. Default is ``None``.
        regions : list[CFSRegData], optional
            List of regions to be split. Default is ``None`` in which case all regions are considered.

        Examples
        --------
        >>> from pyCFS.data.io import CFSReader
        >>> with CFSReader('file.cfs') as f:
        >>>     mesh = f.MeshData
        >>>     result = f.ResultMeshData
        >>> mesh.split_regions_by_connectivity(result_data = result)
        """
        # Find clusters in the connectivity array
        clusters = CFSMeshData._find_clusters(connectivity=self.Connectivity)

        # create new result data arrays
        new_result_data_arrays = []

        if regions is None or len(regions) == 0:
            regions = self.Regions

        # iterate over all source regions
        for i_regions in range(len(regions)):
            print("Processing region:", regions[i_regions].Name)
            # iterate over all clusters
            full_region_node_ids = regions[i_regions].Nodes
            for i_cluster in range(len(clusters)):
                print("Processing cluster:", i_cluster)
                # new region name
                curr_reg_name = f"{regions[i_regions].Name}_{i_cluster}"
                num_digits = len(str(len(clusters)))
                curr_reg_name = f"{regions[i_regions].Name}_{i_cluster:0{num_digits}d}"

                # create new region
                curr_reg_data = CFSRegData(
                    name=curr_reg_name,
                    dimension=regions[i_regions].Dimension,
                    is_group=regions[i_regions].IsGroup,
                    verbosity=self.Verbosity,
                )
                # set clustered elements
                curr_reg_data.Elements = clusters[i_cluster]
                # retrieve nodes from connectivity list
                curr_reg_data.Nodes = np.unique(self.Connectivity[clusters[i_cluster] - 1])
                if curr_reg_data.Nodes[0] == 0:
                    curr_reg_data.Nodes = curr_reg_data.Nodes[1:]
                # add region to mesh data
                self.Regions.append(curr_reg_data)

                if result_data is not None:
                    result_info = result_data.ResultInfo
                    # remove all data not contained in the current cluster region..
                    node_indices = np.where(np.isin(full_region_node_ids, curr_reg_data.Nodes))[0]
                    # loop over result quantities
                    for i_quantity in range(len(result_info)):
                        quant = str(result_info[i_quantity].Quantity)
                        # get the result data array
                        print("Processing quantity:", quant)
                        curr_result_data_array = result_data.get_data_array(
                            region=regions[i_regions].Name, quantity=quant
                        )
                        # remove all data not contained in the region
                        new_result_data_array = CFSResultArray(curr_result_data_array.DataArray[:, node_indices, :])
                        new_result_data_array.MetaData = curr_result_data_array.MetaData
                        # assign the curr region name
                        new_result_data_array.Region = curr_reg_data.Name
                        # collect
                        new_result_data_arrays.append(new_result_data_array)
            # clear the old region
            self.Regions.pop(i_regions)
        if result_data is not None:
            # combine all results into one result data object
            all_new_result_data = CFSResultData(
                analysis_type=new_result_data_arrays[0].AnalysisType, data=new_result_data_arrays
            )
        else:
            all_new_result_data = None
        return all_new_result_data

    @staticmethod
    def _find_clusters(connectivity: np.ndarray, perform_sanity_check: bool = True) -> List[np.ndarray]:
        """
        Find clusters in the connectivity array to separate non-connected regions using a breadth-first search (BFS) algorithm.

        Parameters
        ----------
        connectivity : np.ndarray
            The connectivity array with shape (n, m), where n is the number of elements and m is the maximum number of nodes for each element.
        perform_sanity_check : bool, optional
            Perform a sanity check to ensure that no element id is contained in multiple regions. Default is ``True``.

        Returns
        -------
        list of np.ndarray
            The clusters containing the element ids
        """

        def bfs(start, visited, adjacency_list) -> np.ndarray:
            queue = deque([start])
            cluster = []
            while queue:
                node = queue.popleft()
                if node not in visited:
                    visited.add(node)
                    cluster.append(node)
                    queue.extend(adjacency_list[node])
            return np.array(cluster)

        # Create adjacency list
        adjacency_list = defaultdict(list)
        for element_id, element in enumerate(connectivity):
            for i in range(len(element)):
                if element[i] <= 0:  # Skip padding elements and node number 0
                    continue
                for j in range(i + 1, len(element)):
                    if element[j] <= 0:  # Skip padding elements and node number 0
                        continue
                    adjacency_list[element[i]].append(element[j])
                    adjacency_list[element[j]].append(element[i])

        # Find clusters using BFS
        visited: set[int] = set()
        clusters = []
        for node in adjacency_list:
            if node not in visited:
                cluster = bfs(node, visited, adjacency_list)
                clusters.append(cluster)

        # Map nodes back to element ids
        element_clusters = []
        for cluster in clusters:
            element_cluster = set()
            for node in cluster:
                for element_id, element in enumerate(connectivity):
                    if node in element:
                        element_cluster.add(element_id + 1)  # Adjust element_id to start from 1
            element_clusters.append(np.array(list(element_cluster)))

        # Sanity check: Ensure no element id is contained in multiple regions
        if perform_sanity_check:
            element_id_set = set()
            for cluster in element_clusters:
                for element_id in cluster:
                    if element_id in element_id_set:
                        raise ValueError(f"Clustering Error: Element ID {element_id} is contained in multiple regions")
                    element_id_set.add(element_id)

        print(f"{len(element_clusters)} clusters found in the connectivity list.")

        return element_clusters


class CFSRegData:
    """
    Data structure containing mesh region definition

    .. figure:: ../../../docs/source/resources/data_structures_CFSRegData.png

    Parameters
    ----------
    name : str, optional
        Group/Region name
    elements : numpy.ndarray, optional
        array of element ids (Nx1) of the group/region (N number of elements in the group/region).
    nodes : numpy.ndarray, optional
        array of node ids (Nx1) of the group/region (N number of nodes in the group/region).
    dimension : int, optional
        Group/Region dimension
    is_group : bool, optional
        flag indicating if the entity is a group.
    verbosity : int, optional
        Verbosity level <=1000 ; see v_def.py for predefined levels. Default is v_def.release.

    Attributes
    ----------
    Name : str
        Group/Region name
    Elements : numpy.ndarray
        array of element ids, starting from 1, (Nx1) of the group/region (N number of elements in the group/region).
    Nodes : numpy.ndarray
        array of node ids, starting from 1, (Nx1) of the group/region (N number of nodes in the group/region).
    Dimension : int
        Group/Region dimension
    IsGroup : bool
        flag indicating if the entity is a group.

    Notes
    -----
    -  ``merge`` Merges region with other region removing duplicate node/element indices

    -  ``update_nodes_from_elements`` Update region nodes based on element ids.

    Examples
    --------
    >>> from pyCFS.data.io import CFSReader, CFSMeshInfo
    >>> with CFSReader('file.cfs') as f:
    >>>     coordinates = f.Coordinates
    >>>     connectivity = f.Connectivity
    >>>     ElementTypes = f.ElementTypes
    >>>     region_data = f.MeshGroupsRegions
    >>> mesh = CFSMeshData(coordinates=coordinates, connectivity=connectivity, ElementTypes=ElementTypes,
    >>>                    regions=region_data)

    """

    def __init__(
        self,
        name: str,
        elements=np.empty(0),
        nodes=np.empty(0),
        dimension=-1,
        is_group=False,
        verbosity=v_def.release,
    ):
        self._Elements = np.empty(0)
        self._Nodes = np.empty(0)

        self.Name = name
        self.Elements = elements
        self.Nodes = nodes
        self.Dimension: int = dimension
        self.IsGroup: bool = is_group
        self.Verbosity = verbosity

    @property
    def Nodes(self):
        return self._Nodes

    @Nodes.setter
    def Nodes(self, nodes: np.ndarray):
        self._Nodes = np.array(nodes, dtype=np.uint32).flatten()  # type: ignore

    @property
    def Elements(self):
        return self._Elements

    @Elements.setter
    def Elements(self, elements: np.ndarray):
        self._Elements = np.array(elements, dtype=np.int32).flatten()  # type: ignore

    def __repr__(self) -> str:
        if self.IsGroup:
            reg_type = "Group"
        else:
            reg_type = "Region"
        return f"{reg_type}: {self.Name}"

    def __str__(self) -> str:
        if self.IsGroup:
            reg_type = "Group "
        else:
            reg_type = "Region"
        return textwrap.dedent(
            f"{reg_type}: {self.Name} ({self.Dimension}D, {self.Nodes.size} nodes, {self.Elements.size} elements)"
        )

    def __eq__(self, other: object | str):
        if not isinstance(other, CFSRegData):
            if type(other) is str:
                return self.Name == other
            else:
                raise NotImplementedError("Object comparison implemented for CFSRegData and str only!")
        return all(
            [
                self.Name == other.Name,
                np.array_equal(self.Elements, other.Elements),
                np.array_equal(self.Nodes, other.Nodes),
                self.Dimension == other.Dimension,
            ]
        )

    def __lt__(self, other):
        if not isinstance(other, CFSRegData):
            raise NotImplementedError("Object comparison implemented for CFSRegData and str only!")
        else:
            return self.Name < other.Name

    def __add__(self, other: CFSRegData):
        return_data, _, _ = self.merge(other)
        return return_data

    def merge(self, other: CFSRegData):
        """
        Merges region with other region removing duplicate node/element indices
        """
        # TODO add method to manipulate data after region merge
        if type(other) is not CFSRegData:
            raise NotImplementedError("Addition of CFSRegData only implemented with other object of type CFSRegData!")
        merged_region = CFSRegData(self.Name, verbosity=self.Verbosity)
        merged_region.Dimension = max(self.Dimension, other.Dimension)
        merged_region.IsGroup = self.IsGroup
        if other.IsGroup != self.IsGroup:
            p_dict = {False: "region", True: "group"}
            vprint(
                f"Merging {p_dict[self.IsGroup]} with {p_dict[other.IsGroup]} into {p_dict[merged_region.IsGroup]}",
                verbose=self.Verbosity > v_def.release,
            )
        merged_region.Nodes, idx_node = np.unique(np.append(self.Nodes, other.Nodes), return_index=True)
        merged_region.Elements, idx_elem = np.unique(np.append(self.Elements, other.Elements), return_index=True)

        return merged_region, idx_node, idx_elem

    def update_nodes_from_connectivity(
        self, connectivity: np.ndarray, elems: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray | None, np.ndarray | None]:
        """
        Update region nodes based on element ids.

        Parameters
        ----------
        connectivity: numpy.ndarray
        elems : numpy.ndarray, optional

        Returns
        -------
        node_idx : numpy.ndarray
            Updated node indices (starting from 0)
        elem_idx : numpy.ndarray
            Updated element indices (starting from 0)

        """
        if elems is None:
            elems = self.Elements

        reg_conn = connectivity[elems - 1, :]
        nodes = np.unique(reg_conn)
        # Remove zero entry
        nodes = np.delete(nodes, np.where(nodes == 0)[0])

        node_idx = None
        if np.all(np.isin(nodes, self.Nodes)):
            _, idx_intersect, node_idx = np.intersect1d(nodes, self.Nodes, return_indices=True)
            nodes = nodes[idx_intersect]

        elem_idx = None
        if np.all(np.isin(elems, self.Elements)):
            _, idx_intersect, elem_idx = np.intersect1d(elems, self.Elements, return_indices=True)
            elems = elems[idx_intersect]

        self.Nodes = nodes
        self.Elements = elems

        return node_idx, elem_idx


# Usability functions
def _compute_mesh_node_normal(node_idx: int, connectivity: np.ndarray, coordinates: np.ndarray) -> np.ndarray:
    """
    Helper function for CFSMeshData.get_surface_normals. Computes node surface normal for single node in mesh.

    Parameters
    ----------
    node_idx : int
    connectivity : np.ndarray
    coordinates : np.ndarray

    Returns
    -------
    np.ndarray

    """
    el_idx = np.argwhere(np.any(connectivity == node_idx + 1, axis=1)).flatten()
    node_close_ids = connectivity[el_idx, :]
    # Put center node id in 1st position
    node_neighbor_ids = np.empty_like(node_close_ids, dtype=int)
    for row in range(node_neighbor_ids.shape[0]):
        neighbor_n_idx = np.argwhere(node_close_ids[row, :] != node_idx + 1).flatten()
        # Ensure consistent node sequence (23,13->31,12), when common node is 2nd node in connectivity
        if (node_close_ids[row, :] == node_idx + 1)[1]:
            neighbor_n_idx[:2] = np.array([2, 0])
        node_neighbor_ids[row, 1:] = node_close_ids[row, neighbor_n_idx]
        node_neighbor_ids[row, 0] = node_idx + 1
    neighbor_coord = coordinates[node_neighbor_ids - 1, 0:3]
    return node_normal_2d(neighbor_coord)


def _compute_mesh_quality(
    idx: int, connectivity: np.ndarray, coordinates: np.ndarray, el_types: np.ndarray, metric: str
):
    """Helper function for CFSMeshData._get_mesh_quality. Computes element quality for single element in mesh"""
    element_connectivity = connectivity[idx, :]
    # Remove 0 entries
    idx_zeros = np.argwhere(element_connectivity == 0)
    element_connectivity = np.delete(element_connectivity, idx_zeros)
    element_coordinates = coordinates[element_connectivity - 1, :]
    return element_quality(element_coordinates, cfs_element_type(el_types[idx]), metric=metric)
