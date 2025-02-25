# DART-Physics

![](./assets/dexhub.png)

This is a MuJoCo-based Physics Engine compatible with [DART](). 
You can launch this on a cloud server through [dexhub.ai](https://dexhub.ai) or run locally on your machine. 

### Launching Physics Engine
![](./assets/choices.png)
1. On the Cloud: Visit [dexhub.ai](https://dexhub.ai) and request a cloud-running physics engine. 
2. On your Local Machine: Launch the server by simply running
    ```
    pip install dart_physics
    python -m dart_physics.server 
    ```
   and register the IP address of your machine through the [dexhub.ai](https://dexhub.ai) dashboard. We support all platforms including Windows, Mac, and Linux.

    > If you are running the server locally, check if your machine is powerful enough to run the physics engine real-time. 
    > You can run the following command to check the performance of your machine: 
    > ```
    > python -m dart_physics.perf_check
    > ```
    > You should see an average FPS of around 490-500, real-time ratio of around 0.95-1.00. If not, we recommend running the engine on our cloud server. 


### Acknowledgements

This project was possible thanks to the following open-source projects:

- [MuJoCo](https://mujoco.org/)
- High-fidelity MuJoCo robot models are from [MuJoCo Menagerie](https://github.com/deepmind/mujoco_menagerie).
- DART app on VisionOS is forked from [Tracking Streamer](https://github.com/dexhub-ai/tracking-streamer).
- IK solver is based on [mink](https://github.com/younghyo-park/mink).



### Importing Tasks 

0. Try to run the following and see if it's running properly
    ```
    cd dart_physics
    python server.py 
    ```

1. Get a USDZ file (either by scanning or from the internet) 
2. Convert USDZ file to OBJ file. Recommend using this [link](https://products.aspose.app/3d/conversion/usdz-to-obj).
3. Unzip the converted file, and place the unzipped folder under `dart_physics/assets/custom` 
4. **Convex Decomposition** 
    ```
    obj2mjcf --obj-dir ./assets/custom/your_new_obj --save-mjcf --verbose  --decompose
    ```
5. **Task Creation**: take a look at files under `./cfgs`. Those are task description files. Try to duplicate one for your own task. 
6. **Run the simulation**: 
    ```
    python runs/teleop.py --task YOUR_TASK --robot aloha 
    ```

    You should be able to see a mujoco viewer. 
