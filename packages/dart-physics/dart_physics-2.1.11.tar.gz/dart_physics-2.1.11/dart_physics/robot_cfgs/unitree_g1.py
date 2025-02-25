
from dart_physics.robot_cfgs import * 
from pathlib import Path

_HERE = Path(__file__).resolve().parent


def qpos2ctrl(model, data, qpos_target): 

    ctrl = np.zeros(25)
    ctrl = qpos_target[:25]
    return ctrl 


bodies = ["left_shoulder_pitch_link", \
          "left_shoulder_roll_link", "left_shoulder_yaw_link", \
            "left_elbow_pitch_link", "left_elbow_roll_link", \
            "left_zero_link", "left_one_link", "left_two_link", \
            "left_three_link", "left_four_link", "left_five_link", \
            "left_six_link"] \
        + ["right_shoulder_pitch_link", "right_shoulder_roll_link", \
            "right_shoulder_yaw_link", "right_elbow_pitch_link", \
            "right_elbow_roll_link", "right_zero_link", "right_one_link", \
            "right_two_link", "right_three_link", "right_four_link", \
            "right_five_link", "right_six_link"]

robot_cfg = {

    "name": "DualPanda",

    "robots": { 
        "robot": RobotConfig( 
                    xml_path = (_HERE / "../assets" / "unitree_g1" / "g1.xml").as_posix(),
                    home_q = [0.0] * 25, 
                    freejoint = False, 
                    attach_to = [0.0, 0.0, 0.2, 0.7071068 , 0, 0, 0.7071068 ], 
                    parallel_jaw = False, 
                    add_bodies = [ 
                        NewBodyConfig(attach_to = "right_six_link", \
                                      body_name = "right_six_link_tip", pos = [0.05, 0.0, 0.0]),
                        NewBodyConfig(attach_to = "right_four_link", \
                                        body_name = "right_four_link_tip", pos = [0.05, 0.0, 0.0]), 
                        NewBodyConfig(attach_to = "right_two_link", \
                                        body_name = "right_two_link_tip", pos = [0.0, 0.05, 0.0]),
                        NewBodyConfig(attach_to = "right_zero_link", \
                                        body_name = "right_zero_link_tip", pos = [-0.05, 0, 0]),

                        NewBodyConfig(attach_to = "left_six_link", \
                                        body_name = "left_six_link_tip", pos = [0.05, 0.0, 0.0]),
                        NewBodyConfig(attach_to = "left_four_link", \
                                        body_name = "left_four_link_tip", pos = [0.05, 0.0, 0.0]),
                        NewBodyConfig(attach_to = "left_two_link", \
                                        body_name = "left_two_link_tip", pos = [0.0, -0.05, 0.0]),
                        NewBodyConfig(attach_to = "left_zero_link", \
                                        body_name = "left_zero_link_tip", pos = [-0.05, 0, 0]),
                    ], 
                    
                ), 
    }, 

    "qpos2ctrl": qpos2ctrl, 
    "obj_startidx": (7+2) * 2, 
        
    "points" : { 

        "left_wrist":     FingerKeypoints("left", 0, "left_wrist_target", "robot/left_zero_link_tip", type = "body", avp_transform = rot_x(90)),
        "left_two":      FingerKeypoints("left", 4, "left_two_target", "robot/left_two_link_tip", type = "body"),
        "left_four":      FingerKeypoints("left", 9, "left_four_target", "robot/left_four_link_tip", type = "body"),
        "left_six":      FingerKeypoints("left", 14, "left_six_target", "robot/left_six_link_tip", type = "body"),

        "right_wrist":     FingerKeypoints("right", 0, "right_wrist_target", "robot/right_zero_link_tip", type = "body", avp_transform = rot_x(90) @ rot_y(180)),
        "right_two":      FingerKeypoints("right", 4, "right_two_target", "robot/right_two_link_tip", type = "body"),
        "right_four":      FingerKeypoints("right", 9, "right_four_target", "robot/right_four_link_tip", type = "body"),
        "right_six":      FingerKeypoints("right", 14, "right_six_target", "robot/right_six_link_tip", type = "body"),

    },

    "reverse_points" : { 

        "left_wrist":     FingerKeypoints("left", 0, "left_wrist_target", "robot/left_zero_link_tip", type = "body", avp_transform = rot_x(90)),
        "left_two":      FingerKeypoints("left", 4, "left_two_target", "robot/left_two_link_tip", type = "body"),
        "left_four":      FingerKeypoints("left", 9, "left_four_target", "robot/left_four_link_tip", type = "body"),
        "left_six":      FingerKeypoints("left", 14, "left_six_target", "robot/left_six_link_tip", type = "body"),

        "right_wrist":     FingerKeypoints("right", 0, "right_wrist_target", "robot/right_zero_link_tip", type = "body", avp_transform = rot_x(90) @ rot_y(180)),
        "right_two":      FingerKeypoints("right", 4, "right_two_target", "robot/right_two_link_tip", type = "body"),
        "right_four":      FingerKeypoints("right", 9, "right_four_target", "robot/right_four_link_tip", type = "body"),
        "right_six":      FingerKeypoints("right", 14, "right_six_target", "robot/right_six_link_tip", type = "body"),

    },


    "avp_calib": { 

        "left_wrist": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_two": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_four": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_six": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

        "right_wrist": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_two": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_four": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_six": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
    }, 

    "ik_task" : [
        # IKTasks(target = "left_wrist", pos_cost = 1.0, ori_cost = 0.5), 
        # IKTasks(root = "left_wrist", target = "left_two"),
        # IKTasks(root = "left_wrist", target = "left_four"),
        # IKTasks(root = "left_wrist", target = "left_six"),

        # # IKTasks(target = "right_wrist", pos_cost = 1.0, ori_cost = 0.5),
        # IKTasks(root = "right_wrist", target = "right_two"),
        # IKTasks(root = "right_wrist", target = "right_four"),
        # IKTasks(root = "right_wrist", target = "right_six"),

        IKTasks(target = "left_wrist"), 
        IKTasks(target = "left_two"), 
        IKTasks(target = "left_four"), 
        IKTasks(target = "left_six"),

        IKTasks(target = "right_wrist"),
        IKTasks(target = "right_two"), 
        IKTasks(target = "right_four"), 
        IKTasks(target = "right_six"), 
    ],

    "joints" : ["robot/torso_joint",
                            
                "robot/left_shoulder_pitch_joint",
                "robot/left_shoulder_roll_joint",
                "robot/left_shoulder_yaw_joint",
                "robot/left_elbow_pitch_joint",
                "robot/left_elbow_roll_joint",

                "robot/right_shoulder_pitch_joint",
                "robot/right_shoulder_roll_joint",
                "robot/right_shoulder_yaw_joint",
                "robot/right_elbow_pitch_joint",
                "robot/right_elbow_roll_joint",

                ], 

    "bodies":  {f"robot/{key}":f"gggg1_{key}" for key in bodies}, 

    "usdz_geoms":  [ 
        

        # LEFT 

        BodyInfo(
            name = "g1_left_shoulder_pitch_link",
            geoms = [GeomInfo(mesh = "left_shoulder_pitch_link")],
            pos="-0.0025 0.10396 0.25928", quat="0.990268 0.139172 0 0"
        ), 

        BodyInfo(
            name = "g1_left_shoulder_roll_link",
            geoms = [GeomInfo(mesh = "left_shoulder_roll_link")],
            pos="0 0.052 0", quat="0.990268 -0.139172 0 0", 
        ), 

        BodyInfo(
            name = "g1_left_shoulder_yaw_link",
            geoms = [GeomInfo(mesh = "left_shoulder_yaw_link")],
            pos="-0.00354 0.0062424 -0.1032", 
        ), 

        BodyInfo(
            name = "g1_left_elbow_pitch_link",
            geoms = [GeomInfo(mesh = "left_elbow_pitch_link")],
            pos="0 0.00189 -0.0855", 
        ), 

        BodyInfo(
            name = "g1_left_elbow_roll_link",
            geoms = [GeomInfo(mesh = "left_elbow_roll_link"), GeomInfo(mesh = "left_palm_link", pos=[0.12, 0, 0])],
            pos="0.1 0 0", 
        ),


        BodyInfo(
            name = "g1_left_zero_link",
            geoms = [GeomInfo(mesh = "left_zero_link")],
            pos="0.17 0 0", 
        ), 

        BodyInfo(
            name = "g1_left_one_link",
            geoms = [GeomInfo(mesh = "left_one_link")],
            pos="-0.026525 -0.0188 -5e-05", 
        ), 

        BodyInfo(
            name = "g1_left_two_link",
            geoms = [GeomInfo(mesh = "left_two_link")],
            pos="0 -0.0431 0", 
        ), 

        BodyInfo(
            name = "g1_left_three_link",
            geoms = [GeomInfo(mesh = "left_three_link")],
            pos="0.205 0.004 0.02395"
        ), 

        BodyInfo(
            name = "g1_left_four_link",
            geoms = [GeomInfo(mesh = "left_four_link")],
            pos="0.0471 -0.0036 0", 
        ), 

        BodyInfo(
            name = "g1_left_five_link", 
            geoms = [GeomInfo(mesh = "left_five_link")],
            pos="0.205 0.004 -0.02395", 
        ), 

        BodyInfo(
            name = "g1_left_six_link",
            geoms = [GeomInfo(mesh = "left_six_link")],
            pos="0.0471 -0.0036 0", 
        ), 

        # RIGHT 

        BodyInfo(
            name = "g1_right_shoulder_pitch_link",
            geoms = [GeomInfo(mesh = "right_shoulder_pitch_link")],
            pos="-0.0025 -0.10396 0.25928", quat="0.990268 -0.139172 0 0"
        ), 



        BodyInfo(
            name = "g1_right_shoulder_roll_link",
            geoms = [GeomInfo(mesh = "right_shoulder_roll_link")],
            pos="0 -0.052 0", quat="0.990268 0.139172 0 0"
        ), 

        BodyInfo(
            name = "g1_right_shoulder_yaw_link",
            geoms = [GeomInfo(mesh = "right_shoulder_yaw_link")],
            pos="-0.00354 -0.0062424 -0.1032",
        ), 

        BodyInfo(
            name = "g1_right_elbow_pitch_link",
            geoms = [GeomInfo(mesh = "right_elbow_pitch_link")],
            pos="0 -0.00189 -0.0855",
        ), 

        BodyInfo(
            name = "g1_right_elbow_roll_link",
            geoms = [GeomInfo(mesh = "right_elbow_roll_link"), GeomInfo(mesh = "right_palm_link", pos=[0.12, 0, 0])],
            pos="0.1 0 0",
        ),

        BodyInfo(
            name = "g1_right_zero_link",
            geoms = [GeomInfo(mesh = "right_zero_link")],
            pos="0.17 0 0",
        ),

        BodyInfo(
            name = "g1_right_one_link",
            geoms = [GeomInfo(mesh = "right_one_link")],
            pos="-0.026525 0.0188 -5e-05",
        ),

        BodyInfo(
            name = "g1_right_two_link",
            geoms = [GeomInfo(mesh = "right_two_link")],
            pos="0 0.0431 0",
        ),

        BodyInfo(
            name = "g1_right_three_link",
            geoms = [GeomInfo(mesh = "right_three_link")],
            pos="0.205 -0.004 0.02395"
        ),

        BodyInfo(
            name = "g1_right_four_link",
            geoms = [GeomInfo(mesh = "right_four_link")],
            pos="0.0471 0.0036 0",
        ),

        BodyInfo(
            name = "g1_right_five_link",
            geoms = [GeomInfo(mesh = "right_five_link")],
            pos="0.205 -0.004 -0.02395",
        ),

        BodyInfo(
            name = "g1_right_six_link",
            geoms = [GeomInfo(mesh = "right_six_link")],
            pos="0.0471 0.0036 0",
        ),

    ]



} 


if __name__ == "__main__": 

    import trimesh 
    from scipy.spatial.transform import Rotation as R
    import os 

    asset_root = os.path.join(_HERE, "../assets", "unitree_g1", "assets")
    usdz_root = os.path.join(_HERE, "../assets", "unitree_g1", "transformed_stl3")\

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

            mesh.apply_transform(mat)

            meshes.append(mesh)
        
        meshes = trimesh.util.concatenate(meshes)
        # mat = np.eye(4)
        # pos = np.array(body.pos)
        # quat = np.array(body.quat)

        # mat[:3, :3] = R.from_quat(quat, scalar_first = True).as_matrix()
        # mat[:3, 3] = pos

        # meshes.apply_transform(mat)

        meshes.export(f"{usdz_root}/{body.name}.obj")


