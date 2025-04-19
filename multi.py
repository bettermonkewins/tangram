import js

import pygame
import socket
import time

import json


# List of Raspberry Pi IPs
SERVERS = [
    ("172.16.196.158", 5005),  # Raspberry Pi 1
    ("172.16.141.155", 5005),  # Raspberry Pi 1
]

# Initialize Pygame
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

inputs = {}

# Connect to all Raspberry Pis
sockets = []
for host, port in SERVERS:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sockets.append(sock)
        print(f"Connected to {host}:{port}")
    except Exception as e:
        print(f"Failed to connect to {host}:{port} - {e}")

# Define all vars
A = False
B = False

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

i = 0

try:
    while True:
        pygame.event.pump()
        axis_0 = joystick.get_axis(0)  # Left stick X-axis
        axis_1 = joystick.get_axis(1)  # Left stick Y-axis
        i += 1
        #message = f"{axis_0},{axis_1},{float(A)},{float(B)},{float(pi_Num)},{i}\n"  # Add newline to avoid partial reads
        ax4 = joystick.get_axis(4)
        ax5 = joystick.get_axis(5)

        inputs["axis_0"] = joystick.get_axis(0)
        print(inputs)

        message = json.dumps(inputs) + "\n"
        print(len(inputs))

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

        events = list(pygame.event.get())
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
        
        inputs = js.getJS(events)


        # Send data to all connected Raspberry Pis
        for sock in sockets:
            try:
                print(json.dumps(message))
                sock.sendall(message.encode())  # Use sendall() to ensure full message is sent
            except Exception as e:
                print(f"Connection lost to {sock.getpeername()} - {e}")

        time.sleep(0.1)  # Small delay to avoid spamming
except KeyboardInterrupt:
    print("Closing connections.")
finally:
    for sock in sockets:
        sock.close()
    pygame.quit()