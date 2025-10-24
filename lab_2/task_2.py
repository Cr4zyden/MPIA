import math
import time
import random

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def brute_force_closest_pair(points):
    min_dist = float('inf')
    closest_pair = None
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])
    
    return closest_pair

def closest_pair_divide_conquer(points):
    if len(points) <= 3:
        return brute_force_closest_pair(points)
    
    points_sorted = sorted(points, key=lambda p: p[0])
    mid = len(points_sorted) // 2
    left = points_sorted[:mid]
    right = points_sorted[mid:]
    
    left_pair = closest_pair_divide_conquer(left)
    right_pair = closest_pair_divide_conquer(right)
    
    left_dist = distance(left_pair[0], left_pair[1])
    right_dist = distance(right_pair[0], right_pair[1])
    
    if left_dist < right_dist:
        min_dist = left_dist
        min_pair = left_pair
    else:
        min_dist = right_dist
        min_pair = right_pair
    
    mid_x = points_sorted[mid][0]
    strip = [p for p in points_sorted if abs(p[0] - mid_x) < min_dist]
    strip_sorted = sorted(strip, key=lambda p: p[1])
    
    for i in range(len(strip_sorted)):
        for j in range(i + 1, len(strip_sorted)):
            if strip_sorted[j][1] - strip_sorted[i][1] >= min_dist:
                break
            dist = distance(strip_sorted[i], strip_sorted[j])
            if dist < min_dist:
                min_dist = dist
                min_pair = (strip_sorted[i], strip_sorted[j])
    
    return min_pair

def generate_points(n):
    return [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]

def measure_time():
    sizes = [10, 100, 1000, 10000]
    
    print("N\tВремя перебора\t\tВремя разделяй и властвуй")
    print("-" * 50)
    
    for size in sizes:
        points = generate_points(size)
        
        start = time.time()
        brute_force_closest_pair(points)
        brute_time = time.time() - start
        
        start = time.time()
        closest_pair_divide_conquer(points)
        dc_time = time.time() - start
        
        print(f"{size}\t{brute_time:.6f}\t\t{dc_time:.6f}")

if __name__ == "__main__":
    # Юнит-тесты
    
    # Point distance
    assert distance((2, 2), (2, 3)) == 1
    assert distance((3, 3), (-1, 3)) == 4
    assert abs(distance((2.7, 1.5), (4.7, 2.5)) - math.sqrt(5)) < 1e-9
    
    # Point equal
    assert (3, 2) == (3, 2)
    assert (-2, 1) == (-2, 1)
    assert (3.7, -4.9) == (3.7, -4.9)
    
    # Point not equal
    assert (3, 2) != (2, 3)
    assert (-2, 1) != (-2, 1.5)
    assert (3.7, -4.9) != (3.7, -4.85)
    
    # Point less
    assert (3, 2) < (3, 3)
    assert (-2, 1) < (-2, 2)
    assert (3.7, -4.9) < (3.7, -4.85)
    
    # Point less or equal
    assert (3, 2) <= (3, 3)
    assert (2, 2) <= (2, 2)
    assert (-2, 1) <= (-2, 2)
    assert (-2, -1) <= (-2, -1)
    assert (3.7, -4.9) <= (3.7, -4.85)
    assert (3.7, -4.9) <= (3.7, -4.9)
    
    print("Все предложенные юнит-тесты пройдены успешно")
    
    # Замер времени
    measure_time()