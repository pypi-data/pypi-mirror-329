"""
Module containing utility functions for io submodule
"""

import numpy as np
from typing import Optional

from pyCFS.data import v_def
from pyCFS.data import io
from pyCFS.data.io import CFSResultArray
from pyCFS.data.io.cfs_types import (
    cfs_element_type,
    cfs_analysis_type,
    cfs_result_type,
    cfs_history_types,
    cfs_result_definition,
)
from pyCFS.data.util import vprint


def check_mesh(mesh: io.CFSMeshData) -> bool:
    """
    Check mesh data for consistency and validity.

    Parameters
    ----------
    mesh: CFSMeshData
        Mesh data object to be checked.

    Returns
    -------
    bool
        True if mesh data is valid, raises AssertionError otherwise.

    """
    vprint("Checking mesh", verbose=mesh.Verbosity >= v_def.debug)
    # Check connectivity
    assert (
        np.max(mesh.Connectivity) <= mesh.MeshInfo.NumNodes
    ), f"Connectivity idx {np.max(mesh.Connectivity)} exceeds number of nodes {mesh.MeshInfo.NumNodes}."
    assert (
        mesh.Connectivity.shape[0] == mesh.MeshInfo.NumElems
    ), f"Connectivity element count ({mesh.Connectivity.shape[0]}) mismatch with element types array ({mesh.MeshInfo.NumElems})."

    # Check element types

    possible_types = [etype.value for etype in cfs_element_type]

    assert np.all(np.isin(mesh.Types, possible_types)), "Invalid element type found in Types array."

    # Check regions
    for reg in mesh.Regions:
        assert (
            np.max(reg.Nodes) <= mesh.MeshInfo.NumNodes
        ), f"Region {reg.Name} has invalid node index {np.max(reg.Nodes)}."
        assert (
            np.max(reg.Elements) <= mesh.MeshInfo.NumElems
        ), f"Region {reg.Name} has invalid element index {np.max(reg.Elements)}."

        reg_con = mesh.get_region_connectivity(reg)

        assert np.all(
            np.isin(reg_con[reg_con != 0].flatten(), reg.Nodes)
        ), f"Region {reg.Name} has incomplete Node id definition."
        assert np.all(
            np.isin(reg.Nodes, reg_con)
        ), f"Region {reg.Name} has Node ids defined that are not contained in any region element."

    return True


def check_result(result: io.CFSResultData, mesh: Optional[io.CFSMeshData] = None) -> bool:
    """
    Check result data for consistency and validity.

    Parameters
    ----------
    result: CFSResultData
        Result data object to be checked.
    mesh: CFSMeshData, optional
        Mesh data object to check result data array shapes against.

    Returns
    -------
    bool
        True if result data is valid, raises AssertionError otherwise.

    """
    vprint("Checking result", verbose=result._Verbosity >= v_def.debug)
    # Check analysis type
    possible_types = [atype.value for atype in cfs_analysis_type]

    assert result.AnalysisType in possible_types, "Invalid analysis type."

    # StepValues
    for item in result.Data:
        np.testing.assert_array_equal(item.StepValues, result.StepValues, err_msg="StepValues mismatch.")

    # Data arrays
    for item in result.Data:
        assert item.shape[0] == result.StepValues.size, f"Data array {item.ResultInfo} mismatch with number of steps."

        check_result_array(result_array=item, mesh=mesh)

        if cfs_history_types[item.ResType] == cfs_result_definition.HISTORY:
            ndim = 2
        else:
            ndim = 3

        assert item.ndim == ndim, f"Data array {item.ResultInfo} has invalid number of dimensions."
        assert item.shape[-1] == len(
            item.DimNames
        ), f"Data array {item.ResultInfo} dimension label mismatch with number of data dimensions."

    if mesh is None:
        vprint("Data array shapes not checked due to missing mesh data.", verbose=result._Verbosity >= v_def.debug)

    return True


def check_result_array(result_array: CFSResultArray, mesh: Optional[io.CFSMeshData] = None) -> bool:
    """
    Check result array for consistency and validity.

    Parameters
    ----------
    result_array: CFSResultArray
        Result array object to be checked.
    mesh: CFSMeshData, optional
        Mesh data object to check result array shapes against.

    Returns
    -------
    bool
        True if result array is valid, raises AssertionError otherwise.

    """
    if cfs_history_types[result_array.ResType] == cfs_result_definition.HISTORY:
        ndim = 2
    else:
        ndim = 3

    assert result_array.ndim == ndim, f"Data array {result_array.ResultInfo} has invalid number of dimensions."
    assert result_array.shape[-1] == len(
        result_array.DimNames
    ), f"Data array {result_array.ResultInfo} dimension label mismatch with number of data dimensions."
    assert result_array.shape[0] == len(
        result_array.StepValues
    ), f"Data array {result_array.ResultInfo} step values mismatch with number of steps."

    if mesh is not None:
        assert (
            result_array.Region in mesh.Regions
        ), f"Data array {result_array.ResultInfo} region not found in mesh regions {[reg.Name for reg in mesh.Regions]}."
        item_reg = mesh.get_region(result_array.Region)
        if result_array.ResType == cfs_result_type.NODE:
            assert (
                result_array.shape[1] == item_reg.Nodes.size
            ), f"Data array {result_array.ResultInfo} mismatch of number of data points ({result_array.shape[1]}) with region nodes ({item_reg.Name}: {item_reg.Nodes.size})"  # noqa : E501
        if result_array.ResType == cfs_result_type.ELEMENT:
            assert (
                result_array.shape[1] == item_reg.Elements.size
            ), f"Data array {result_array.ResultInfo} mismatch of number of data points ({result_array.shape[1]}) with region elements ({item_reg.Name}: {item_reg.Elements.size})"  # noqa : E501

    return True
