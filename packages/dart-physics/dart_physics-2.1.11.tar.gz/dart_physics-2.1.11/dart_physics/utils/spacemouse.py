import pyspacemouse
import time
import numpy as np
import zmq

def main():     

    r_device = pyspacemouse.open(dof_callback=pyspacemouse.silent_callback, button_callback=pyspacemouse.silent_callback, DeviceNumber = 0) 
    l_device = pyspacemouse.open(dof_callback=pyspacemouse.silent_callback, button_callback=pyspacemouse.silent_callback, DeviceNumber = 2) 
    if r_device:
        # while True: 
        while True: 
            r_state, l_state = r_device.read(), l_device.read()
            # print xyz of right and left spacemouse with 3 decimals 
            # state.x, state.y, state.z 
            # in one line, use format 

            print("[L] x: {:+.3f}, y: {:+.3f}, z: {:+.3f} roll: {:+.3f}, pitch: {:+.3f}, yaw: {:+.3f}"\
                  .format(l_state.x, l_state.y, l_state.z, l_state.roll, l_state.pitch, l_state.yaw) + "       " + \
                  "[R] x: {:+.3f}, y: {:+.3f}, z: {:+.3f} roll: {:+.3f}, pitch: {:+.3f}, yaw: {:+.3f}"\
                  .format(r_state.x, r_state.y, r_state.z, r_state.roll, r_state.pitch, r_state.yaw), end="\r")
            
            time.sleep(0.01)



if __name__ == "__main__": 

    main()