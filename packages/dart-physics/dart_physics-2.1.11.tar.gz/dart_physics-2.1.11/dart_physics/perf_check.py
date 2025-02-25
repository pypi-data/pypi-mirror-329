from dart_physics.runs import * 
from dart_physics.utils.scene_gen import construct_scene
import mujoco
from dart_physics.utils.loop_rate_limiter import RateLimiter
import time 
import sys
import contextlib

# A helper context manager to suppress print statements
@contextlib.contextmanager
def suppress_print():
    # Redirect standard output to None temporarily
    with open(os.devnull, 'w') as fnull:
        old_stdout = sys.stdout
        sys.stdout = fnull
        try:
            yield
        finally:
            # Restore the original stdout
            sys.stdout = old_stdout


def check_perf(robot, task):
    with suppress_print():

        robot_cfg = load_robot_cfg(robot)
        task_cfg = load_task_cfg(task)

        model, root = construct_scene(task_cfg, robot_cfg)
        data = mujoco.MjData(model)
        
        mujoco.mj_resetDataKeyframe(model, data, 0)
        mujoco.mj_forward(model, data)
        mujoco.mj_camlight(model, data)

    times = [] 

    rate = RateLimiter(500, warn = False)


    for _ in range(1000): 

        start = time.time()
        mujoco.mj_step(model, data)
        
        rate.sleep()
        end = time.time()
        times.append(end - start)

    print(f"[{robot} | {task}] Average FPS: {1 / (sum(times) / len(times))} | Real-time ratio: {1 / (sum(times) / len(times)) / 500}")



if __name__ == "__main__":

    check_perf("dual_panda", "bimanual_insertion")
    check_perf("aloha", "bolt_nut_sort")
    check_perf("rby1", "rubiks_cube")

    