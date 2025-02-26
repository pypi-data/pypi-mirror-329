import random
import time

import numpy as np
import pytest

from pyCFS.data.io.cfs_types import cfs_element_type
from pyCFS.data.util import (
    trilateration,
    element_quality,
    progressbar,
    connectivity_list_to_matrix,
    element_normal_2d,
    node_normal_2d,
    compare_coordinate_arrays,
    TimeRecord,
)


def test_trilateration():
    A = np.array([1, 1, 2])
    B = np.array([4, 7, 2])
    C = np.array([0, -2, 4])
    P = np.array([1, 2, 3])

    R1 = np.linalg.norm(P - A)
    R2 = np.linalg.norm(P - B)
    R3 = np.linalg.norm(P - C)

    print(trilateration(A, B, C, R1, R2, R3))


def test_element_normal():
    coord = np.array([[1, 1, 1], [2, 3, 1], [1, 4, 1], [-1, 2, 1]], dtype=float)
    normal_vec = element_normal_2d(coord)
    np.testing.assert_array_equal(normal_vec, np.array([0, 0, 1.0]))

    coord = np.tile(coord, (3, 1, 1))
    normal_vec = element_normal_2d(coord)
    np.testing.assert_array_equal(normal_vec, np.tile(np.array([0, 0, 1.0]), (3, 1)))


def test_node_normal():
    coord = np.array(
        [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
        ]
    )
    conn = np.array(
        [
            [2, 3, 1],
            [2, 4, 3],
        ]
    )

    np.testing.assert_array_equal(node_normal_2d(element_coordinates=coord[conn - 1]), np.array([-1.0, 0, 0]))


def test_element_quality():
    A = np.array([1, 1, 2])
    B = np.array([4, 7, 2])
    C = np.array([0, -2, 4])
    P = np.array([1, 2, 3])

    coordinates = np.array([A, B, C])
    connectivity = np.array([[1, 2, 3, 0]])

    el_conn = connectivity[0, :]
    print(element_quality(coordinates[el_conn[:3] - 1, :], cfs_element_type.TRIA3, metric="skewness"))
    print(element_quality(coordinates[el_conn[:3] - 1, :], cfs_element_type.TRIA3, metric="quality"))

    coordinates = np.array([A, B, C, P])
    connectivity = np.array([[1, 2, 3, 4]])
    el_conn = connectivity[0, :]
    print(element_quality(coordinates[el_conn[:4] - 1, :], cfs_element_type.TET4, metric="quality"))


def test_progressbar():

    for _ in progressbar([]):
        pass

    for _ in progressbar(range(40), "loop progress"):
        time.sleep(2e-2 * random.random())


def test_connectivity_list_to_matrix():

    conn_list = np.array(
        [
            1,
            2,
            15,
            22,
            3,
            4,
            16,
            23,
            62,
            66,
            101,
            64,
            67,
            71,
            103,
            69,
            63,
            65,
            100,
            116,
            3,
            4,
            16,
            23,
            5,
            6,
            17,
            24,
            67,
            71,
            103,
            69,
            72,
            76,
            105,
            74,
            68,
            70,
            102,
            117,
            5,
            6,
            17,
            24,
            7,
            8,
            18,
            25,
            72,
            76,
            105,
            74,
            77,
            81,
            107,
            79,
            73,
            75,
            104,
            118,
            7,
        ]
    )
    offset = np.array([0, 20, 40, 60])

    conn = connectivity_list_to_matrix(connectivity_list=conn_list, offsets=offset, verbose=True)
    print(conn)


def test_compare_coordinate_arrays():
    arr1 = np.array([[1.0, 2.0, 3.0], [4.1, 5.2, 6.1], [7.0, 8.0, 9.0]])
    arr2 = np.array([[7.05, 8.02, 9.01], [1.02, 2.03, 3.01], [10.0, 11.0, 12.0]])
    arr3 = np.array([[1.0, 2.0, 3.0], [7.02, 8.01, 9.03], [0.0, 0.0, 0.0]])
    arrays = [arr1, arr2, arr3]
    eps = 0.05
    indices = compare_coordinate_arrays(arrays, eps)
    assert indices == [np.array([0]), np.array([1]), np.array([0])]


def test_TimeRecord():
    with TimeRecord(message="Run function", single_line=True):
        time.sleep(1e-2)

    with TimeRecord(message="Run function"):
        time.sleep(1e-2)
        print("do stuff")

    with TimeRecord(message="Run function", single_line=False) as t_rec:
        print("do stuff")
        time.sleep(1e-2)
        print(f"Time elapsed: {t_rec.TimeElapsed}")
        print("do more stuff")
        time.sleep(1e-2)
