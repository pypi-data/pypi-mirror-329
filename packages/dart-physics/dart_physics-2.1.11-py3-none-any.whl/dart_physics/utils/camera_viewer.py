# utils/camera_viewer.py
import zmq
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue
from threading import Thread
import time
import multiprocessing as mp

def data_receiver(socket, data_queue):
    while True:
        msg = socket.recv_pyobj()  # Receive the image data
        data_queue.put(msg)

def image_rendering_process(addr, stereo = False):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(addr)
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    data_queue = Queue()

    # Start the data receiving thread
    receiver_thread = Thread(target=data_receiver, args=(socket, data_queue))
    receiver_thread.daemon = True
    receiver_thread.start()

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()

    # Initialize the image plot with some dummy data
    if stereo: 
        img = np.zeros((640, 1920, 3), dtype=np.uint8)  # Assuming a 480x640 RGB image
    else:
        img = np.zeros((640, 960, 3), dtype=np.uint8)
    im_plot = ax.imshow(img)

    plt.tight_layout()

    while True:
        while not data_queue.empty():
            img_data = data_queue.get()

            # Update the image plot with the new image data
            im_plot.set_data(img_data)

            ax.draw_artist(im_plot)
            fig.canvas.flush_events()  # Update the plot

        time.sleep(0.01)  # Small sleep to prevent overloading the CPU

def start_camera_viewer_process(addr, stereo = False):
    # Start the image rendering process using multiprocessing
    process = mp.Process(target=image_rendering_process, args=(addr,stereo, ))
    process.start()
    return process

def get_socket(addr):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(addr)
    return socket