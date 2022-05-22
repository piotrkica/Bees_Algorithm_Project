import numpy as np


def get_score(antennas, best_solution):
    antennas_total_area = sum([antenna_count * (3.14 * antenna_range ** 2)
                               for antenna_type, (antenna_count, antenna_range) in antennas.items()])

    return best_solution / antennas_total_area


def circles_intersection_area(circle_a, circle_b):
    x_a, y_a, r_a = circle_a
    x_b, y_b, r_b = circle_b
    distance = np.linalg.norm((x_a - x_b, y_a - y_b))
    if distance > r_a + r_b:
        return 0

    R = max(r_a, r_b)
    r = min(r_a, r_b)

    if R - r - distance > 0:
        return int(np.pi * r * r)

    part1 = r * r * np.arccos((distance * distance + r * r - R * R) / (2 * distance * r))
    part2 = R * R * np.arccos((distance * distance + R * R - r * r) / (2 * distance * R))
    part3 = 0.5 * np.sqrt((-distance + r + R) * (distance + r - R) * (distance - r + R) * (distance + r + R))

    intersection_area = part1 + part2 - part3
    return int(intersection_area)
