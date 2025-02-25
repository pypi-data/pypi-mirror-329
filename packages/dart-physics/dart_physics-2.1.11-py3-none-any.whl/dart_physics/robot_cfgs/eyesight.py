
from dart_physics.robot_cfgs import * 
from pathlib import Path

_HERE = Path(__file__).resolve().parent


def qpos2ctrl(model, data, qpos): 

    ctrl = np.zeros(9)
    ctrl[:9] = qpos[7:16]
    return ctrl 

robot_cfg = {

    "name": "FreefloatingEyeSight",

    "robots": { 
        "r_robot": RobotConfig(
                    xml_path = (_HERE / "../assets" / "eyesight_R" / "robot_actuate.xml").as_posix(),
                    home_q = [0.5, 0.0, 0.3, 0, 0, 0, 1] + [0.] * 9,
                    freejoint = True,
                ) 
    }, 

    "qpos2ctrl": qpos2ctrl, 
    "obj_startidx": (7+9) * 1, 
        
    "points" : { 
        "right_wrist": FingerKeypoints("right", 0, "right_wrist_target", "r_robot/base_link", weld = True, \
                                       avp_transform = rot_z(-90) @ rot_x(90), \
                                       init_posquat = [0.5, 0.0, 0.3, 0, 0, 0, 1]),
        
        
        "right_mf":     FingerKeypoints("right", 14, "right_mf_tip_target", "r_robot/middle_tip", type = "site", ),
        "right_rf":     FingerKeypoints("right", 9, "right_rf_tip_target", "r_robot/index_tip", type = "site"),
        "right_th":     FingerKeypoints("right", 4, "right_th_tip_target", "r_robot/thumb_tip", type = "site"),
    },

    "reverse_points" : { 
        "right_wrist": FingerKeypoints("right", 0, "right_wrist_target", "r_robot/base_link", weld = True, \
                                       avp_transform = rot_z(-90) @ rot_x(-90), init_posquat = [0.5, 0.0, 0.3, 0, 0, 0, 1]),
        
        
        "right_mf":     FingerKeypoints("right", 14, "right_mf_tip_target", "r_robot/middle_tip", type = "site",),
        "right_rf":     FingerKeypoints("right", 9, "right_rf_tip_target", "r_robot/index_tip", type = "site"),
        "right_th":     FingerKeypoints("right", 4, "right_th_tip_target", "r_robot/thumb_tip", type = "site"),
    },


    "avp_calib": { 

        "right_mf": {"scale": 1.0, "offset": np.array([0.0, -0.00, 0.0])},
        "right_rf": {"scale": 1.0, "offset": np.array([0.0, +0.0, 0.0])},
        "right_th": {"scale": 1.0, "offset": np.array([0.0, +0.00, 0.0])},

    }, 

    "ik_task" : [

        IKTasks(root = "right_wrist", target = "right_rf"),
        IKTasks(root = "right_wrist", target = "right_mf"),
        IKTasks(root = "right_wrist", target = "right_th"),
    ],

    "joints" : [ 
        # right hand
        "r_robot/base_l00", "r_robot/l00_l01", "r_robot/l01_l02", 
        "r_robot/base_l10", "r_robot/l10_l11", "r_robot/l11_l12",
        "r_robot/base_l20", "r_robot/l20_l21", "r_robot/l21_l22", 
    ],

    "bodies":  {
        "r_robot/base_link":  "eyesight_right_base_link", 

        # right ff
        "r_robot/link_1_0":   "eyesight_right_link_1_0",  
        "r_robot/link_1_1":   "eyesight_right_link_1_1",
        "r_robot/link_1_2":   "eyesight_right_link_1_2", 

        # right mf
        "r_robot/link_2_0":   "eyesight_right_link_2_0",   
        "r_robot/link_2_1":   "eyesight_right_link_2_1",
        "r_robot/link_2_2":   "eyesight_right_link_2_2", 

        # right rf
        "r_robot/link_0_0":   "eyesight_right_link_0_0",
        "r_robot/link_0_1":   "eyesight_right_link_0_1",
        "r_robot/link_0_2":   "eyesight_right_link_0_2",

    }, 

    "usdz_geoms":  [ 


        # BASEE 
        BodyInfo(
            name = "base_link", 
            geoms = [GeomInfo(mesh = "base_link", quat=[0.707107, 0, 0, 0.707107])], 
        ),

        #  RIGHT 

        BodyInfo(
            name = "link_0_0", 
            geoms = [GeomInfo(mesh = "link_0_0", quat=[0.5, -0.5, -0.5, -0.5])], 
        ),
        BodyInfo(
            name = "link_0_1", 
            geoms = [GeomInfo(mesh = "link_0_1", quat=[0, -1, 0, 0])], 
        ),
        BodyInfo(
            name = "link_0_2", 
            geoms = [GeomInfo(mesh = "link_0_2", pos=[0, -0.0045, -0.007], quat=[0.5, -0.5, -0.5, -0.5])], 
        ),

        BodyInfo(
            name = "link_1_0", 
            geoms = [GeomInfo(mesh = "link_1_0", quat=[0.707107, 0.707107, 0, 0])], 
        ),
        BodyInfo(
            name = "link_1_1", 
            geoms = [GeomInfo(mesh = "link_1_1", pos=[0, 0, 0.0082], quat=[0.5, -0.5, -0.5, -0.5])], 
        ),
        BodyInfo(
            name = "link_1_2", 
            geoms = [GeomInfo(mesh = "link_1_2", pos=[0, -0.0045, -0.0081], quat=[0.5, -0.5, -0.5, -0.5])]
        ),
        BodyInfo(
            name = "link_2_0", 
            geoms = [GeomInfo(mesh = "link_2_0", quat=[0.707107, -0.707107, 0, 0])], 
        ),
        BodyInfo(
            name = "link_2_1", 
            geoms = [GeomInfo(mesh = "link_2_1", quat=[0.5, -0.5, -0.5, -0.5])], 
        ),
        BodyInfo(
            name = "link_2_2", 
            geoms = [GeomInfo(mesh = "link_2_2", pos=[0, -0.0045, -0.0081], quat=[0.5, -0.5, -0.5, -0.5])], 
        ),

    ]

}


if __name__ == "__main__": 


    import trimesh 
    from scipy.spatial.transform import Rotation as R
    import os 

    asset_root = os.path.join(_HERE, "../assets", "eyesight_R", "assets")
    usdz_root = os.path.join(_HERE, "../assets", "eyesight_R", "transformed_stl")\

    os.makedirs(usdz_root, exist_ok = True)

    input_list = [f"{k}" for k in robot_cfg["bodies"].values()]
    output_string = str(input_list).replace("'", '"')
    print(output_string)

    for body in robot_cfg["usdz_geoms"]:

        body: BodyInfo

        meshes = [] 
        for i, geom in enumerate(body.geoms): 
            geom: GeomInfo
            mesh = trimesh.load_mesh(f"{asset_root}/{geom.mesh}.stl")
            pos = np.array(geom.pos)
            quat = np.array(geom.quat)

            mat = np.eye(4)
            mat[:3, :3] = R.from_quat(quat, scalar_first = True).as_matrix()
            mat[:3, 3] = pos

            mesh.visual.vertex_colors = np.array([0, 0, 0, 255], dtype = np.uint8)

            mesh.apply_transform(mat)

            meshes.append(mesh)
        
        meshes = trimesh.util.concatenate(meshes)
        # mat = np.eye(4)
        # pos = np.array(body.pos)
        # quat = np.array(body.quat)

        # mat[:3, :3] = R.from_quat(quat, scalar_first = True).as_matrix()
        # mat[:3, 3] = pos

        # meshes.apply_transform(mat)

        meshes.export(f"{usdz_root}/eyesight_right_{body.name}.glb")

