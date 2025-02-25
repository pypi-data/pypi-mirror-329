
from dart_physics.robot_cfgs import * 
from pathlib import Path

_HERE = Path(__file__).resolve().parent


def qpos2ctrl(model, data, qpos): 

    ctrl = np.zeros(32)
    ctrl[:16] = qpos[7:23]
    ctrl[16:] = qpos[30:46]
    return ctrl 

robot_cfg = {

    "name": "FreefloatingDualAllegro",

    "robots": { 
        "l_robot": RobotConfig( 
                    xml_path = (_HERE / "../assets" / "wonik_allegro" / "left_hand.xml").as_posix(),
                    home_q = [-0.5, 0.0, 0.3, 0, 0, 0, 1] + [0.] * 16, 
                    freejoint = True, 
                ), 
        "r_robot": RobotConfig(
                    xml_path = (_HERE / "../assets" / "wonik_allegro" / "right_hand.xml").as_posix(),
                    home_q = [0.5, 0.0, 0.3, 0, 0, 0, 1] + [0.] * 16,
                    freejoint = True,
                ) 
    }, 

    "qpos2ctrl": qpos2ctrl, 
    "obj_startidx": (7+16) * 2, 
        
    "points" : { 
        "left_wrist":  FingerKeypoints("left", 0, "left_wrist_target", "l_robot/palm", weld = True, \
                                       avp_transform = rot_z(90) @ rot_x(90), init_posquat = [-0.5, 0.0, 0.3, 0, 0, 0, 1]), 
        "right_wrist": FingerKeypoints("right", 0, "right_wrist_target", "r_robot/palm", weld = True, \
                                       avp_transform = rot_z(-90) @ rot_x(90), init_posquat = [0.5, 0.0, 0.3, 0, 0, 0, 1]),
        
        "left_ff":     FingerKeypoints("left", 9, "left_ff_tip_target", "l_robot/ff_tip", type = "site"),
        "left_mf":      FingerKeypoints("left", 14, "left_mf_tip_target", "l_robot/mf_tip", type = "site"),
        "left_rf":      FingerKeypoints("left", 19, "left_rf_tip_target", "l_robot/rf_tip", type = "site"),
        "left_th":      FingerKeypoints("left", 4, "left_th_tip_target", "l_robot/th_tip", type = "site"),
        
        "right_ff":     FingerKeypoints("right", 9, "right_ff_tip_target", "r_robot/ff_tip", type = "site"),
        "right_mf":     FingerKeypoints("right", 14, "right_mf_tip_target", "r_robot/mf_tip", type = "site"),
        "right_rf":     FingerKeypoints("right", 19, "right_rf_tip_target", "r_robot/rf_tip", type = "site"),
        "right_th":     FingerKeypoints("right", 4, "right_th_tip_target", "r_robot/th_tip", type = "site"),
    },

    "reverse_points": { 
        "left_wrist":  FingerKeypoints("left", 0, "left_wrist_target", "l_robot/palm", weld = True, \
                                       avp_transform = rot_z(90) @ rot_x(90), init_posquat = [-0.5, 0.0, 0.3, 0, 0, 0, 1]), 
        "right_wrist": FingerKeypoints("right", 0, "right_wrist_target", "r_robot/palm", weld = True, \
                                       avp_transform = rot_z(-90) @ rot_x(90), init_posquat = [0.5, 0.0, 0.3, 0, 0, 0, 1]),
        
        "left_ff":     FingerKeypoints("left", 9, "left_ff_tip_target", "l_robot/ff_tip", type = "site"),
        "left_mf":      FingerKeypoints("left", 14, "left_mf_tip_target", "l_robot/mf_tip", type = "site"),
        "left_rf":      FingerKeypoints("left", 19, "left_rf_tip_target", "l_robot/rf_tip", type = "site"),
        "left_th":      FingerKeypoints("left", 4, "left_th_tip_target", "l_robot/th_tip", type = "site"),
        
        "right_ff":     FingerKeypoints("right", 9, "right_ff_tip_target", "r_robot/ff_tip", type = "site"),
        "right_mf":     FingerKeypoints("right", 14, "right_mf_tip_target", "r_robot/mf_tip", type = "site"),
        "right_rf":     FingerKeypoints("right", 19, "right_rf_tip_target", "r_robot/rf_tip", type = "site"),
        "right_th":     FingerKeypoints("right", 4, "right_th_tip_target", "r_robot/th_tip", type = "site"),
    },

    "avp_calib": { 

        "left_ff": {"scale": 1.3, "offset": np.array([-0.02, 0.0, 0.0])},
        "left_mf": {"scale": 1.2, "offset": np.array([+0.00, 0.0, 0.0])},
        "left_rf": {"scale": 1.2, "offset": np.array([+0.02, 0.0, 0.0])},
        "left_th": {"scale": 1.0, "offset": np.array([+0.00, 0.0, 0.0])},

        "right_ff": {"scale": 1.3, "offset": np.array([0.0, -0.02, 0.0])},
        "right_mf": {"scale": 1.2, "offset": np.array([0.0, -0.00, 0.0])},
        "right_rf": {"scale": 1.2, "offset": np.array([0.0, +0.02, 0.0])},
        "right_th": {"scale": 1.0, "offset": np.array([0.0, +0.00, 0.0])},

    }, 

    "ik_task" : [
        IKTasks(root = "left_wrist", target = "left_rf"), 
        IKTasks(root = "left_wrist", target = "left_mf"),
        IKTasks(root = "left_wrist", target = "left_ff"),
        IKTasks(root = "left_wrist", target = "left_th"),

        IKTasks(root = "right_wrist", target = "right_rf"),
        IKTasks(root = "right_wrist", target = "right_mf"),
        IKTasks(root = "right_wrist", target = "right_ff"),
        IKTasks(root = "right_wrist", target = "right_th"),
    ],

    "joints" : [ 
        # left hand 
        "l_robot/rfj0", "l_robot/rfj1", "l_robot/rfj2", "l_robot/rfj3",
        "l_robot/mfj0", "l_robot/mfj1", "l_robot/mfj2", "l_robot/mfj3",
        "l_robot/ffj0", "l_robot/ffj1", "l_robot/ffj2", "l_robot/ffj3",
        "l_robot/thj0", "l_robot/thj1", "l_robot/thj2", "l_robot/thj3",

        # right hand
        "r_robot/rfj0", "r_robot/rfj1", "r_robot/rfj2", "r_robot/rfj3",
        "r_robot/mfj0", "r_robot/mfj1", "r_robot/mfj2", "r_robot/mfj3",
        "r_robot/ffj0", "r_robot/ffj1", "r_robot/ffj2", "r_robot/ffj3",
        "r_robot/thj0", "r_robot/thj1", "r_robot/thj2", "r_robot/thj3",
    ],

    "bodies":  {
        "l_robot/palm": "left_allegro_palm", 
        "r_robot/palm": "right_allegro_palm",


        # left ff 
        "l_robot/ff_base":   "left_allegro_ff_base",   "l_robot/ff_distal":   "left_allegro_ff_distal", 
        "l_robot/ff_medial": "left_allegro_ff_medial", "l_robot/ff_proximal": "left_allegro_ff_proximal", 
        "l_robot/ff_tip": "left_allegro_ff_tip", 

        # left mf 
        "l_robot/mf_base":   "left_allegro_mf_base",   "l_robot/mf_distal":   "left_allegro_mf_distal", 
        "l_robot/mf_medial": "left_allegro_mf_medial", "l_robot/mf_proximal": "left_allegro_mf_proximal", 
        "l_robot/mf_tip": "left_allegro_mf_tip", 

        # left rf 
        "l_robot/rf_base":   "left_allegro_rf_base",   "l_robot/rf_distal":   "left_allegro_rf_distal",
        "l_robot/rf_medial": "left_allegro_rf_medial", "l_robot/rf_proximal": "left_allegro_rf_proximal",
        "l_robot/rf_tip": "left_allegro_rf_tip",

        # left th
        "l_robot/th_base":   "left_allegro_th_base",   "l_robot/th_distal":   "left_allegro_th_distal",
        "l_robot/th_medial": "left_allegro_th_medial", "l_robot/th_proximal": "left_allegro_th_proximal",
        "l_robot/th_tip": "left_allegro_th_tip",

        # right ff
        "r_robot/ff_base":   "right_allegro_ff_base",   "r_robot/ff_distal":   "right_allegro_ff_distal",
        "r_robot/ff_medial": "right_allegro_ff_medial", "r_robot/ff_proximal": "right_allegro_ff_proximal",
        "r_robot/ff_tip": "right_allegro_ff_tip",

        # right mf
        "r_robot/mf_base":   "right_allegro_mf_base",   "r_robot/mf_distal":   "right_allegro_mf_distal",
        "r_robot/mf_medial": "right_allegro_mf_medial", "r_robot/mf_proximal": "right_allegro_mf_proximal",
        "r_robot/mf_tip": "right_allegro_mf_tip",

        # right rf
        "r_robot/rf_base":   "right_allegro_rf_base",   "r_robot/rf_distal":   "right_allegro_rf_distal",
        "r_robot/rf_medial": "right_allegro_rf_medial", "r_robot/rf_proximal": "right_allegro_rf_proximal",
        "r_robot/rf_tip": "right_allegro_rf_tip",

        # right th
        "r_robot/th_base":   "right_allegro_th_base",   "r_robot/th_distal":   "right_allegro_th_distal",
        "r_robot/th_medial": "right_allegro_th_medial", "r_robot/th_proximal": "right_allegro_th_proximal",
        "r_robot/th_tip": "right_allegro_th_tip",

    }, 

    "usdz_geoms":  [ 

        # LEFT 
        BodyInfo(
            name = "left_allegro_ff_base", 
            geoms = [GeomInfo(mesh = "link_0.0")], 
        ), 
        BodyInfo(
            name = "left_allegro_ff_distal", 
            geoms = [GeomInfo(mesh = "link_3.0")], 
        ),
        BodyInfo(
            name = "left_allegro_ff_medial", 
            geoms = [GeomInfo(mesh = "link_2.0")], 
        ),
        BodyInfo(
            name = "left_allegro_ff_proximal", 
            geoms = [GeomInfo(mesh = "link_1.0")], 
        ),
        BodyInfo(
            name = "left_allegro_ff_tip", 
            geoms = [GeomInfo(mesh = "link_3.0_tip", pos=[0, 0, 0.0267])], 
        ),
        BodyInfo(
            name = "left_allegro_mf_base", 
            geoms = [GeomInfo(mesh = "link_0.0")], 
        ),
        BodyInfo(
            name = "left_allegro_mf_distal", 
            geoms = [GeomInfo(mesh = "link_3.0")], 
        ),
        BodyInfo(
            name = "left_allegro_mf_medial", 
            geoms = [GeomInfo(mesh = "link_2.0")], 
        ),
        BodyInfo(
            name = "left_allegro_mf_proximal", 
            geoms = [GeomInfo(mesh = "link_1.0")], 
        ),
        BodyInfo(
            name = "left_allegro_mf_tip", 
            geoms = [GeomInfo(mesh = "link_3.0_tip", pos=[0, 0, 0.0267])], 
        ),
        BodyInfo(
            name = "left_allegro_rf_base", 
            geoms = [GeomInfo(mesh = "link_0.0")], 
        ),
        BodyInfo(
            name = "left_allegro_rf_distal", 
            geoms = [GeomInfo(mesh = "link_3.0")], 
        ),
        BodyInfo(
            name = "left_allegro_rf_medial", 
            geoms = [GeomInfo(mesh = "link_2.0")], 
        ),
        BodyInfo(
            name = "left_allegro_rf_proximal", 
            geoms = [GeomInfo(mesh = "link_1.0")], 
        ),
        BodyInfo(
            name = "left_allegro_rf_tip", 
            geoms = [GeomInfo(mesh = "link_3.0_tip", pos=[0, 0, 0.0267])], 
        ),
        BodyInfo(
            name = "left_allegro_th_base", 
            geoms = [GeomInfo(mesh = "link_12.0_left", quat = [0, 1, 0, 0])], 
        ),
        BodyInfo(
            name = "left_allegro_th_distal", 
            geoms = [GeomInfo(mesh = "link_15.0")], 
        ),
        BodyInfo( 
            name = "left_allegro_th_medial",
            geoms = [GeomInfo(mesh = "link_14.0")],
        ), 
        BodyInfo(
            name = "left_allegro_th_proximal",
            geoms = [GeomInfo(mesh = "link_13.0")],
        ),
        BodyInfo(
            name = "left_allegro_th_tip",
            geoms = [GeomInfo(mesh = "link_15.0_tip", pos=[0, 0, 0.0423])],
        ),
        BodyInfo(
            name = "left_allegro_palm", 
            geoms = [GeomInfo(mesh = "base_link_left", quat = [1, -1, 0, 0])], 
        ),



        # LEFT 

        BodyInfo(
            name = "right_allegro_ff_base", 
            geoms = [GeomInfo(mesh = "link_0.0")], 
        ),
        BodyInfo(
            name = "right_allegro_ff_distal", 
            geoms = [GeomInfo(mesh = "link_3.0")], 
        ),
        BodyInfo(
            name = "right_allegro_ff_medial", 
            geoms = [GeomInfo(mesh = "link_2.0")], 
        ),
        BodyInfo(
            name = "right_allegro_ff_proximal", 
            geoms = [GeomInfo(mesh = "link_1.0")], 
        ),
        BodyInfo(
            name = "right_allegro_ff_tip", 
            geoms = [GeomInfo(mesh = "link_3.0_tip", pos=[0, 0, 0.0267])], 
        ),
        BodyInfo(
            name = "right_allegro_mf_base", 
            geoms = [GeomInfo(mesh = "link_0.0")], 
        ),
        BodyInfo(
            name = "right_allegro_mf_distal", 
            geoms = [GeomInfo(mesh = "link_3.0")], 
        ),
        BodyInfo(
            name = "right_allegro_mf_medial", 
            geoms = [GeomInfo(mesh = "link_2.0")], 
        ),
        BodyInfo(
            name = "right_allegro_mf_proximal", 
            geoms = [GeomInfo(mesh = "link_1.0")], 
        ),
        BodyInfo(
            name = "right_allegro_mf_tip", 
            geoms = [GeomInfo(mesh = "link_3.0_tip", pos=[0, 0, 0.0267])], 
        ),
        BodyInfo(
            name = "right_allegro_rf_base", 
            geoms = [GeomInfo(mesh = "link_0.0")], 
        ),
        BodyInfo(
            name = "right_allegro_rf_distal", 
            geoms = [GeomInfo(mesh = "link_3.0")], 
        ),
        BodyInfo(
            name = "right_allegro_rf_medial", 
            geoms = [GeomInfo(mesh = "link_2.0")], 
        ),
        BodyInfo(
            name = "right_allegro_rf_proximal", 
            geoms = [GeomInfo(mesh = "link_1.0")], 
        ),
        BodyInfo(
            name = "right_allegro_rf_tip", 
            geoms = [GeomInfo(mesh = "link_3.0_tip", pos=[0, 0, 0.0267])], 
        ),
        BodyInfo(
            name = "right_allegro_th_base", 
            geoms = [GeomInfo(mesh = "link_12.0_right")], 
        ),
        BodyInfo(
            name = "right_allegro_th_distal", 
            geoms = [GeomInfo(mesh = "link_15.0")], 
        ),
        BodyInfo( 
            name = "right_allegro_th_medial",
            geoms = [GeomInfo(mesh = "link_14.0")],
        ),
        BodyInfo(
            name = "right_allegro_th_proximal",
            geoms = [GeomInfo(mesh = "link_13.0")],
        ),
        BodyInfo(
            name = "right_allegro_th_tip",
            geoms = [GeomInfo(mesh = "link_15.0_tip", pos=[0, 0, 0.0423])],
        ),
        BodyInfo(
            name = "right_allegro_palm", 
            geoms = [GeomInfo(mesh = "base_link")], 
        ),

    ]

}


if __name__ == "__main__": 


    import trimesh 
    from scipy.spatial.transform import Rotation as R
    import os 

    asset_root = os.path.join(_HERE, "../assets", "wonik_allegro", "assets")
    usdz_root = os.path.join(_HERE, "../assets", "wonik_allegro", "transformed_stl")\

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

        meshes.export(f"{usdz_root}/{body.name}.glb")

