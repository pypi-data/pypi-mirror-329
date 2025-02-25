import os 
from pathlib import Path
import yaml

_HERE = Path(__file__).resolve().parent

LOG_STORE_DIR = os.getenv('LOG_STORE_DIR', './runs')

def load_task_cfg(task): 

    # if task.yaml exists: 

    if os.path.exists(os.path.join(_HERE, "..", "cfgs", f"{task}.yaml")):

        with open(os.path.join(_HERE, "..", "cfgs", f"{task}.yaml"), "r") as f:
            return yaml.load(f, Loader = yaml.FullLoader)
        
    elif os.path.exists(os.path.join(_HERE, "..", "cfgs", f"{task}.py")):
        task_cfg = __import__(f"dart_physics.cfgs.{task}", fromlist = ["task_cfg"])

        return task_cfg.task_cfg
    
    else:
        print("First tried to load task from ", os.path.join(_HERE, "..", "cfgs", f"{task}.yaml"))
        print("Then tried to load task from ", os.path.join(_HERE, "..", "cfgs", f"{task}.py"))
        print("No task config found")
        raise ValueError(f"Task config {task} not found")
    
def load_robot_cfg(robot): 
    
    robot_cfg = __import__(f"dart_physics.robot_cfgs.{robot}", fromlist = ["robot_cfg"])

    return robot_cfg.robot_cfg

if __name__ == "__main__":

    cfg = load_robot_cfg("freefloating_dual_allegro")
    print(cfg)