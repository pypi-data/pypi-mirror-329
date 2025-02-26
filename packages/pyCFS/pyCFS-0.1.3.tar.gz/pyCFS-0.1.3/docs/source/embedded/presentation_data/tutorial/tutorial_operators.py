#%% 
# Import necessary modules
from pyCFS.data import io
from pyCFS.data.operators import interpolators

#%% 
# Read source file
with io.CFSReader(filename="file.cfs") as h5r:
    print(h5r)
    mesh = h5r.MeshData
    results = h5r.MultiStepData

#%% 
# Perform interpolation
results_interpolated = interpolators.interpolate_node_to_cell(
    mesh_data=mesh,
    result_data=results,
    regions=["V_air"],
    quantity_names={"elecPotential": "interpolated_elecPotential"},
)

#%% 
# Add interpolated result to results container
results.combine_with(results_interpolated)

# Check results container
print(results)

#%% 
# Write output file
with io.CFSWriter("file_out.cfs") as h5w:
    # Write mesh and results to new file
    h5w.create_file(mesh_data=mesh, result_data=results)
