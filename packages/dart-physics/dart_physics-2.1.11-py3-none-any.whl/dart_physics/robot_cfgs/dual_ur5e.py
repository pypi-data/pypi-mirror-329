
from dart_physics.robot_cfgs import * 
from pathlib import Path
import dart_physics.mink as mink 

_HERE = Path(__file__).resolve().parent


def qpos2ctrl(model, data, qpos_target): 

    ctrl = np.zeros(14)
    ctrl[:6] = qpos_target[0:6]
    # ctrl[7:13] = qpos_target[8:14]

    # left gripper control
    tip1 = mink.SE3.from_mocap_name(model, data, "left_lf_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "left_rf_target").as_matrix()

    finger_dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])
    max_grip = data.qpos[8] - 0.01

    # if the fingers are close  (dist 0), it should command 0.788 
    # if the fingers are far away  (dist 0.1), it should command 0 
    # otherwise, it should be linearly interpolated between 0.788 and 0 
    ctrl[6] = 0.788 - 0.788 * finger_dist / 0.1 
    
    ctrl[7:13] = qpos_target[14:20]

    # right gripper control
    tip1 = mink.SE3.from_mocap_name(model, data, "right_lf_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "right_rf_target").as_matrix()

    finger_dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])
    max_grip = data.qpos[16] + 0.01

    ctrl[13] = 0.788 - 0.788 * finger_dist / 0.1 

    return ctrl 

joints = ["shoulder_pan", "shoulder_lift", "forearm_link", "wrist_1", "wrist_2", "wrist_3", "right_driver_joint", "right_coupler_joint",
          "right_spring_link_joint", "right_follower_joint", "left_driver_joint", "left_coupler_joint",
          "left_spring_link_joint", "left_follower_joint"]

gripper_bodies = ["2f85_base", "base_mount", "left_coupler", "left_driver", "left_follower", "left_pad", 
          "left_silicone_pad", "left_spring_link", "right_coupler", "right_driver", "right_follower", "right_pad", "right_silicone_pad", "right_spring_link"]

arm_bodies = ["base", "shoulder_link", "upper_arm_link", "forearm_link", "wrist_1_link", "wrist_2_link", "wrist_3_link"]

robot_cfg = {

    "name": "DualUR5e2F85",

    "robots": { 
        "l_robot": RobotConfig( 
                    xml_path = (_HERE / "../assets" / "ur5e_2f85" / "ur5e.xml").as_posix(),
                    home_q = [-1.5708, -1.5708, 1.5708, -1.5708, -1.5708, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    freejoint = False, 
                    attach_to = [-0.5, -0.0, 0.0, 1, 0, 0, 0 ], 
                    parallel_jaw = True, 
                    add_bodies = [ 
                        NewBodyConfig(attach_to = "left_silicone_pad", \
                                      body_name = "leftarm_left_finger_tip", pos = [0.0, 0.0, 0.02]),
                        NewBodyConfig(attach_to = "left_follower", \
                                        body_name = "leftarm_left_finger_base", pos = [0, 0, 0.0]), 
                        # NewBodyConfig(attach_to = "left_right_finger_link", \
                        #                 body_name = "leftarm_right_finger_tip", pos = [0.0, 0.05, 0.02]),
                        # NewBodyConfig(attach_to = "left_left_finger_link", \
                        #                 body_name = "leftarm_left_finger_tip", pos = [0, -0.05, 0.02]),

                        NewBodyConfig(attach_to = "right_silicone_pad", \
                                        body_name = "leftarm_right_finger_tip", pos = [0.0, 0.0, 0.02]),
                        NewBodyConfig(attach_to = "right_follower", \
                                        body_name = "leftarm_right_finger_base", pos = [0, 0, 0.0]),
                        # NewBodyConfig(attach_to = "right_right_finger_link", \
                        #                 body_name = "rightarm_right_finger_tip", pos = [0.0, 0.05, 0.02]),
                        # NewBodyConfig(attach_to = "right_left_finger_link", \
                        #                 body_name = "rightarm_left_finger_tip", pos = [0, -0.05, 0.02]),
                    ],
                ), 

        "r_robot": RobotConfig(
                    xml_path = (_HERE / "../assets" / "ur5e_2f85" / "ur5e.xml").as_posix(),
                    home_q = [-1.5708, -1.5708, 1.5708, -1.5708, -1.5708, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    freejoint = False, 
                    attach_to = [0.5, -0.0, 0.0, 1, 0, 0, 0 ], 
                    parallel_jaw = True, 
                    add_bodies = [ 
                        NewBodyConfig(attach_to = "left_silicone_pad", \
                                      body_name = "rightarm_left_finger_tip", pos = [0.0, 0.0, 0.02]),
                        NewBodyConfig(attach_to = "left_follower", \
                                      body_name = "rightarm_left_finger_base", pos = [0.0, 0.0, 0.0]),
                        # NewBodyConfig(attach_to = "left_right_finger_link", \
                        #                 body_name = "leftarm_right_finger_tip", pos = [0.0, 0.05, 0.02]),
                        # NewBodyConfig(attach_to = "left_left_finger_link", \
                        #                 body_name = "leftarm_left_finger_tip", pos = [0, -0.05, 0.02]),

                        NewBodyConfig(attach_to = "right_silicone_pad", \
                                        body_name = "rightarm_right_finger_tip", pos = [0.0, 0.0, 0.02]),
                        NewBodyConfig(attach_to = "right_follower", \
                                        body_name = "rightarm_right_finger_base", pos = [0, 0, 0.0]),
                        # NewBodyConfig(attach_to = "right_right_finger_link", \
                        #                 body_name = "rightarm_right_finger_tip", pos = [0.0, 0.05, 0.02]),
                        # NewBodyConfig(attach_to = "right_left_finger_link", \
                        #                 body_name = "rightarm_left_finger_tip", pos = [0, -0.05, 0.02]),
                    ],
                ) 
    }, 

    "qpos2ctrl": qpos2ctrl, 
    "obj_startidx": 28, 
        
    "points" : { 

        "left_lb":     FingerKeypoints("left", 3, "left_lb_target", "l_robot/leftarm_left_finger_base", type = "body"),
        "left_lf":      FingerKeypoints("left", 4, "left_lf_target", "l_robot/leftarm_left_finger_tip", type = "body"),
        "left_rb":      FingerKeypoints("left", 8, "left_rb_target", "l_robot/leftarm_right_finger_base", type = "body"),
        "left_rf":      FingerKeypoints("left", 9, "left_rf_target", "l_robot/leftarm_right_finger_tip", type = "body"),
        
        "right_lb":     FingerKeypoints("right", 3, "right_lb_target", "r_robot/rightarm_left_finger_base", type = "body"),
        "right_lf":     FingerKeypoints("right", 4, "right_lf_target", "r_robot/rightarm_left_finger_tip", type = "body"),
        "right_rb":     FingerKeypoints("right", 8, "right_rb_target", "r_robot/rightarm_right_finger_base", type = "body"),
        "right_rf":     FingerKeypoints("right", 9, "right_rf_target", "r_robot/rightarm_right_finger_tip", type = "body"),

    },

    "reverse_points": { 

        "left_lb":     FingerKeypoints("left", 3, "left_lb_target", "l_robot/leftarm_left_finger_base", type = "body"),
        "left_lf":      FingerKeypoints("left", 4, "left_lf_target", "l_robot/leftarm_left_finger_tip", type = "body"),
        "left_rb":      FingerKeypoints("left", 8, "left_rb_target", "l_robot/leftarm_right_finger_base", type = "body"),
        "left_rf":      FingerKeypoints("left", 9, "left_rf_target", "l_robot/leftarm_right_finger_tip", type = "body"),
        
        "right_lb":     FingerKeypoints("right", 3, "right_lb_target", "r_robot/rightarm_left_finger_base", type = "body"),
        "right_lf":     FingerKeypoints("right", 4, "right_lf_target", "r_robot/rightarm_left_finger_tip", type = "body"),
        "right_rb":     FingerKeypoints("right", 8, "right_rb_target", "r_robot/rightarm_right_finger_base", type = "body"),
        "right_rf":     FingerKeypoints("right", 9, "right_rf_target", "r_robot/rightarm_right_finger_tip", type = "body"),
    },

    "avp_calib": { 

        "left_lb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_lf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_rb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_rf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

        "right_lb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_lf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_rb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_rf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

    }, 

    "ik_task" : [
        IKTasks(target = "left_lb"), 
        IKTasks(target = "left_lf"),
        IKTasks(target = "left_rb"),
        IKTasks(target = "left_rf"),

        IKTasks(target = "right_lb"),
        IKTasks(target = "right_lf"),
        IKTasks(target = "right_rb"),
        IKTasks(target = "right_rf"),
    ],

    "joints" : [f'l_robot/{j}' for j in joints] + [f'r_robot/{j}' for j in joints],

    "bodies":  {},

} 

# add the right arm bodies 
robot_cfg["bodies"].update({f"r_robot/{b}": f"2f85_{b}_right" for b in gripper_bodies})
robot_cfg["bodies"].update({f"r_robot/{b}": f"ur5e_{b}_right" for b in arm_bodies})
robot_cfg["bodies"].update({f"l_robot/{b}": f"2f85_{b}_left" for b in gripper_bodies})
robot_cfg["bodies"].update({f"l_robot/{b}": f"ur5e_{b}_left" for b in arm_bodies})



if __name__ == "__main__": 

    import trimesh 
    from scipy.spatial.transform import Rotation as R
    import os 

    asset_root = os.path.join(_HERE, "../assets", "ur5e_2f85", "assets")
    usdz_root = os.path.join(_HERE, "../assets", "ur5e_2f85", "transformed_stl")\

    os.makedirs(usdz_root, exist_ok = True)

    print([f"{k}" for k in robot_cfg["bodies"].values()])

    for k, v in robot_cfg["usdz_geoms"].items():

        meshes = [] 
        for i, geom in enumerate(v): 
            geom: GeomInfo
            mesh = trimesh.load_mesh(f"{asset_root}/{geom.mesh}.stl")
            pos = np.array(geom.pos)
            quat = np.array(geom.quat)

            mesh.visual.vertex_colors = np.array([0, 0, 0, 255], dtype = np.uint8)

            mat = np.eye(4)
            mat[:3, :3] = R.from_quat(quat, scalar_first = True).as_matrix()
            mat[:3, 3] = pos

            mesh.apply_transform(mat)

            meshes.append(mesh)

        scale = [mesh.scale for mesh in meshes]
        avg_scale = np.mean(scale, axis = 0)
        print(k, avg_scale)
        
        meshes = trimesh.util.concatenate(meshes)

        if avg_scale > 100: 

            meshes.apply_scale(0.001)

        if avg_scale < 1: 

            meshes.apply_scale(1)
        
        meshes.export(f"{usdz_root}/{k}.glb")


