import numpy as np


def circles_intersection_area(circle_a, circle_b):
    x_a, y_a, r_a = circle_a
    x_b, y_b, r_b = circle_b
    distance = np.linalg.norm(np.array([x_a, y_a] - np.array([x_b, y_b])))
    if distance > r_a + r_b:
        return 0

    R = max(r_a, r_b)
    r = min(r_a, r_b)

    if R - r - distance > 0:
        return np.pi * r * r

    part1 = r * r * np.arccos((distance * distance + r * r - R * R) / (2 * distance * r))
    part2 = R * R * np.arccos((distance * distance + R * R - r * r) / (2 * distance * R))
    part3 = 0.5 * np.sqrt((-distance + r + R) * (distance + r - R) * (distance - r + R) * (distance + r + R))

    intersection_area = part1 + part2 - part3
    return intersection_area
