import numpy as np
import pygame

pygame.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))

l1 = 100
l2 = 100

joint_angles = np.radians(np.array([70, 90]))

def forward_kinematics(joint_angles):
    x = l1 * np.cos(joint_angles[0]) + l2 * np.cos(joint_angles[0] + joint_angles[1])
    y = l1 * np.sin(joint_angles[0]) + l2 * np.sin(joint_angles[0] + joint_angles[1])

    return np.array([x, y])

def Jacobian(joint_angles):
    t1 = joint_angles[0]
    t2 = joint_angles[1]

    J = np.array([[-l1 * np.sin(t1) - l2 * np.sin(t1 + t2), -l2 * np.sin(t1 + t2)],
                 [l1 * np.cos(t1) + l2 * np.cos(t1 + t2), l2 * np.cos(t1 + t2)]])
    
    return J


WHITE = (255, 255, 255)
BLUE = (0, 0, 200)

target = forward_kinematics(joint_angles)

Kp = 0.1
Ki = 0
Kd = 0
integral = 0
prev_error = 0
dt = 0.1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            target = np.array(pygame.mouse.get_pos())
            print(target)
     
    screen.fill(WHITE)
    
    position = forward_kinematics(joint_angles)
    origin = np.array([300, 200])
    error = (target - position) - origin

    derivative = (error - prev_error) / dt
    integral += error * dt
    desired_v = Kp*error + Kd*derivative + Ki*integral

    J = Jacobian(joint_angles)

    theta_v = np.linalg.pinv(J) @ desired_v

    joint_min = np.radians([-360, 0])
    joint_max = np.radians([360, 180])
    joint_angles += theta_v * dt

    joint_angles = np.clip(joint_angles, joint_min, joint_max)

    prev_error = error

    pygame.draw.line(screen, BLUE, (300, 200), (300 + l1*np.cos(joint_angles[0]), 200 + l1*np.sin(joint_angles[0])), 3)
    pygame.draw.line(screen, BLUE, (300 + l1*np.cos(joint_angles[0]), 200 + l1*np.sin(joint_angles[0])), (300 + position[0], 200 + position[1]), 3)

    pygame.display.flip()

pygame.quit()