import trimesh
import xml.etree.ElementTree as ET
from scipy.spatial.transform import Rotation as R
import os
from dm_control import mjcf

# Load the MuJoCo XML model
xml_path = "./assets/eyesight_R"
xml_file = 'mjmodel.xml'

xml_full_path = os.path.join(xml_path, xml_file)

# Load the MJCF model
model = mjcf.from_path(xml_full_path)

def apply_transformations(mesh, pos, quat):
    """Apply translation and rotation to a mesh."""
    # Apply translation
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    # Apply rotation
    rotation_matrix = R.from_quat(quat).as_matrix()
    rotation_matrix_4x4 = trimesh.transformations.identity_matrix()
    rotation_matrix_4x4[:3, :3] = rotation_matrix
    # Apply transformation
    transformation_matrix = trimesh.transformations.concatenate_matrices(translation_matrix, rotation_matrix_4x4)
    return mesh.apply_transform(transformation_matrix)

def process_body(body):
    """Process a body, apply transformations, and export its mesh."""
    print("A", body)
    try: 
        body_name = body.full_identifier.replace("/", "_")
    except:
        return []
    meshes = []
    
    for geom in body.find_all('geom'):
        pos = geom.pos if geom.pos is not None else [0.0, 0.0, 0.0]
        quat = geom.quat if geom.quat is not None else [1.0, 0.0, 0.0, 0.0]
        mesh_file = None
        
        if geom.mesh:
            print(geom.mesh.name)
            mesh_file = geom.mesh.name
        # else:
        #     print(geom.dclass)
        elif geom.dclass and geom.dclass.geom.mesh:
            mesh_file = geom.dclass.geom.mesh.name
        
        if mesh_file:
            print("found mesh file")
            mesh_file_path = os.path.join(xml_path, 'assets', mesh_file + '.stl')
            if os.path.exists(mesh_file_path):
                mesh = trimesh.load(mesh_file_path)
                # Apply the transformations
                transformed_mesh = apply_transformations(mesh, pos, quat)
                meshes.append(transformed_mesh)
                print("added")
            else:
                print(f"Warning: Mesh file {mesh_file_path} not found.")
    
    # Recursively process child bodies
    for child_body in body.all_children():
        child_meshes = process_body(child_body)
        meshes.extend(child_meshes)
    
    # Combine all meshes under this body, even if it is empty
    # if not meshes:
    #     # Create an empty mesh if no geometries are found
    #     empty_mesh = trimesh.Trimesh(vertices=[], faces=[])
    #     meshes.append(empty_mesh)
    if meshes == []: 
        print("falling back")
        return meshes
    combined_mesh = trimesh.util.concatenate(meshes)
    output_path = os.path.join(xml_path, f'{body_name}.stl')
    print("exporting to", output_path)
    combined_mesh.export(output_path)

    return meshes

# Start processing from the root body
root_body = model.worldbody
process_body(root_body)
