import itertools

def edges_to_matrix(edges):
    if not edges:
        return [], 0

    max_vertex = max(max(u, v) for u, v, _ in edges)
    n = max_vertex + 1
    graph = [[float('inf')] * n for _ in range(n)]

    for u, v, w in edges:
        graph[u][v] = w
        graph[v][u] = w

    for i in range(n):
        graph[i][i] = 0

    return graph, n

def tsp_brute_force(edges):
    if not edges:
        return []

    graph, n = edges_to_matrix(edges)

    all_vertices = set()
    for u, v, _ in edges:
        all_vertices.add(u)
        all_vertices.add(v)

    if len(all_vertices) == 1:
        return []

    start_vertex = min(all_vertices)

    vertices = list(all_vertices)
    vertices.remove(start_vertex)

    min_weight = float('inf')
    best_route = None

    for perm in itertools.permutations(vertices):
        current_route = [start_vertex] + list(perm)
        current_weight = 0

        for i in range(len(current_route) - 1):
            u, v = current_route[i], current_route[i+1]
            if graph[u][v] == float('inf'):
                current_weight = float('inf')
                break
            current_weight += graph[u][v]

        current_weight += graph[current_route[-1]][start_vertex]

        if current_weight < min_weight:
            min_weight = current_weight
            best_route = current_route

    return best_route if best_route else []

def aligned(route, start):
    if not route:
        return route
    try:
        idx = route.index(start)
    except ValueError:
        return route
    return route[idx:] + route[:idx]

def cycles_equal(cycle1, cycle2):
    """Проверяет, являются ли два цикла эквивалентными (с точностью до сдвига и направления)"""
    if len(cycle1) != len(cycle2):
        return False
    if len(cycle1) == 0:
        return True

    n = len(cycle1)
    # Генерируем все возможные сдвиги и их реверсы
    rotations = []
    for i in range(n):
        rotated = cycle1[i:] + cycle1[:i]
        rotations.append(rotated)
        rotations.append(rotated[::-1])

    for rot in rotations:
        if rot == cycle2:
            return True

    return False

def route_weight(route, edges):
    """Вычисляет вес маршрута (включая замыкание)"""
    if len(route) < 2:
        return 0.0
    graph, n = edges_to_matrix(edges)
    total = 0.0
    for i in range(len(route) - 1):
        u, v = route[i], route[i+1]
        total += graph[u][v]
    total += graph[route[-1]][route[0]]  # замыкание
    return total

# --- Тесты ---
if __name__ == "__main__":
    # [TSP] Empty graph
    g = []
    result = tsp_brute_force(g)
    expected = []
    print(f"Empty graph: result={result}, expected={expected}")
    assert cycles_equal(result, expected)
    print("✓ Empty graph")

    # [TSP] Single vertex
    g = []
    result = tsp_brute_force(g)
    expected = []
    print(f"Single vertex: result={result}, expected={expected}")
    assert cycles_equal(result, expected)
    print("✓ Single vertex")

    # [TSP] One edge
    g = [[0, 1, 2.5]]
    result = tsp_brute_force(g)
    expected = [0, 1]
    print(f"One edge: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ One edge")

    # [TSP] Three vertices, three edges
    g = [[0, 1, 2.5], [0, 2, 0.5], [1, 2, 1.0]]
    result = tsp_brute_force(g)
    expected = [0, 1, 2]
    print(f"Three vertices: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ Three vertices")

    # [TSP] Four vertices
    g = [[0, 1, 6.0], [0, 2, 4.0], [0, 3, 1.0],
         [1, 2, 3.5], [1, 3, 2.0],
         [2, 3, 5.0]]
    result = tsp_brute_force(g)
    expected = [0, 2, 1, 3]
    print(f"Four vertices: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ Four vertices")

    # [TSP] Five vertices
    g = [[0, 1, 2.0], [0, 2, 4.0], [0, 3, 1.0], [0, 4, 2.5],
         [1, 2, 3.6], [1, 3, 6.0], [1, 4, 3.0],
         [2, 3, 7.0], [2, 4, 5.0],
         [3, 4, 9.0]]
    result = tsp_brute_force(g)
    expected = [0, 3, 2, 1, 4]
    print(f"Five vertices: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ Five vertices")

    # [TSP] Six vertices
    g = [[0, 1, 2.0], [0, 2, 4.0], [0, 3, 1.0], [0, 4, 2.5], [0, 5, 3.2],
         [1, 2, 3.6], [1, 3, 6.0], [1, 4, 3.0], [1, 5, 0.1],
         [2, 3, 7.0], [2, 4, 5.0], [2, 5, 9],
         [3, 4, 9.0], [3, 5, 0.5],
         [4, 5, 1.0]]
    result = tsp_brute_force(g)
    expected = [0, 3, 2, 1, 5, 4]
    print(f"Six vertices: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ Six vertices")

    print("\n✅ Все тесты пройдены для полного перебора!")
