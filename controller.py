import pygame
import socket

# Initialize the controller
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Set up socket
HOST = "172.16.196.158"  # Replace with your Raspberry Pi's IP address
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define all da variables

pi_Num = 0
PI_COUNT = 7

A = False
B = False
ax4_held = False
ax4_held_prev = False
ax5_held = False
ax5_held_prev = False
decr = False        # decrement pi_Num if True
incr = False        # increment pi_Num if True

try:
    while True:
        pygame.event.pump()
        axis_0 = joystick.get_axis(0)  # Left stick X-axis
        axis_1 = joystick.get_axis(1)  # Left stick Y-axis
        ax4 = joystick.get_axis(4)
        ax5 = joystick.get_axis(5)

        if ax4 >= 0.9:
            ax4_held = True
        elif ax4 < 0.9:
            ax4_held = False
        decr =  not ax4_held_prev and ax4_held

        if ax5 >= 0.9:
            ax5_held = True  
        elif ax5 < 0.9:
            ax5_held = False
        incr = not ax5_held_prev and ax5_held

        if decr:
            pi_Num -= 1
            pi_Num %= PI_COUNT
        if incr:
            pi_Num += 1
            pi_Num %= PI_COUNT

        if decr or incr:
            print(pi_Num)

        ax4_held_prev = ax4_held
        ax5_held_prev = ax5_held

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(0):
                    B = False
                    A = not A
                    print(f"A: {A}, B: {B}")
                elif joystick.get_button(1):
                    A = False
                    B = not B
                    print(f"A: {A}, B: {B}")

            message = f"{axis_0},{axis_1}"
            sock.sendto(message.encode(), (HOST, PORT))
except KeyboardInterrupt:
    print("Closing connection")
finally:
    sock.close()
    pygame.quit()