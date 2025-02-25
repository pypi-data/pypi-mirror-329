import dart_physics.mink as mink
from typing import Dict 
import numpy as np 
from dart_physics.robot_cfgs import IKTasks, PostureTask, RelativeCoMTask, CoMTask, DampingTask

class DiffIK: 
    
    def __init__(self, configuration: mink.Configuration, robot_cfg: Dict, thirdperson = False): 

        self.configuration = configuration
        self.model = self.configuration.model
        self.data = self.configuration.data 

        self.thirdperson = thirdperson

        self.tasks = [] 

        self.regulation_tasks = [ ] 
        self.scales = [] 

        regulation_tasks = robot_cfg.get("regulation_task", [])

        for task in regulation_tasks: 
            # task: PostureTask or RelativeCoMTask or CoMTask
            if isinstance(task, PostureTask): 
                t: PostureTask
                t = mink.PostureTask(model=self.model, cost=task.cost)

                if task.qpos is not None: 
                    t.set_target(task.qpos)
                else:   
                    t.set_target_from_configuration(self.configuration)

                if task.disable_joints is not None: 
                    t.disable_joints(task.disable_joints)

                self.regulation_tasks.append(t)

            elif isinstance(task, RelativeCoMTask): 
                t = mink.RelativeComTask(root_name=task.root_name, root_type=task.root_type, cost=task.cost)
                t.set_target_from_configuration(self.configuration)
                self.regulation_tasks.append(t)
            elif isinstance(task, CoMTask): 
                t = mink.ComTask(cost=task.cost)
                t.set_target_from_configuration(self.configuration)
                self.regulation_tasks.append(t)

            elif isinstance(task, DampingTask): 
                t = mink.DampingTask(model=self.model, cost=task.cost)
                t.disable_joints(task.disable_joints)
                self.regulation_tasks.append(t)


        for task in robot_cfg['ik_task']: 
            task: IKTasks

            point = "points" if not self.thirdperson else "reverse_points"

            # if frame is tuple: 
            if task.type == "relative":

                root = robot_cfg[point][task.root]
                target = robot_cfg[point][task.target]

                pos_cost = task.pos_cost
                ori_cost = task.ori_cost

                self.tasks.append(mink.RelativeFrameTask(
                    root_name = root.body_frame,
                    root_type = root.type,
                    frame_name = target.body_frame,
                    frame_type = target.type,
                    position_cost = pos_cost,
                    orientation_cost = ori_cost
                ))
                self.scales.append(task.scale)

            elif task.type == "absolute":

                target = robot_cfg[point][task.target]
                
                pos_cost = task.pos_cost
                ori_cost = task.ori_cost

                self.tasks.append(mink.FrameTask(
                    frame_name = target.body_frame,
                    frame_type = "body",
                    position_cost = pos_cost,
                    orientation_cost = ori_cost,
                ))
                self.scales.append(task.scale)

        
        joint_names = robot_cfg["joints"]
        
        max_velocities = {joint: 10 * np.pi for joint in joint_names}

        self.solver = "quadprog"
        self.pos_threshold = 1e-4
        self.ori_threshold = 1e-4
        self.max_iters = 20

        self.limits = [
            mink.ConfigurationLimit(model = self.model, gain= 0.99,  min_distance_from_limits=0.0001),
            # velocity_limit,
            # mink.CollisionAvoidanceLimit(
            #     model=self.model,
            #     geom_pairs=collision_pairs,
            #     minimum_distance_from_collisions=0.01,
            #     collision_detection_distance=0.01,
            # ),
        ]



    def solve(self): 

        """
        input: targets containing dictionary of mocap frames
        """

        try:
            vel = mink.solve_ik(
                self.configuration, self.tasks + self.regulation_tasks, 0.002, self.solver, 1e-3, limits=self.limits,  
            )

            qtarget = self.configuration.integrate(vel, 0.002)

            return qtarget
        
        except Exception as e: 

            print(e)

            return self.configuration.data.qpos 

    def update(self, q): 
        self.configuration.update(q=q)
