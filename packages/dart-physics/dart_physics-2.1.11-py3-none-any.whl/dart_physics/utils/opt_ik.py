import time
import math
import numpy as np

from adam.jax import KinDynComputations
from adam.geometry import utils
import jax.numpy as jnp
from jax import jit, grad
from scipy.optimize import minimize, Bounds
from scipy import optimize
from scipy.spatial.transform import Rotation as R
from pathlib import Path 
import os
# from torchmin import minimize

CUR_PATH  = Path(__file__).resolve().parent

flags = 0
eps = 1e-6
eta1 = 1e-4
eta2 = 3e-2
beta = 1
gamma = 2.5e-10


class OptIK:
    def __init__(self, robot = 'ur3', chilarity="right", with_hand = False):
        
        if robot == 'ur3': 
            self.joint_names = ["j_shoulder_pan_joint",
                                "j_shoulder_lift_joint",
                                "j_elbow_joint",
                                "j_wrist_1_joint",
                                "j_wrist_2_joint",
                                "j_wrist_3_joint",
                                ]
        
            urdf_path = os.path.join(CUR_PATH, '../assets', 'ur3e.urdf')
            kinDyn = KinDynComputations(urdf_path,
                                        self.joint_names, 'base_link')

            self.fk = kinDyn.forward_kinematics_fun('wrist_axis')

            # lb = [-6.283185307179586, -6.283185307179586, -3.141592653589793, -6.283185307179586, -6.283185307179586, -15.]
            # ub = [6.283185307179586, 6.283185307179586, 3.141592653589793, 6.283185307179586, 6.283185307179586, 15.]

            lb = [-3.14] * 5 + [-3.14 * 3]
            ub = [+3.14] * 5 + [+3.14 * 3]

            self.bounds = Bounds(lb=lb,
                                ub=ub)

            self.num_joints = len(self.joint_names)

            if chilarity == "right":
                self.init_start_angles = np.array([1.570796, -1.570796, 1.2, -2.7707, -1.570796, -1.570796])
            else:
                self.init_start_angles = np.array([-1.570796, -1.570796, -1.2, -0.3707, 1.570796, -1.570796])

            # self.start_angles = np.zeros(self.num_joints)
            # start angles from floating_finger_env -> create_robot_env -> default_dof_pos_tensor
            # wrists positioned such that palms go down, with thumbs pointing towards each other
            if chilarity == "right":
                self.start_angles = np.array([1.570796, -1.570796, 1.2, -2.7707, -1.570796, -1.570796])
            else:
                self.start_angles = np.array([-1.570796, -1.570796, -1.2, -0.3707, 1.570796, -1.570796])
            self.prev_angles = self.start_angles


        if robot == 'ur5': 
            self.joint_names = ["shoulder_pan_joint",
                                "shoulder_lift_joint",
                                "elbow_joint",
                                "wrist_1_joint",
                                "wrist_2_joint",
                                "wrist_3_joint",
                                ]

            from robot_descriptions import ur5_description        
            urdf_path = ur5_description.URDF_PATH
            kinDyn = KinDynComputations(urdf_path,
                                        self.joint_names, 'base_link_inertia')

            self.fk = kinDyn.forward_kinematics_fun('tool0')

            lb = [-3.14] * 5 + [-3.14 * 3]
            ub = [+3.14] * 5 + [+3.14 * 3]
            # lb =


            self.bounds = Bounds(lb=lb,
                                ub=ub)

            self.num_joints = len(self.joint_names)

            if chilarity == "right":
                self.init_start_angles = np.array([1.570796, -1.570796, 1.2, -2.7707, -1.570796, -1.570796])
            else:
                self.init_start_angles = np.array([-1.570796, -1.570796, -1.2, -0.3707, 1.570796, -1.570796])

            # self.start_angles = np.zeros(self.num_joints)
            # start angles from floating_finger_env -> create_robot_env -> default_dof_pos_tensor
            # wrists positioned such that palms go down, with thumbs pointing towards each other
            if chilarity == "right":
                self.start_angles = np.array([1.570796, -1.570796, 1.2, -2.7707, -1.570796, -1.570796])
            else:
                self.start_angles = np.array([-1.570796, -1.570796, -1.2, -0.3707, 1.570796, -1.570796])
            self.prev_angles = self.start_angles



        elif robot == 'panda':
            self.joint_names = ["panda_joint1",
                                "panda_joint2",
                                "panda_joint3",
                                "panda_joint4",
                                "panda_joint5",
                                "panda_joint6",
                                "panda_joint7",
                                ]
            # from robot_descriptions import panda_description
            # urdf_path = panda_description.URDF_PATH
            # copy this urdf to ./assets/panda.urdf
            # import shutil 
            # shutil.copy(urdf_path, os.path.join(CUR_PATH, '../assets', 'panda.urdf'))
            urdf_path = os.path.join(CUR_PATH, '../assets', 'panda.urdf')
            kinDyn = KinDynComputations(urdf_path,
                                        self.joint_names, 'panda_link0')

            self.fk1 = kinDyn.forward_kinematics_fun('panda_leftfinger_tip')
            self.fk2 = kinDyn.forward_kinematics_fun('panda_rightfinger_tip')

            lb = [-3.14] * 8
            ub = [+3.14] * 8

            self.bounds = Bounds(lb=lb,
                                ub=ub)

            self.num_joints = len(self.joint_names)

            self.init_start_angles = np.array([0.0, -0.785398, 0.0, -2.35619, 0.0, 1.5708, 0.785398, 0])

            self.start_angles = np.array([0.0, -0.785398, 0.0, -2.35619, 0.0, 1.5708, 0.785398, 0])
            self.prev_angles = self.start_angles


        self.compile()

    def compute_fk(self, angles):
        return self.fk(jnp.eye(4), angles)

    def cost(self, angles, r_h, prev_angles, close_joints_coefficient):
        H_b = jnp.eye(4)

        tf_w = self.fk1(H_b, angles)

        cost = 0

        # cost += jnp.linalg.norm(tf_w.flatten() - r_h.flatten()) ** 2 

        tf_w_rot = tf_w[:3, :3]
        r_h_rot = r_h[:3, :3]

        rot_error = tf_w_rot.flatten() - r_h_rot.flatten()
        cost += jnp.dot(rot_error, rot_error) * 1e-2

        tf_w_pos = tf_w[:3, 3]
        r_h_pos = r_h[:3, 3]

        pose_error = tf_w_pos.flatten() - r_h_pos.flatten()
        cost += jnp.dot(pose_error, pose_error)

        angle_error = angles - prev_angles
        cost += close_joints_coefficient * jnp.dot(angle_error, angle_error)
        # cost += close_joints_coefficient * jnp.sum(() ** 2)
        return cost

    def compile(self):
        self.fast_c = jit(self.cost, backend='cpu')
        self.grad_c = jit(grad(self.fast_c), backend='cpu')
        self.fast_fk = jit(self.compute_fk, backend='cpu')

        print('compiled!')

    def retarget(self, target_se3_in_world_frame, return_cost=False, close_joints_coefficient=1e-2):
        """
        r_h: vector of fingertip targets
        """

        # print(r_h)

        res = minimize(self.fast_c,
                       self.start_angles, method="SLSQP", args=(target_se3_in_world_frame, self.prev_angles,
                                                                close_joints_coefficient),
                       jac=self.grad_c, tol=1e-10, options={'maxiter': 6000}, bounds=self.bounds,
                       )
        self.prev_angles = res.x
        self.start_angles = res.x

        #print("arm retargeter")
        #print("optimal value")
        #print(self.start_angles)

        if return_cost:
            return res.x, res.fun  # ,  [fk1[:3,-1], fk2[:3,-1], fk3[:3,-1], fk4[:3,-1]]
        else:
            return res.x


class PandaOptIK:
    def __init__(self, chilarity="right", with_hand = False):
        
        self.joint_names = ["panda_joint1",
                            "panda_joint2",
                            "panda_joint3",
                            "panda_joint4",
                            "panda_joint5",
                            "panda_joint6",
                            "panda_joint7",
                            ]
        # from robot_descriptions import panda_description
        # urdf_path = panda_description.URDF_PATH
        # copy this urdf to ./assets/panda.urdf
        # import shutil 
        # shutil.copy(urdf_path, os.path.join(CUR_PATH, '../assets', 'panda.urdf'))
        urdf_path = os.path.join(CUR_PATH, '../assets', 'panda.urdf')
        kinDyn = KinDynComputations(urdf_path,
                                    self.joint_names, 'panda_link0')

        self.fk1 = kinDyn.forward_kinematics_fun('panda_leftfinger_tip')
        self.fk2 = kinDyn.forward_kinematics_fun('panda_rightfinger_tip')

        self.fk1_b = kinDyn.forward_kinematics_fun('panda_leftfinger_base')
        self.fk2_b = kinDyn.forward_kinematics_fun('panda_rightfinger_base')

        lb = [-3.14 * 2] * 8
        ub = [+3.14 * 2] * 8

        self.bounds = Bounds(lb=lb,
                            ub=ub)

        self.num_joints = len(self.joint_names)

        self.init_start_angles = np.array([0.0, -0.785398, 0.0, -2.35619, 0.0, 1.5708, 0.785398, 0])

        self.start_angles = np.array([0.0, -0.785398, 0.0, -2.35619, 0.0, 1.5708, 0.785398, 0])
        self.prev_angles = self.start_angles

        self.home_angles = np.array([0, 0, 0, -1.5707899999999999, 0, 1.5707899999999999, -0.7853, 0.0 ]) 

        self.compile()

    def compute_fk1(self, angles):
        return self.fk1(jnp.eye(4), angles)
    
    def compute_fk2(self, angles):
        return self.fk2(jnp.eye(4), angles)
    
    def compute_fk3(self, angles):
        return self.fk3(jnp.eye(4), angles)

    def cost(self, angles, fingertip_1b, fingertip_2b, fingertip_1, fingertip_2, prev_angles, close_joints_coefficient):
        H_b = jnp.eye(4)

        tf_w1 = self.fk1(H_b, angles)
        tf_w2 = self.fk2(H_b, angles)
        tf_w1b = self.fk1_b(H_b, angles)
        tf_w2b = self.fk2_b(H_b, angles)

        cost = 0

        # tf_w_rot1 = tf_w1[:3, :3]
        # tf_w_rot2 = tf_w2[:3, :3]
        # r_h_rot1 = fingertip_1[:3, :3]
        # r_h_rot2 = fingertip_2[:3, :3]

        # rot_error1 = tf_w_rot1.flatten() - r_h_rot1.flatten()
        # rot_error2 = tf_w_rot2.flatten() - r_h_rot2.flatten()
        # cost += jnp.dot(rot_error1, rot_error1) * 1e-5
        # cost += jnp.dot(rot_error2, rot_error2) * 1e-5

        tf_w_pos1 = tf_w1[:3, 3]
        tf_w_pos2 = tf_w2[:3, 3]
        tf_w_pos1b = tf_w1b[:3, 3]
        tf_w_pos2b = tf_w2b[:3, 3]

        r_h_pos1 = fingertip_1[:3, 3]
        r_h_pos2 = fingertip_2[:3, 3]
        r_h_pos1b = fingertip_1b[:3, 3]
        r_h_pos2b = fingertip_2b[:3, 3]


        pose_error1 = tf_w_pos1.flatten() - r_h_pos1.flatten()
        pose_error2 = tf_w_pos2.flatten() - r_h_pos2.flatten()
        pose_error3 = tf_w_pos1b.flatten() - r_h_pos1b.flatten()
        pose_error4 = tf_w_pos2b.flatten() - r_h_pos2b.flatten()

        cost += jnp.dot(pose_error1, pose_error1) * 1.0
        cost += jnp.dot(pose_error2, pose_error2) * 1.0
        cost += jnp.dot(pose_error3, pose_error3) * 0.1  #e-2
        cost += jnp.dot(pose_error4, pose_error4) * 0.1 #e-2

        angle_error = angles - prev_angles
        cost += close_joints_coefficient * jnp.dot(angle_error, angle_error)

        dist_to_home_angle = angles - self.home_angles
        cost += 1e-5 * jnp.dot(dist_to_home_angle, dist_to_home_angle)

        return cost

    def compile(self):
        self.fast_c = jit(self.cost, backend='cpu')
        self.grad_c = jit(grad(self.fast_c), backend='cpu')
        self.fast_fk1 = jit(self.compute_fk1, backend='cpu')
        self.fast_fk2 = jit(self.compute_fk2, backend='cpu')

        print('compiled!')

    def retarget(self, fingertip_1b_se3, fingertip_2b_se3, fingertip_1_se3, fingertip_2_se3, return_cost=False, close_joints_coefficient=1e-2):
        """
        r_h: vector of fingertip targets
        """

        # print(r_h)

        res = minimize(self.fast_c,
                       self.start_angles, method="SLSQP", args=(fingertip_1b_se3, fingertip_2b_se3, fingertip_1_se3, fingertip_2_se3, self.prev_angles,
                                                                close_joints_coefficient),
                       jac=self.grad_c, tol=1e-10, options={'maxiter': 3000}, bounds=self.bounds,
                       )
        self.prev_angles = res.x
        self.start_angles = res.x

        #print("arm retargeter")
        #print("optimal value")
        #print(self.start_angles)

        if return_cost:
            return res.x, res.fun  # ,  [fk1[:3,-1], fk2[:3,-1], fk3[:3,-1], fk4[:3,-1]]
        else:
            return res.x


class FR3AgileHandOptIK:
    def __init__(self, chilarity="right", with_hand = False):
        
        self.joint_names = ["panda_joint1",
                            "panda_joint2",
                            "panda_joint3",
                            "panda_joint4",
                            "panda_joint5",
                            "panda_joint6",
                            "panda_joint7",

                            "right_thumb_0", 
                            "right_thumb_1",
                            "right_thumb_2",
                            "right_thumb_3",

                            "right_index_0",
                            "right_index_1",
                            "right_index_2",
                            "right_index_3",

                            "right_middle_0",
                            "right_middle_1",
                            "right_middle_2",
                            "right_middle_3",

                            "right_ring_0",
                            "right_ring_1",
                            "right_ring_2",
                            "right_ring_3",

                            "right_little_0",
                            "right_little_1",
                            "right_little_2",
                            "right_little_3",

                            ]
        # urdf_path = panda_description.URDF_PATH
        # copy this urdf to ./assets/panda.urdf
        # import shutil 
        # shutil.copy(urdf_path, os.path.join(CUR_PATH, '../assets', 'panda.urdf'))
        urdf_path = os.path.join(CUR_PATH, '../assets', 'fr3_agilehand', 'fr3_agilehand.urdf')
        kinDyn = KinDynComputations(urdf_path,
                                    self.joint_names, 'panda_link0')

        self.fk_wrist = kinDyn.forward_kinematics_fun('panda_link8')
        self.fk_thumb_axis = kinDyn.forward_kinematics_fun('right_thumb_phadist_axis')
        self.fk_index_axis = kinDyn.forward_kinematics_fun('right_index_phadist_axis')
        self.fk_middle_axis = kinDyn.forward_kinematics_fun('right_middle_phadist_axis')
        self.fk_ring_axis = kinDyn.forward_kinematics_fun('right_ring_phadist_axis')
        self.fk_little_axis = kinDyn.forward_kinematics_fun('right_little_phadist_axis')

        lb = [-2.74, -1.78, -2.9, -3.040, -2.81, +0.544, -3.02] \
             + [-0.262, 0, 0, 0] * 5
        ub = [+2.74, +1.78, +2.9, -0.152, +2.81, +4.520, +3.02] \
             + [+0.262, 1.48, 1.13, 1.13] * 5 

        self.bounds = Bounds(lb=lb,
                            ub=ub)

        self.num_joints = len(self.joint_names)

        self.init_start_angles = np.array([0, 0, 0, -1.5707899999999999, 0, 1.5707899999999999, -0.7853] + [0.0] * 20)  

        self.start_angles = np.array([0, 0, 0, -1.5707899999999999, 0, 1.5707899999999999, -0.7853] + [0.0] * 20)  
        self.prev_angles = self.start_angles

        self.home_angles = np.array([0, 0, 0, -1.5707899999999999, 0, 1.5707899999999999, -0.7853] + [0.0] * 20)  

        self.compile()


    def cost(self, angles, wrist, thumb, index, middle, ring, little, prev_angles, close_joints_coefficient):
        H_b = jnp.eye(4)

        tf_w_wrist = self.fk_wrist(H_b, angles)
        tf_w_thumb = self.fk_thumb_axis(H_b, angles)
        tf_w_index = self.fk_index_axis(H_b, angles)
        tf_w_middle = self.fk_middle_axis(H_b, angles)
        tf_w_ring = self.fk_ring_axis(H_b, angles)
        tf_w_little = self.fk_little_axis(H_b, angles)

        cost = 0

        # tf_w_rot1 = tf_w1[:3, :3]
        # tf_w_rot2 = tf_w2[:3, :3]
        # r_h_rot1 = fingertip_1[:3, :3]
        # r_h_rot2 = fingertip_2[:3, :3]

        # rot_error1 = tf_w_rot1.flatten() - r_h_rot1.flatten()
        # rot_error2 = tf_w_rot2.flatten() - r_h_rot2.flatten()
        # cost += jnp.dot(rot_error1, rot_error1) * 1e-5
        # cost += jnp.dot(rot_error2, rot_error2) * 1e-5

        tf_w1 = tf_w_wrist[:3, 3]
        tf_w2 = tf_w_thumb[:3, 3]
        tf_w3 = tf_w_index[:3, 3]
        tf_w4 = tf_w_middle[:3, 3]
        tf_w5 = tf_w_ring[:3, 3]
        tf_w6 = tf_w_little[:3, 3]

        rh_p1 = wrist[:3, 3]
        rh_p2 = thumb[:3, 3]
        rh_p3 = index[:3, 3]
        rh_p4 = middle[:3, 3]
        rh_p5 = ring[:3, 3]
        rh_p6 = little[:3, 3]

        tf_rot = tf_w_wrist[:3, :3]
        rh_rot = wrist[:3, :3]

        rot_error = tf_rot.flatten() - rh_rot.flatten()
        cost += jnp.dot(rot_error, rot_error) * 0.0


        pose_error1 = tf_w1.flatten() - rh_p1.flatten()
        pose_error2 = tf_w2.flatten() - rh_p2.flatten()
        pose_error3 = tf_w3.flatten() - rh_p3.flatten()
        pose_error4 = tf_w4.flatten() - rh_p4.flatten()
        pose_error5 = tf_w5.flatten() - rh_p5.flatten()
        pose_error6 = tf_w6.flatten() - rh_p6.flatten()

        cost += jnp.dot(pose_error1, pose_error1) * 1.0
        # cost += jnp.dot(pose_error2, pose_error2) * 1.0
        # cost += jnp.dot(pose_error3, pose_error3) * 1.0  #e-2
        # cost += jnp.dot(pose_error4, pose_error4) * 1.0 #e-2
        # cost += jnp.dot(pose_error5, pose_error5) * 1.0
        # cost += jnp.dot(pose_error6, pose_error6) * 1.0

        angle_error = angles - prev_angles
        cost += close_joints_coefficient * jnp.dot(angle_error, angle_error)

        # dist_to_home_angle = angles - self.home_angles
        # cost += 1e-5 * jnp.dot(dist_to_home_angle, dist_to_home_angle)

        return cost

    def compile(self):
        self.fast_c = jit(self.cost, backend='cpu')
        self.grad_c = jit(grad(self.fast_c), backend='cpu')

        print('compiled!')

    def retarget(self, wrist, thumb, index, middle, ring, little, return_cost=False, close_joints_coefficient=1e-2):
        """
        r_h: vector of fingertip targets
        """

        # print(r_h)

        res = minimize(self.fast_c,
                       self.start_angles, method="SLSQP", args=(wrist, thumb, index, middle, ring, little, self.prev_angles,
                                                                close_joints_coefficient),
                       jac=self.grad_c, tol=1e-10, options={'maxiter': 6000}, bounds=self.bounds,
                       )
        self.prev_angles = res.x
        self.start_angles = res.x

        #print("arm retargeter")
        #print("optimal value")
        #print(self.start_angles)

        if return_cost:
            return res.x, res.fun  # ,  [fk1[:3,-1], fk2[:3,-1], fk3[:3,-1], fk4[:3,-1]]
        else:
            return res.x



class G1OptIK:
    def __init__(self):
        
        self.joint_names = ["torso_joint",
                            
                            "left_shoulder_pitch_joint",
                            "left_shoulder_roll_joint",
                            "left_shoulder_yaw_joint",
                            "left_elbow_pitch_joint",
                            "left_elbow_roll_joint",

                            "right_shoulder_pitch_joint",
                            "right_shoulder_roll_joint",
                            "right_shoulder_yaw_joint",
                            "right_elbow_pitch_joint",
                            "right_elbow_roll_joint",

                            ]
        # urdf_path = panda_description.URDF_PATH
        # copy this urdf to ./assets/panda.urdf
        # import shutil 
        # shutil.copy(urdf_path, os.path.join(CUR_PATH, '../assets', 'panda.urdf'))
        urdf_path = os.path.join(CUR_PATH, '../assets', 'unitree_g1', 'g1.urdf')
        kinDyn = KinDynComputations(urdf_path,
                                    self.joint_names, 'pelvis')

        self.right_wrist_fk = kinDyn.forward_kinematics_fun('right_wrist_link')
        self.left_wrist_fk = kinDyn.forward_kinematics_fun('left_wrist_link')

        lb = [-np.pi] * 11 #[-2.62] + [-2.97, -1.59, -2.62, -0.227, -2.09, -0.524] # [-0.524, -1, 0, -1.84, -1.84, -1.84, -1.84]
        ub = [+np.pi] * 11 #[+2.74, +1.78, +2.9, -0.152, +2.81, +4.520, +3.02] \
             #+ [+0.262, 1.48, 1.13, 1.13] * 5 

        self.bounds = Bounds(lb=lb,
                            ub=ub)

        self.num_joints = len(self.joint_names)

        self.init_start_angles = np.array([0.0] * 11 )  

        self.start_angles = np.array([0.0] * 11 ) 
        self.prev_angles = self.start_angles

        self.home_angles = np.array([0.0] * 11 ) 

        self.compile()


    def cost(self, angles, right_wrist, left_wrist, prev_angles, close_joints_coefficient):
        H_b = jnp.eye(4)

        tf_w_right_wrist = self.right_wrist_fk(H_b, angles)
        tf_w_left_wrist = self.left_wrist_fk(H_b, angles)

        cost = 0

        # tf_w_rot1 = tf_w1[:3, :3]
        # tf_w_rot2 = tf_w2[:3, :3]
        # r_h_rot1 = fingertip_1[:3, :3]
        # r_h_rot2 = fingertip_2[:3, :3]

        # rot_error1 = tf_w_rot1.flatten() - r_h_rot1.flatten()
        # rot_error2 = tf_w_rot2.flatten() - r_h_rot2.flatten()
        # cost += jnp.dot(rot_error1, rot_error1) * 1e-5
        # cost += jnp.dot(rot_error2, rot_error2) * 1e-5

        right_tf_w1 = tf_w_right_wrist[:3, 3]
        right_rh_p1 = right_wrist[:3, 3]

        right_tf_rot = tf_w_right_wrist[:3, :3]
        right_rh_rot = right_wrist[:3, :3]

        right_rot_error = right_tf_rot.flatten() - right_rh_rot.flatten()
        right_pose_error = right_tf_w1.flatten() - right_rh_p1.flatten()

        cost += jnp.dot(right_rot_error, right_rot_error) * 0.0
        cost += jnp.dot(right_pose_error, right_pose_error) * 1.0

        left_tf_w1 = tf_w_left_wrist[:3, 3]
        left_rh_p1 = left_wrist[:3, 3]

        left_tf_rot = tf_w_left_wrist[:3, :3]
        left_rh_rot = left_wrist[:3, :3]

        left_rot_error = left_tf_rot.flatten() - left_rh_rot.flatten()
        left_pose_error = left_tf_w1.flatten() - left_rh_p1.flatten()

        cost += jnp.dot(left_rot_error, left_rot_error) * 0.0
        cost += jnp.dot(left_pose_error, left_pose_error) * 1.0

        angle_error = angles - prev_angles
        cost += close_joints_coefficient * jnp.dot(angle_error, angle_error)
        
        dist_to_home_angle = angles - self.home_angles
        cost += 1e-3 * jnp.dot(dist_to_home_angle, dist_to_home_angle)

        return cost

    def compile(self):
        self.fast_c = jit(self.cost, backend='cpu')
        self.grad_c = jit(grad(self.fast_c), backend='cpu')

        print('compiled!')

    def retarget(self, right_wrist, left_wrist, return_cost=False, close_joints_coefficient=1e-2):
        """
        r_h: vector of fingertip targets
        """

        # print(r_h)

        res = minimize(self.fast_c,
                       self.start_angles, method="SLSQP", args=(right_wrist, left_wrist, self.prev_angles,
                                                                close_joints_coefficient),
                       jac=self.grad_c, tol=1e-10, options={'maxiter': 6000}, bounds=self.bounds,
                       )
        self.prev_angles = res.x
        self.start_angles = res.x

        #print("arm retargeter")
        #print("optimal value")
        #print(self.start_angles)

        if return_cost:
            return res.x, res.fun  # ,  [fk1[:3,-1], fk2[:3,-1], fk3[:3,-1], fk4[:3,-1]]
        else:
            return res.x

