# network_utils.py: flat functions for network services (sending/receiving socket messages)

import socket

XT_CONTROLLER_PORT = 12345

def send_msg_to_xt_controller(msg):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()

    # Connection to hostname on the port
    client_socket.connect((host, XT_CONTROLLER_PORT))

    # Send a simple 'go' signal
    client_socket.send(msg.encode('utf-8'))

    # Close the connection
    client_socket.close()


def xt_controller_msg_receiver(msg_action_dict):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()

    # Bind to the port
    server_socket.bind((host, XT_CONTROLLER_PORT))

    # Queue up to 5 requests
    server_socket.listen(5)

    while True:
        # Establish a connection
        client_socket, addr = server_socket.accept()

        # Receive the message
        msg = client_socket.recv(1024)
        msg_text = msg.decode('utf-8')
        #print("xt controller received message: %s" % msg_text)

        # Process the message
        if msg_text in msg_action_dict:
            action = msg_action_dict[msg_text]

            # call the action for this msg
            action()
        else:
            print("xt_controller_msg_receiver: unknown message received: %s" % msg_text)

        # Close the connection
        client_socket.close()

def run_msg_reciever_on_bg_thread(msg_action_dict):
    import threading

    msg_thread = threading.Thread(target=xt_controller_msg_receiver, args=(msg_action_dict,), daemon=True)
    msg_thread.start()
    

