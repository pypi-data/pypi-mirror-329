import zmq
import threading
import time 

class ALOHAZMQSubscriber(threading.Thread):
    def __init__(self, zmq_port):
        """
        Initializes the ZMQSubscriber, connects to the ZMQ publisher, and starts the thread.
        
        :param zmq_port: The ZMQ port to connect to for receiving data.
        """
        super(ALOHAZMQSubscriber, self).__init__()
        self.zmq_port = zmq_port
        self.latest = None  # Store the latest received data
        self.keep_running = True
        
        # Setup ZMQ subscriber socket
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(f"tcp://128.31.35.92:{zmq_port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')  # Subscribe to all messages

    def run(self):
        """
        Run method to receive ZMQ messages in the background and continuously update `self.latest`.
        """
        while self.keep_running:
            try:
                # Receive the message (deserialized NumPy array)
                self.latest = self.socket.recv_pyobj()

            except zmq.ZMQError as e:
                print(f"ZMQ Error: {e}")
                break
    
    def stop(self):
        """
        Stop the ZMQ subscriber thread.
        """
        self.keep_running = False
        self.socket.close()

# Usage example in your main launch script
if __name__ == "__main__":
    zmq_port = 5555  # Replace with the port you're using for ZMQ

    # Instantiate the subscriber
    zmq_sub = ALOHAZMQSubscriber(zmq_port)

    # Start the subscriber thread
    zmq_sub.start()

    try:
        while True:
            # Read the latest data at your own pace
            if zmq_sub.latest is not None:
                print(f"Latest concatenated joint data: {zmq_sub.latest}")
            
            # Simulate doing other tasks in your main thread
            time.sleep(1)

    except KeyboardInterrupt:
        print("Shutting down...")
    
    finally:
        # Stop the ZMQ subscriber thread
        zmq_sub.stop()
        zmq_sub.join()
