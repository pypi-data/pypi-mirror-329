
from dart_physics.robot_cfgs import * 
from pathlib import Path
import mujoco
import dart_physics.mink as mink 

_HERE = Path(__file__).resolve().parent


def qpos2ctrl(model, data, qpos_target): 

    ctrl = np.zeros(8)
    ctrl[:7] = qpos_target[0:7]

    # gripper control
    tip1 = mink.SE3.from_mocap_name(model, data, "right_lf_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "right_rf_target").as_matrix()

    finger_dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])

    max_grip = data.qpos[8] - 0.01

    ctrl[-1] = np.clip(finger_dist - 0.01, max_grip, 0.04)

    return ctrl 


robot_cfg = {

    "name": "right_panda",

    "robots": { 
        "r_robot": RobotConfig( 
                    xml_path = (_HERE / "../assets" / "franka_emika_panda" / "new_panda.xml").as_posix(),
                    home_q = [0, 0, 0, -1.5707899999999999, 0, 1.5707899999999999, -0.7853, 0.040000000000000001, 0.040000000000000001], 
                    freejoint = False, 
                    attach_to = [+0.4, -0.15, 0.0, 0.7071068 , 0, 0, 0.7071068 ], 
                    parallel_jaw = True, 
                    add_bodies = [ 
                        NewBodyConfig(attach_to = "right_finger", \
                                      body_name = "right_finger_base", pos = [0.0, 0.02, 0.0]),
                        NewBodyConfig(attach_to = "right_finger", \
                                        body_name = "right_finger_tip", pos = [0, 0, 0.05]), 
                        NewBodyConfig(attach_to = "left_finger", \
                                        body_name = "left_finger_base", pos = [0.0, 0.02, 0.0]),
                        NewBodyConfig(attach_to = "left_finger", \
                                        body_name = "left_finger_tip", pos = [0, 0, 0.05]),
                    ], 
                    
                ), 
    }, 

    "qpos2ctrl": qpos2ctrl, 
    "obj_startidx": (7+2) , 
        
    "points" : { 

        "right_lb":     FingerKeypoints("right", 3, "right_lb_target", "r_robot/left_finger_base", type = "body"),
        "right_lf":     FingerKeypoints("right", 4, "right_lf_target", "r_robot/left_finger_tip", type = "body"),
        "right_rb":     FingerKeypoints("right", 8, "right_rb_target", "r_robot/right_finger_base", type = "body"),
        "right_rf":     FingerKeypoints("right", 9, "right_rf_target", "r_robot/right_finger_tip", type = "body"),
    },

    "avp_calib": { 

        "right_lb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_lf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_rb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_rf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

    }, 

    "ik_task" : [
        IKTasks(target = "right_lb"), 
        IKTasks(target = "right_lf", pos_cost = 1.5),
        IKTasks(target = "right_rb"),
        IKTasks(target = "right_rf", pos_cost = 1.5),
    ],

    "joints" : ['r_robot/joint{}'.format(i) for i in range(1, 8)], 

    "bodies":  {
        # right robot
        "r_robot/link0":   "panda_link0_right",   "r_robot/link1":   "panda_link1_right",
        "r_robot/link2":   "panda_link2_right",   "r_robot/link3":   "panda_link3_right",
        "r_robot/link4":   "panda_link4_right",   "r_robot/link5":   "panda_link5_right",
        "r_robot/link6":   "panda_link6_right",   "r_robot/link7":   "panda_link7_right",
        "r_robot/hand":    "panda_hand_right",    "r_robot/left_finger": "panda_left_finger_right",
        "r_robot/right_finger": "panda_right_finger_right",
    } 

} 
