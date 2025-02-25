import grpc
from concurrent import futures
import time
import threading
import numpy as np
from dart_physics.avp_stream3.grpc_msg import * 
from dart_physics.avp_stream3.utils.grpc_utils import * 
from flask import Flask, request, jsonify
from PIL import Image
import io 
import cv2 
from dart_physics.utils.run_functions import rot_x

YUP2ZUP = np.array([[[1, 0, 0, 0], 
                    [0, 0, -1, 0], 
                    [0, 1, 0, 0],
                    [0, 0, 0, 1]]], dtype = np.float64)

ZUP2YUP = np.array([[1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, -1, 0, 0],
                    [0, 0, 0, 1]], dtype = np.float64)


class HandTrackingServer:

    def __init__(self, port=12350):
        self.port = port
        self.latest = None
        self.axis_transform = YUP2ZUP
        self.send_sim_states = True 
        self.sim_states = dexterity_pb2.SimStates()
        self.sim_states.matrices["left_hand"].CopyFrom(matrix4x4_to_proto(np.eye(4)))
        
        self.convert = np.array([[-1. ,  0. ,  0. ,  0. ],
            [ 0. , -1. ,  0. ,  0.6],
            [ 0. ,  0. ,  1. ,  0. ],
            [ 0. ,  0. ,  0. ,  1. ]])
        
        self.thirdperson = False 

        # self.cap = cv2.VideoCapture(0) # MODIFY TO CORRECT PORT
        resolution = (1280, 480)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

        ret = False
        # while not ret: 

        #     ret, image = self.cap.read() # reads frame that has stereo images side by side
        #     if not ret:
        #         print("failed to grab")
        #         return 
            
        #     image = cv2.rotate(image, cv2.ROTATE_180)
        #     # print("real_image:", image.shape)
        #     w = image.shape[1]//2
        #     h = image.shape[0]
        #     im_left = image[:, :w]
        #     im_right = image[:, w:2*w]
            
        #     _, buffer = cv2.imencode('.jpg', im_left)
        #     _, buffer2 = cv2.imencode('.jpg', im_right)
        #     # print("encoded both")
            
        #     # # Here, the server will yield the current stereo images that are set
        self.stereo_image = dexterity_pb2.StereoImage() # left_image = buffer.tobytes(), right_image = buffer2.tobytes())


    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
        dexterity_pb2_grpc.add_HandTrackingServiceServicer_to_server(
            self.HandTrackingServicer(self), self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        print(f"Server started, listening on port {self.port}")
        threading.Thread(target=self._keep_alive, daemon=True).start()

    def stop(self):
        if self.server:
            self.server.stop(0)
            print("Server stopped")

    def _keep_alive(self):
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            self.stop()

    def get_latest(self):
        return self.latest

    class HandTrackingServicer(dexterity_pb2_grpc.HandTrackingServiceServicer):
        def __init__(self, outer):
            print("HandTrackingServicer init")
            self.outer = outer


        def StreamHandUpdatesandGetSimStates(self, request_iterator, context):
            for hand_update in request_iterator:
                try: 
                    start_transformation_time = time.time()
                    # print(f"Transformation started at: {start_transformation_time} seconds")
                    transformations = {
                        "left_wrist": self.outer.axis_transform @ process_matrix(hand_update.left_hand.wristMatrix),
                        "right_wrist": self.outer.axis_transform @ process_matrix(hand_update.right_hand.wristMatrix),
                        "left_fingers": process_matrices(hand_update.left_hand.skeleton.jointMatrices),
                        "right_fingers": process_matrices(hand_update.right_hand.skeleton.jointMatrices),
                        "head": rotate_head(self.outer.axis_transform @ process_matrix(hand_update.Head)),
                        "left_pinch_distance": get_pinch_distance(hand_update.left_hand.skeleton.jointMatrices),
                        "right_pinch_distance": get_pinch_distance(hand_update.right_hand.skeleton.jointMatrices),
                    }
                    transformations["right_wrist_roll"] = get_wrist_roll(transformations["right_wrist"])
                    transformations["left_wrist_roll"] = get_wrist_roll(transformations["left_wrist"])

                    self.outer.latest = transformations
                    end_transformation_time = time.time()
                    # print(f"Transformation ended at: {end_transformation_time} seconds")
                    elapsed_time = end_transformation_time - start_transformation_time
                    # print(f"Elapsed time: {elapsed_time * 1000} ms")
                    
                    # You can add any processing here to fill sim_states based on transformations
                    if self.outer.send_sim_states: 
                        yield self.outer.sim_states
                    else: 
                        yield dexterity_pb2.SimStates()

                except Exception as e: 
                    print(e)


        def StreamHandUpdatesandGetStereoImages(self, request_iterator, context):
            for hand_update in request_iterator:
                try:

                    # print(f"Transformation started at: {start_transformation_time} seconds")
                    transformations = {
                        "left_wrist": self.outer.axis_transform @ process_matrix(hand_update.left_hand.wristMatrix),
                        "right_wrist": self.outer.axis_transform @ process_matrix(hand_update.right_hand.wristMatrix),
                        "left_fingers": process_matrices(hand_update.left_hand.skeleton.jointMatrices),
                        "right_fingers": process_matrices(hand_update.right_hand.skeleton.jointMatrices),
                        "head": rotate_head(self.outer.axis_transform @ process_matrix(hand_update.Head)  @ rot_x(60)),
                        "left_pinch_distance": get_pinch_distance(hand_update.left_hand.skeleton.jointMatrices),
                        "right_pinch_distance": get_pinch_distance(hand_update.right_hand.skeleton.jointMatrices),
                    }
                    transformations["right_wrist_roll"] = get_wrist_roll(transformations["right_wrist"])
                    transformations["left_wrist_roll"] = get_wrist_roll(transformations["left_wrist"])

                    self.outer.latest = transformations

                    # print("real_image:", image.shape)
                    # w = image.shape[1]//2
                    # h = image.shape[0]
                    # im_left = image[:, :w]
                    # im_right = image[:, w:2*w]
                    
                    # _, buffer = cv2.imencode('.jpg', im_left)
                    # _, buffer2 = cv2.imencode('.jpg', im_right)
                    # print("encoded both")
                    
                    # # Here, the server will yield the current stereo images that are set
                    # yield dexterity_pb2.StereoImage(left_image = buffer.tobytes(), right_image = buffer2.tobytes())

                    yield self.outer.stereo_image

                except Exception as e:
                    print(f"Error streaming stereo images: {e}")


        def Check(self, request, context):
            response = dexterity_pb2.HealthCheckResponse()
            response.status = dexterity_pb2.HealthCheckResponse.SERVING
            return response

    def set_sim_states(self, sim_dict):
        # You can add any processing here to set sim_states
        for key, value in sim_dict.items(): 
            if self.thirdperson: 
                self.sim_states.matrices[key].CopyFrom(matrix4x4_to_proto(ZUP2YUP @ self.convert @ value))
            else: 
                self.sim_states.matrices[key].CopyFrom(matrix4x4_to_proto(ZUP2YUP @ value))

    # Method to update stereo images, automatically applying JPEG encoding
    def set_image_states(self, stereo_image_np, stereo = False):
        # Extract the numpy arrays from the input dictionary
        image = stereo_image_np
        # convert rgb to bgr
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if stereo: 
            w = image.shape[1] // 2
            h = image.shape[0]
            print("sim_image:", image.shape)

            # Split the image into left and right
            im_left = image[:,:w]
            im_right = image[:,w:2*w]

            _, buffer_left = cv2.imencode('.jpg', im_left)
            _, buffer_right = cv2.imencode('.jpg', im_right)


        else:

            # Encode both images as JPEG using OpenCV
            _, buffer_left = cv2.imencode('.jpg', image)
            _, buffer_right = cv2.imencode('.jpg', image)

        # Create and set the StereoImage message
        stereo_image = dexterity_pb2.StereoImage(left_image = buffer_left.tobytes(), right_image = buffer_right.tobytes())

        self.stereo_image = stereo_image

        # ret, image = self.cap.read() # reads frame that has stereo images side by side
        # if not ret:
        #     print("failed to grab")
        #     return 

        # # split image in half
        # image = cv2.rotate(image, cv2.ROTATE_180)
        # w = image.shape[1]//2
        # h = image.shape[0]
        # im_left = image[:, :w]
        # im_right = image[:, w:2*w]
        
        # _, buffer = cv2.imencode('.jpg', im_left)
        # _, buffer2 = cv2.imencode('.jpg', im_right)
        # print("encoded both")

        # self.stereo_image.left_image = buffer.tobytes()
        # self.stereo_image.right_image = buffer2.tobytes()
        # pass 



    def _encode_jpeg(self, image):
        """Encodes a PIL image to JPEG format."""
        try:
            output = io.BytesIO()
            image.save(output, format='JPEG')
            jpeg_data = output.getvalue()

            return jpeg_data
        
        except Exception as e:
            print(f"JPEG encoding error: {e}")
            return None



# Usage example
if __name__ == '__main__':


    server = HandTrackingServer()
    server.start()

    try:
        while True:
            latest = server.get_latest()
            if latest:
                pass
                # print(f"Latest head position: {latest['head'][0, :3, 3]}")
    except KeyboardInterrupt:
        server.stop()