import math
import random
import pygame

# import time
# import matplotlib.pyplot as plt

npoints = 100

# two point distance
def pDist(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


w = 800
adjw = w / 2
adjwpad = w / 2 - w / 20

# sample randomly generated group of points
plist = []
while len(plist) < npoints:
    x = random.randint(int(-adjwpad), int(adjwpad))
    y = random.randint(int(-adjwpad), int(adjwpad))
    if pDist((x, y), (0, 0)) <= adjwpad:
        plist += [(x, y)]

pygame.init()
screen = pygame.display.set_mode((w, w))
screen.fill((0, 0, 0))


# wrapping pygame's draw.line and draw.circle
def drawLine(p1, p2, color=(255, 0, 0), width=1):
    pygame.draw.line(screen, color, (p1[0] + adjw, p1[1] + adjw), (p2[0] + adjw, p2[1] + adjw), width)


def drawCircle(p, color=(255, 255, 255), width=1):
    pygame.draw.circle(screen, color, (p[0] + adjw, p[1] + adjw), width)

# finds the bottom-most point in the group
def bPoint(pntlist):
    minp = pntlist[0]
    for p in pntlist:
        if p[1] < minp[1]:
            minp = p

    return minp


def slope(p1, p2):
    if p2[0] - p1[0] == 0:
        return float("inf")
    return (p2[1] - p1[1]) / (p2[0] - p1[0])

# dot product of vectors
def dotP(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

# angle between ab and bc
# got this formula from https://math.stackexchange.com/a/361419
def threeAngle(a, b, c):
    abv = (b[0] - a[0], b[1] - a[1])
    bcv = (c[0] - b[0], c[1] - b[1])

    rdn = dotP(abv, bcv) / (pDist(a, b) * pDist(b, c))
    # adjusting for the fact that due to float multiplication sometimes the radian value ends up being
    # out of its possible range
    if rdn >= 1:
        rdn = 0.999999999999999
    elif rdn <= -1:
        rdn = -0.999999999999999

    angle = math.degrees(math.acos(rdn))

    return -angle


startP = bPoint(plist)
ms = []
# tries to find a point to the right of the lowest point whose slope is closest to 0,
# which would imply it is the next point in the hull to the right of it.
for p in plist:
    if p != startP and p[0] > startP[0]:
        mdev = abs(0 - slope(p, startP))
        ms += [[mdev, p]]
if ms:
    nextP = min(ms, key=lambda a: a[0])[1]
# if the lowest point happens to be the right-most point, it goes the other way and finds the
# next point in the hull to the left
else:
    for p in plist:
        if p != startP and p[0] < startP[0]:
            m = -abs(0 - slope(p, startP))
            ms += [[m, p]]
    nextP = max(ms, key=lambda a: a[0])[1]
    # exchange the order of the line segment since ultimately the checking is anti-clockwise
    # so it must go left->right
    startP, nextP = nextP, startP

hull = [startP, nextP]
reached = False
while not reached:
    p1, p2 = hull[-2], hull[-1]  # the latest line segment found so far
    angles = []
    for p3 in plist:
        if p3 != p1 and p3 != p2:
            # stores the angle every point in the group makes with the latest line segment
            angles += [[threeAngle(p1, p2, p3), p3]]
    foundP = max(angles, key=lambda angs: angs[0])[1]  # the point that makes the largest such angle
    # if the p3 found is already in the hull, consider hull finished
    if foundP in hull:
        reached = True
        break
    hull += [foundP]
print(hull)

# if npoints <= 25:
#     for p1 in plist:
#         for p2 in plist:
#             drawLine(p1, p2, (255, 255, 255))

for i in range(len(hull)):
    drawLine(hull[i], hull[i - 1], (255, 0, 0), 4)

for p in plist:
    drawCircle(p, (255, 255, 255), 1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
