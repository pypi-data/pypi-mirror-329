import numpy as np

from pyCFS.data.io import CFSReader, cfs_types, CFSWriter, CFSResultData
from pyCFS.data.operators import interpolators, transformation, sngr
from .pycfs_data_fixtures import dummy_CFSMeshData_obj


def test_transformation_fit_coordinates(working_directory="."):
    from pyCFS.data.operators.transformation import fit_coordinates

    filename_src = f"{working_directory}/tests/data/operators/transformation/fit_geometry/fit_geometry_src.cfs"
    filename_target = f"{working_directory}/tests/data/operators/transformation/fit_geometry/fit_geometry_target.cfs"
    filename_out = f"{working_directory}/tests/data_tmp/operators/transformation/fit_geometry/fit_geometry_out.cfs"

    regions_target = ["HULL_TARGET"]
    regions_fit = ["surface"]

    transform_param_init = [0.02, 0.1, 0.07, 0, 150, 0]

    while len(transform_param_init) < len(regions_fit) * 6:
        transform_param_init.extend([0, 0, 0, 0, 0, 0])

    fit_coordinates(
        filename_src,
        filename_out,
        filename_target,
        regions_target=regions_target,
        regions_fit=regions_fit,
        transform_param_init=transform_param_init,
        init_angle_degree=True,
    )


def test_transformation_transform_mesh_only(working_directory="."):
    from pyCFS.data.operators.transformation import transform_mesh

    filename_src = (
        f"{working_directory}/tests/data/operators/transformation/transform_mesh_only/transform_mesh_only_src.cfs"
    )
    filename_out = (
        f"{working_directory}/tests/data_tmp/operators/transformation/transform_mesh_only/transform_mesh_only_out.cfs"
    )

    transform_regions = ["domain2"]
    translate_coords = (0.05, 0.1, 0.2)
    rotate_angles = (45, 35, 75)
    rotate_origin = (1, 1.5, 1.9)

    transform_mesh(
        filename_src,
        filename_out,
        translate_coords=translate_coords,
        rotate_angles=rotate_angles,
        rotate_origin=rotate_origin,
        regions=transform_regions,
        transform_results=False,
    )


def test_transformation_transform_mesh_with_results(working_directory="."):
    from pyCFS.data.operators.transformation import transform_mesh

    filename_src = f"{working_directory}/tests/data/operators/transformation/transform_mesh_with_results/transform_mesh_with_results_src.cfs"
    filename_out = f"{working_directory}/tests/data_tmp/operators/transformation/transform_mesh_with_results/transform_mesh_with_results_out.cfs"

    transform_regions = ["domain2"]
    translate_coords = (0.05, 0.1, 0.2)
    rotate_angles = (45, 35, 75)
    rotate_origin = (0, 0, 0)

    transform_mesh(
        filename_src,
        filename_out,
        translate_coords=translate_coords,
        rotate_angles=rotate_angles,
        rotate_origin=rotate_origin,
        regions=transform_regions,
        transform_results=True,
    )


def test_interpolators_cell2node_node2cell(working_directory="."):
    file_in = f"{working_directory}/tests/data/operators/interpolators/interpolators.cfs"
    file_out = f"{working_directory}/tests/data_tmp/operators/interpolators/cell2node_node2cell.cfs"

    quantity = "quantity"
    reg_name = "Vol"
    with CFSReader(file_in) as h5r:
        mesh_data = h5r.MeshData
        result_data_read = h5r.ResultMeshData

        reg_coord = h5r.get_mesh_region_coordinates(reg_name)
        reg_conn = h5r.get_mesh_region_connectivity(reg_name)

    m_interp = interpolators.interpolation_matrix_node_to_cell(reg_coord, reg_conn)
    r_array = result_data_read.get_data_array(quantity, reg_name, cfs_types.cfs_result_type.NODE)
    r_array_N2C = interpolators.apply_interpolation(
        result_array=r_array,
        interpolation_matrix=m_interp,
        restype_out=cfs_types.cfs_result_type.ELEMENT,
        quantity_out="quantity_N2C",
    )

    m_interp = interpolators.interpolation_matrix_cell_to_node(reg_coord, reg_conn).tocsr()

    r_array_C2N = interpolators.apply_interpolation(
        result_array=r_array_N2C,
        interpolation_matrix=m_interp,
        restype_out=cfs_types.cfs_result_type.NODE,
        quantity_out="quantity_C2N",
    )

    result_data_write = CFSResultData(
        analysis_type=cfs_types.cfs_analysis_type.TRANSIENT, data=[r_array_C2N, r_array_N2C]
    )

    with CFSWriter(file_out) as h5w:
        h5w.create_file(mesh_data, result_data_write)


def test_interpolators_nearest_neighbor_elem(working_directory="."):
    # TODO Unit test for Nearest Neighbor interpolation
    # NN Elem -> Elem example

    source_file = f"{working_directory}/tests/data/operators/interpolators/nn_elem.cfs"
    interpolated_sim = f"{working_directory}/tests/data_tmp/operators/interpolators/nn_elem_interp.cfs"

    quantity = "acouIntensity"
    region_src_target_dict = {"internal": ["internal"]}

    with CFSReader(source_file) as h5r:
        result_data_src = h5r.ResultMeshData
        mesh_data_src = h5r.MeshData

    with CFSReader(source_file) as h5r:
        mesh_data = h5r.MeshData

    result_array_lst_nn = []
    for src_region_name in region_src_target_dict:
        source_coord = mesh_data_src.get_region_centroids(src_region_name)

        target_coord = []
        for reg_name in region_src_target_dict[src_region_name]:
            target_coord.append(mesh_data.get_region_centroids(reg_name))

        for i, reg_name in enumerate(region_src_target_dict[src_region_name]):
            m_interp = interpolators.interpolation_matrix_nearest_neighbor(
                source_coord,
                target_coord[i],
                num_neighbors=1,
                interpolation_exp=1,
                max_distance=1e-6,
                formulation="forward",
            )
            m_interp = interpolators.interpolation_matrix_nearest_neighbor(
                source_coord, target_coord[i], num_neighbors=1, max_distance=1e-6, formulation="backward"
            )
            result_array_src = result_data_src.get_data_array(
                quantity=quantity, region=src_region_name, restype=cfs_types.cfs_result_type.ELEMENT
            )
            result_array_lst_nn.append(
                interpolators.apply_interpolation(
                    result_array=result_array_src,
                    interpolation_matrix=m_interp,
                    region_out=reg_name,
                    restype_out=cfs_types.cfs_result_type.ELEMENT,
                )
            )

    result_data_disp = CFSResultData(analysis_type=cfs_types.cfs_analysis_type.TRANSIENT, data=result_array_lst_nn)

    with CFSWriter(interpolated_sim) as h5w:
        h5w.create_file(mesh_data, result_data_disp)


def test_interpolators_nearest_neighbor_node(working_directory="."):
    # NN Example
    source_file = f"{working_directory}/tests/data/operators/interpolators/nn_source.cfs"
    target_file = f"{working_directory}/tests/data/operators/interpolators/nn_target.cfs"
    out_file = f"{working_directory}/tests/data_tmp/operators/interpolators/nn_interpolated.cfs"

    quantity = "function"
    reg_name_source = "S_source"
    reg_name_target = ["S_target"]

    with CFSReader(source_file) as h5r:
        result_data_src = h5r.ResultMeshData
        source_coord = h5r.get_mesh_region_coordinates(reg_name_source)

    with CFSReader(target_file) as h5r:
        mesh_data = h5r.MeshData
        target_coord = []
        for reg_name in reg_name_target:
            target_coord.append(h5r.get_mesh_region_coordinates(reg_name))

    result_array_lst_nn = []
    result_array_lst_nn_inverse = []
    for i, reg_name in enumerate(reg_name_target):
        m_interp = interpolators.interpolation_matrix_nearest_neighbor(
            source_coord, target_coord[i], num_neighbors=10, interpolation_exp=2
        )
        m_interp_inverse = interpolators.interpolation_matrix_nearest_neighbor(
            source_coord, target_coord[i], num_neighbors=10, interpolation_exp=2, formulation="backward"
        )
        result_array_src = result_data_src.get_data_array(
            quantity=quantity, region=reg_name_source, restype=cfs_types.cfs_result_type.NODE
        )
        result_array_lst_nn.append(
            interpolators.apply_interpolation(
                result_array=result_array_src,
                interpolation_matrix=m_interp,
                quantity_out=f"{quantity}_interpolated",
                region_out=reg_name,
                restype_out=cfs_types.cfs_result_type.NODE,
            )
        )
        result_array_lst_nn_inverse.append(
            interpolators.apply_interpolation(
                result_array=result_array_src,
                interpolation_matrix=m_interp_inverse,
                quantity_out=f"{quantity}_interpolated_inverse",
                region_out=reg_name,
                restype_out=cfs_types.cfs_result_type.NODE,
            )
        )

    result_data_write = CFSResultData(
        cfs_types.cfs_analysis_type.TRANSIENT, data=result_array_lst_nn + result_array_lst_nn_inverse
    )

    with CFSWriter(out_file) as h5w:
        h5w.create_file(mesh_data=mesh_data, result_data=result_data_write)


def test_interpolators_interpolate_nearest_neighbor(working_directory="."):
    source_file = f"{working_directory}/tests/data/operators/interpolators/nn_source.cfs"
    target_file = f"{working_directory}/tests/data/operators/interpolators/nn_target.cfs"
    out_file = f"{working_directory}/tests/data_tmp/operators/interpolators/nn_interpolated.cfs"

    quantities = ["function"]

    region_src_target = [
        {"source": ["S_source"], "target": ["S_target"]},
    ]

    with CFSReader(source_file) as h5r:
        src_mesh = h5r.MeshData
        src_data = h5r.ResultMeshData
    with CFSReader(target_file) as h5r:
        target_mesh = h5r.MeshData

    result_data_write = interpolators.interpolate_nearest_neighbor(
        mesh_src=src_mesh,
        data_src=src_data,
        mesh_target=target_mesh,
        region_src_target=region_src_target,
        quantity_names=quantities,
        element_centroid_data_target=True,
    )

    with CFSReader(target_file) as h5r:
        mesh_data = h5r.MeshData

    with CFSWriter(out_file) as h5w:
        h5w.create_file(mesh_data=mesh_data, result_data=result_data_write)


def test_interpolators_interpolate_distinct_nodes_nearest_neighbor(working_directory="."):
    """
    Interpolates nodes on a straight line in the center of a plate.
    """
    source_file = f"{working_directory}/tests/data/operators/interpolators/nn_source.cfs"
    ref_file = f"{working_directory}/tests/data/operators/interpolators/nn_distinct_interpolated.cfs"
    quantity = "function"
    regions = ["S_source"]
    interpolate_node_ids = list(np.arange(start=211, stop=232, step=1))
    # load source file
    with CFSReader(source_file) as h5r:
        src_mesh = h5r.MeshData
        src_data = h5r.ResultMeshData
    # interpolate
    result_data_write = interpolators.interpolate_distinct_nodes(
        mesh_data=src_mesh,
        result_data=src_data,
        quantity_name=quantity,
        interpolate_node_ids=interpolate_node_ids,
        regions=regions,
        num_neighbors=400,
        interpolation_exp=0.0001,
        max_distance=None,
    )
    # load reference file and compare
    with CFSReader(ref_file) as h5r:
        ref_data = h5r.ResultMeshData
    np.testing.assert_array_almost_equal(ref_data.Data, result_data_write.Data, decimal=15)


def test_projection_interpolation(working_directory="."):
    from pyCFS.data.operators.projection_interpolation import interpolate_region

    file_src = f"{working_directory}/tests/data/operators/projection_interpolation/source.cfs"
    file_target = f"{working_directory}/tests/data/operators/projection_interpolation/target.cfs"
    region_src_target_dict = {
        "IFs_mount_inlet": ["IFs_mount_inlet"],
        "IF_pipe_outer": ["IF_pipe_outer"],
    }

    quantity_name = "mechVelocity"

    file_out = f"{working_directory}/tests/data_tmp/operators/projection_interpolation/data_interpolated.cfs"

    return_data = interpolate_region(
        file_src=file_src,
        file_target=file_target,
        region_src_target_dict=region_src_target_dict,
        quantity_name=quantity_name,
        dim_names=["x", "y", "z"],
        is_complex=True,
        projection_direction=None,
        max_projection_distance=5e-3,
        search_radius=5e-2,
    )

    with CFSReader(file_target) as h5reader:
        target_mesh = h5reader.MeshData

    # Create output and write interpolated data
    with CFSWriter(file_out) as h5writer:
        h5writer.create_file(mesh_data=target_mesh, result_data=return_data)


def test_sngr(working_directory="."):
    processes = None
    processes_max = 4
    mem_max = 4  # in GB

    # Constants
    C_mu = 0.09  # (2.46)
    vkp_scaling_const = 1.452762113  # (2.62)

    # Parameters
    eps_orthogonal = 1e-9  # orthogonality check

    delta_t = 1e-4  # Dt
    num_steps = 10  # I
    num_modes = 20  # N
    length_scale_factor = 1.0  # fL
    kin_viscosity = 1.48e-5  # nu
    crit_tke_percentage = 0.5  # beta_k_crit
    max_wave_number_percentage = 100  # beta_K_max
    min_wave_number_percentage = 0.01  # beta_K_min

    file_rans = f"{working_directory}/tests/data/operators/sngr/orifice.cfs"

    with CFSReader(filename=file_rans) as reader:
        mesh_data = reader.MeshData
        result_data = reader.ResultMeshData

    file_reference = f"{working_directory}/tests/data/operators/sngr/orifice_sngr.cfs"
    with CFSReader(filename=file_reference) as reader:
        result_reference = reader.ResultMeshData

    region_list = [
        "fluid",
    ]

    data_on_elems = True

    for reg_name in region_list:
        print(f" - Process region: {reg_name}")

        if data_on_elems:
            coords = mesh_data.get_region_centroids(region=reg_name, processes=processes)
        else:
            coords = mesh_data.get_region_coordinates(region=reg_name)

        mean_velocity = result_data.get_data_array(quantity="U", region=reg_name).squeeze()
        tke = result_data.get_data_array(quantity="k", region=reg_name).squeeze()
        tdr = result_data.get_data_array(quantity="epsilon", region=reg_name).squeeze()

        u_prime, timesteps = sngr.compute_stochastic_velocity_fluctuations(
            coords,
            mean_velocity=mean_velocity,
            tke=tke,
            tdr=tdr,
            C_mu=C_mu,
            vkp_scaling_const=vkp_scaling_const,
            length_scale_factor=length_scale_factor,
            kin_viscosity=kin_viscosity,
            crit_tke_percentage=crit_tke_percentage,
            max_wave_number_percentage=max_wave_number_percentage,
            min_wave_number_percentage=min_wave_number_percentage,
            num_modes=num_modes,
            num_steps=num_steps,
            delta_t=delta_t,
            eps_orthogonal=eps_orthogonal,
            rn_gen=np.random.default_rng(seed=1),
            processes=processes,
            mem_max=mem_max,
            processes_max=processes_max,
            flag_debug=True,
        )

        u_prime_reference = result_reference.get_data_array(quantity="fluctFluidMechVelocity", region=reg_name)

        np.testing.assert_array_almost_equal(
            u_prime, u_prime_reference, decimal=9, err_msg="SNRG velocity fluctuation not equal"
        )


def test_transformation_extrude_mesh_region(dummy_CFSMeshData_obj):
    mesh_extrude, _ = transformation.extrude_mesh_region(
        mesh=dummy_CFSMeshData_obj,
        region="Surf1",
        created_region="Surf1_extrude",
        extrude_vector=np.array([0.5, 0, 0]),
        num_layers=2,
    )

    coord_ref = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 1.0],
            [0.25, 0.0, 0.0],
            [0.25, 0.0, 1.0],
            [0.25, 1.0, 0.0],
            [0.25, 1.0, 1.0],
            [0.5, 0.0, 0.0],
            [0.5, 0.0, 1.0],
            [0.5, 1.0, 0.0],
            [0.5, 1.0, 1.0],
        ]
    )

    conn_ref = np.array(
        [
            [1, 2, 3, 5, 6, 7],
            [2, 4, 3, 6, 8, 7],
            [5, 6, 7, 9, 10, 11],
            [6, 8, 7, 10, 12, 11],
        ]
    )

    np.testing.assert_array_equal(mesh_extrude.Coordinates, coord_ref)
    np.testing.assert_array_equal(mesh_extrude.Connectivity, conn_ref)


def test_transformation_revolve_mesh_region(dummy_CFSMeshData_obj):
    dummy_CFSMeshData_obj.Coordinates = transformation.transform_coord(
        arg=np.array([0, 1.0, 0, 0, 0, 0]), coord=dummy_CFSMeshData_obj.Coordinates
    )

    mesh_revolve, _ = transformation.revolve_mesh_region(
        mesh=dummy_CFSMeshData_obj,
        region="Surf1",
        created_region="Surf1_revolve",
        revolve_axis=np.array([0, 0, 1.0]),
        revolve_angle=2 * np.pi,
        num_layers=4,
    )

    coord_ref = np.array(
        [
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 1.0],
            [0.0, 2.0, 0.0],
            [0.0, 2.0, 1.0],
            [-1.0, 0, 0.0],
            [-1.0, 0.0, 1.0],
            [-2.0, 0.0, 0.0],
            [-2.0, 0.0, 1.0],
            [0.0, -1.0, 0.0],
            [0.0, -1.0, 1.0],
            [0.0, -2.0, 0.0],
            [0.0, -2.0, 1.0],
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [2.0, 0.0, 0.0],
            [2.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 1.0],
            [0.0, 2.0, 0.0],
            [0.0, 2.0, 1.0],
        ]
    )
    conn_ref = np.array(
        [
            [1, 2, 3, 5, 6, 7],
            [2, 4, 3, 6, 8, 7],
            [5, 6, 7, 9, 10, 11],
            [6, 8, 7, 10, 12, 11],
            [9, 10, 11, 13, 14, 15],
            [10, 12, 11, 14, 16, 15],
            [13, 14, 15, 1, 2, 3],
            [14, 16, 15, 2, 4, 3],
        ]
    )

    np.testing.assert_array_almost_equal(mesh_revolve.Coordinates, coord_ref, decimal=15)
    np.testing.assert_array_equal(mesh_revolve.Connectivity, conn_ref)
