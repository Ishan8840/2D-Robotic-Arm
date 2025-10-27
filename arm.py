import numpy as np
import pygame

pygame.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))

l1 = 1
l2 = 1

joint_angles = np.radians(np.array([70, 90]))

def forward_kinematics(joint_angles):
    x = l1 * np.cos(joint_angles[0]) + l2 * np.cos(joint_angles[0] + joint_angles[1])
    y = l1 * np.sin(joint_angles[0]) + l2 * np.sin(joint_angles[0] + joint_angles[1])

    return np.array([x, y])

def Jacobian(joint_angles):
    t1 = joint_angles[0]
    t2 = joint_angles[1]

    J = np.array([[-l1 * np.sin(t1) - l2 * np.sin(t1 + t2), -l2 * np.cos(t1 + t2)],
                 [l1 * np.cos(t1) + l2 * np.cos(t1 + t2), l2 * np.sin(t1 + t2)]])
    
    return J

def to_screen(pos):
    x, y = pos
    return int(WIDTH/2 + x*100), int(HEIGHT/2 - y*100)


WHITE = (255, 255, 255)
BLUE = (0, 0, 200)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(WHITE)

    x, y = forward_kinematics(joint_angles)

    start = to_screen([0,0])
    joint1 = to_screen([l1*np.cos(joint_angles[0]), l1*np.sin(joint_angles[0])])
    end = to_screen([x, y])
    pygame.draw.line(screen, BLUE, start, joint1, 3)
    pygame.draw.line(screen, BLUE, joint1, end, 3)

    pygame.display.flip()

pygame.quit()