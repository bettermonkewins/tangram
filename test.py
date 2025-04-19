import pygame
import socket

# Initialize the controller
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Set up socket
HOST = "172.16.141.155"  # Replace with your Raspberry Pi's IP address
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        pygame.event.pump()
        axis_0 = joystick.get_axis(0)  # Left stick X-axis
        axis_1 = joystick.get_axis(1)  # Left stick Y-axis
        message = f"{axis_0},{axis_1}"
        sock.sendto(message.encode(), (HOST, PORT))
except KeyboardInterrupt:
    print("Closing connection")
finally:
    sock.close()
    pygame.quit()